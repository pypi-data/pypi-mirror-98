[![Test](https://github.com/tmbdev/webdataset/workflows/Test/badge.svg)](https://github.com/tmbdev/webdataset/actions?query=workflow%3ATest)
[![DeepSource](https://static.deepsource.io/deepsource-badge-light-mini.svg)](https://deepsource.io/gh/tmbdev/webdataset/?ref=repository-badge)

# WebDataset

WebDataset is a PyTorch Dataset (IterableDataset) implementation providing
efficient access to datasets stored in POSIX tar archives and uses only sequential/streaming
data access. This brings substantial performance advantage in many compute environments, and it
is essential for very large scale training.

While WebDataset scales to very large problems, it also works well with smaller datasets and simplifies
creation, management, and distribution of training data for deep learning.

WebDataset implements standard PyTorch `IterableDataset` interface and works with the PyTorch `DataLoader`.
Access to datasets is as simple as:

```Python
import webdataset as wds

dataset = wds.WebDataset(url).shuffle(1000).decode("torchrgb").to_tuple("jpg;png", "json")
dataloader = torch.utils.data.DataLoader(dataset, num_workers=4, batch_size=16)

for inputs, outputs in dataloader:
    ...
```

In that code snippet, `url` can refer to a local file, a local HTTP server, a cloud storage object, an object
on an object store, or even the output of arbitrary command pipelines.

WebDataset fulfills a similar function to Tensorflow's TFRecord/tf.Example
classes, but it is much easier to adopt because it does not actually
require any kind of data conversion: data is stored in exactly the same
format inside tar files as it is on disk, and all preprocessing and data
augmentation code remains unchanged.

# Documentation

- [Getting Started](docs/gettingstarted.ipynb) -- a simple demonstration of how to use WebDataset
- [How It Works](docs/howitworks.ipynb) -- WebDataset is just a collection of PyTorch IterableDataset implementations
- [Decoding](docs/decoding.ipynb) -- WebDataset uses file-based representations internally and its Decoder makes turning these into PyTorch tensors easy
- [Desktop Usage and Caching](docs/desktop.ipynb) -- WebDataset is great for desktop development and supports built-in caching
- [Creating Datasets in WebDataset Format](docs/creating.ipynb) -- there are a variety of tools for creating datasets in WebDataset format
- [Writing WebDataset from Python](docs/writing.ipynb) -- you can write WebDataset datasets directly from Python
- [Multinode Training](docs/multinode.ipynb) -- what you need to know to handle distributed, multi-node training with WebDataset
- [Data Sources](docs/sources.ipynb) -- accessing data on local disks, on web servers, or in cloud storage buckets

# Installation

    $ pip install webdataset

For the Github version:

    $ pip install git+https://github.com/tmbdev/webdataset.git

Documentation: [ReadTheDocs](http://webdataset.readthedocs.io)

# Introductory Videos

Here are some videos talking about WebDataset and large scale deep learning:

- [Introduction to Large Scale Deep Learning](https://www.youtube.com/watch?v=kNuA2wflygM)
- [Loading Training Data with WebDataset](https://www.youtube.com/watch?v=mTv_ePYeBhs)
- [Creating Datasets in WebDataset Format](https://www.youtube.com/watch?v=v_PacO-3OGQ)
- [Tools for Working with Large Datasets](https://www.youtube.com/watch?v=kIv8zDpRUec)

# More Examples

- [loading videos](https://github.com/tmbdev/webdataset/blob/master/docs/video-loading-example.ipynb)
- [splitting raw videos into clips for training](https://github.com/tmbdev/webdataset/blob/master/docs/ytsamples-split.ipynb)
- [converting the Falling Things dataset](https://github.com/tmbdev/webdataset/blob/master/docs/falling-things-make-shards.ipynb)

# Related Libraries and Software

The [AIStore](http://github.com/NVIDIA/aistore) server provides an efficient backend for WebDataset; it functions like a combination of web server, content distribution network, P2P network, and distributed file system. Together, AIStore and WebDataset can serve input data from rotational drives distributed across many servers at the speed of local SSDs to many GPUs, at a fraction of the cost. We can easily achieve hundreds of MBytes/s of I/O per GPU even in large, distributed training jobs.

The [tarproc](http://github.com/tmbdev/tarproc) utilities provide command line manipulation and processing of webdatasets and other tar files, including splitting, concatenation, and `xargs`-like functionality.

The [tensorcom](http://github.com/tmbdev/tensorcom/) library provides fast three-tiered I/O; it can be inserted between [AIStore](http://github.com/NVIDIA/aistore) and [WebDataset](http://github.com/tmbdev/webdataset) to permit distributed data augmentation and I/O. It is particularly useful when data augmentation requires more CPU than the GPU server has available.

You can find the full PyTorch ImageNet sample code converted to WebDataset at [tmbdev/pytorch-imagenet-wds](http://github.com/tmbdev/pytorch-imagenet-wds)
