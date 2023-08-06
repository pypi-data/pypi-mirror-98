#!/usr/bin/python
#
# Copyright (c) 2017-2019 NVIDIA CORPORATION. All rights reserved.
# This file is part of the WebDataset library.
# See the LICENSE file for licensing terms (BSD-style).
#


"""Train PyTorch models directly from POSIX tar archive, locally
or over HTTP connections.
"""

__all__ = "WebDataset tariterator default_handlers imagehandler".split()

import pickle
import re
import os

import numpy as np
import json
import tempfile
import io


from .checks import checkmember, checknotnone


check_present = int(os.environ.get("WDS_CHECK_DECODE", 0))


################################################################
# handle basic datatypes
################################################################


def torch_loads(data):
    import io
    import torch

    stream = io.BytesIO(data)
    return torch.load(stream)


def basichandlers(key, data):

    extension = re.sub(r".*[.]", "", key)

    if extension in "txt text transcript":
        return data.decode("utf-8")

    if extension in "cls cls2 class count index inx id".split():
        try:
            return int(data)
        except ValueError:
            return None

    if extension in "json jsn":
        return json.loads(data)

    if extension in "pyd pickle".split():
        return pickle.loads(data)

    if extension in "pth".split():
        return torch_loads(data)

    if extension in "ten tb".split():
        from . import tenbin

        return tenbin.decode_buffer(data)

    if extension in "mp msgpack msg".split():
        import msgpack

        return msgpack.unpackb(data)

    if extension in "npy".split():
        import numpy.lib.format

        stream = io.BytesIO(data)
        return numpy.lib.format.read_array(stream)


################################################################
# handle images
################################################################

imagespecs = {
    "l8": ("numpy", "uint8", "l"),
    "rgb8": ("numpy", "uint8", "rgb"),
    "rgba8": ("numpy", "uint8", "rgba"),
    "l": ("numpy", "float", "l"),
    "rgb": ("numpy", "float", "rgb"),
    "rgba": ("numpy", "float", "rgba"),
    "torchl8": ("torch", "uint8", "l"),
    "torchrgb8": ("torch", "uint8", "rgb"),
    "torchrgba8": ("torch", "uint8", "rgba"),
    "torchl": ("torch", "float", "l"),
    "torchrgb": ("torch", "float", "rgb"),
    "torch": ("torch", "float", "rgb"),
    "torchrgba": ("torch", "float", "rgba"),
    "pill": ("pil", None, "l"),
    "pil": ("pil", None, "rgb"),
    "pilrgb": ("pil", None, "rgb"),
    "pilrgba": ("pil", None, "rgba"),
}


def handle_extension(extensions, f):
    """Returns a decoder function for the list of extensions.

    Extensions can be a space separated list of extensions.
    Extensions can contain dots, in which case the corresponding number
    of extension components must be present in the key given to f.
    Comparisons are case insensitive.

    Examples:

    handle_extension("jpg jpeg", my_decode_jpg)  # invoked for any file.jpg
    handle_extension("seg.jpg", special_case_jpg)  # invoked only for file.seg.jpg
    """
    extensions = extensions.lower().split()

    def g(key, data):
        extension = key.lower().split(".")
        for target in extensions:
            target = target.split(".")
            if len(target) > len(extension):
                continue
            if extension[-len(target) :] == target:
                return f(data)
        return None

    return g


class ImageHandler:
    """Decode image data using the given `imagespec`.

    The `imagespec` specifies whether the image is decoded
    to numpy/torch/pi, decoded to uint8/float, and decoded
    to l/rgb/rgba:

    - l8: numpy uint8 l
    - rgb8: numpy uint8 rgb
    - rgba8: numpy uint8 rgba
    - l: numpy float l
    - rgb: numpy float rgb
    - rgba: numpy float rgba
    - torchl8: torch uint8 l
    - torchrgb8: torch uint8 rgb
    - torchrgba8: torch uint8 rgba
    - torchl: torch float l
    - torchrgb: torch float rgb
    - torch: torch float rgb
    - torchrgba: torch float rgba
    - pill: pil None l
    - pil: pil None rgb
    - pilrgb: pil None rgb
    - pilrgba: pil None rgba

    """

    def __init__(self, imagespec):
        checkmember(imagespec, list(imagespecs.keys()), "unknown image specification")
        self.imagespec = imagespec.lower()

    def __call__(self, key, data):
        import PIL.Image
        extension = re.sub(r".*[.]", "", key)
        if extension.lower() not in "jpg jpeg png ppm pgm pbm pnm".split():
            return None
        imagespec = self.imagespec
        atype, etype, mode = imagespecs[imagespec]
        with io.BytesIO(data) as stream:
            img = PIL.Image.open(stream)
            img.load()
            img = img.convert(mode.upper())
        if atype == "pil":
            return img
        elif atype == "numpy":
            result = np.asarray(img)
            checkmember(result.dtype, [np.uint8])
            if etype == "uint8":
                return result
            else:
                return result.astype("f") / 255.0
        elif atype == "torch":
            import torch

            result = np.asarray(img)
            checkmember(result.dtype, [np.uint8])
            if etype == "uint8":
                result = np.array(result.transpose(2, 0, 1))
                return torch.tensor(result)
            else:
                result = np.array(result.transpose(2, 0, 1))
                return torch.tensor(result) / 255.0
        return None


def imagehandler(imagespec):
    return ImageHandler(imagespec)


################################################################
# torch video
################################################################


def torch_video(key, data):
    extension = re.sub(r".*[.]", "", key)
    if extension not in "mp4 ogv mjpeg avi mov h264 mpg webm wmv".split():
        return None

    import torchvision.io

    with tempfile.TemporaryDirectory() as dirname:
        fname = os.path.join(dirname, f"file.{extension}")
        with open(fname, "wb") as stream:
            stream.write(data)
        return torchvision.io.read_video(fname, pts_unit="sec")


################################################################
# torchaudio
################################################################


def torch_audio(key, data):
    extension = re.sub(r".*[.]", "", key)
    if extension not in ["flac", "mp3", "sox", "wav", "m4a", "ogg", "wma"]:
        return None

    import torchaudio

    with tempfile.TemporaryDirectory() as dirname:
        fname = os.path.join(dirname, f"file.{extension}")
        with open(fname, "wb") as stream:
            stream.write(data)
        return torchaudio.load(fname)


################################################################
# special class for continuing decoding
################################################################


class Continue:
    """Special class for continuing decoding.

    This is mostly used for decompression, as in:

        def decompressor(key, data):
            if key.endswith(".gz"):
                return Continue(key[:-3], decompress(data))
            return None
    """

    def __init__(self, key, data):
        self.key, self.data = key, data


def gzfilter(key, data):
    import gzip

    if not key.endswith(".gz"):
        return None
    decompressed = gzip.open(io.BytesIO(data)).read()
    return Continue(key[:-3], decompressed)


################################################################
# a sample decoder
################################################################


default_pre_handlers = [gzfilter]
default_post_handlers = [basichandlers]


class Decoder:
    """Decode samples using a list of handlers.

    For each key/data item, this iterates through the list of
    handlers until some handler returns something other than None.
    """

    def __init__(self, handlers, pre=None, post=None):
        if pre is None:
            pre = default_pre_handlers
        if post is None:
            post = default_post_handlers
        assert all(callable(h) for h in handlers), f"one of {handlers} not callable"
        assert all(callable(h) for h in pre), f"one of {pre} not callable"
        assert all(callable(h) for h in post), f"one of {post} not callable"
        self.handlers = pre + handlers + post

    def decode1(self, key, data):
        key = "." + key
        for f in self.handlers:
            result = f(key, data)
            if isinstance(result, Continue):
                key, data = result.key, result.data
                continue
            if result is not None:
                return result
        return data

    def decode(self, sample):
        result = {}
        assert isinstance(sample, dict), sample
        for k, v in list(sample.items()):
            if k[0] == "_":
                if isinstance(v, bytes):
                    v = v.decode("utf-8")
                result[k] = v
                continue
            checknotnone(v)
            result[k] = self.decode1(k, v)
        return result

    def __call__(self, sample):
        assert isinstance(sample, dict), (len(sample), sample)
        return self.decode(sample)
