import argparse
import time
from collections import Counter
from . import dataset


class TotalSize:

    def __init__(self):
        self.count = 0
        self.total = 0

    def __call__(self, sample):
        self.count += 1
        self.total += sum(len(x) for x in sample.values())
        return sample


def main(args):
    for shard in args.shards:
        print("===", shard)
        totals = TotalSize()
        ds = dataset.Dataset(shard)
        ds.map(totals)
        if args.decode != "":
            ds = ds.decode(*eval("("+args.decode+",)"))
        keys = set()
        skeys = Counter()
        delta = None
        start = None
        for i, sample in enumerate(ds):
            assert sample["__key__"] not in keys, "bad shard: detected duplicate keys"
            if i == 0:
                start = time.time()
            keys = tuple(sorted(set(sample.keys())))
            skeys.update([keys])
            if i >= args.count:
                break
        delta = time.time() - start
        print()
        print(f"#samples/sec: {totals.count/delta:15.2f}")
        print(f"#bytes/sec:   {totals.total/delta:15.2f}")
        print()
        print("sample keys:")
        for key, count in skeys.most_common():
            print(key, count)
        print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Benchmark webdataset data."
    )
    parser.add_argument("-c", "--count", type=int, default=100)
    parser.add_argument("-d", "--decode", default="")
    parser.add_argument("shards", nargs="*")
    args = parser.parse_args()
    main(args)
