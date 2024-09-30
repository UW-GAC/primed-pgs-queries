"""Script to query PGS catalog and bin score files for later analysis."""
# Note: the following ids do not work with the pgscatalog-combine step.
# See github issue: https://github.com/PGScatalog/pygscatalog/issues/44
# PGS004255
# PGS004256
# PGS004258
# PGS004259
# PGS004260
# PGS004261
# PGS004262
# PGS004263
# PGS004264
# PGS004272
# PGS004273
# PGS004280
# PGS004299
# PGS004301
# PGS004304

import argparse
import os
import sys
import time

import requests

# import pgs_catalog_client

# Define a bin class
class Bin(object):
    """ Container for items that keeps a running sum. """

    def __init__(self):
        self.items = []
        self.weight = 0

    def append(self, item, weight):
        self.items.append(item)
        self.weight += weight

    def __str__(self):
        """ Printable representation """
        return 'Bin(weight=%d, n_items=%s)' % (self.weight, str(len(self.items)))


def pack(items, weight_fn, max_weight):
    """ Pack items into bins with a maximum weight for each bin."""
    items.sort(key=weight_fn)
    bins = []

    for item in items:
        # Try to fit item into a bin
        for bin in bins:
            if bin.weight + weight_fn(item) <= max_weight:
                bin.append(item, weight_fn(item))
                break
        else:
            # item didn't fit into any bin, start a new bin
            bin = Bin()
            bin.append(item, weight_fn(item))
            bins.append(bin)

    return bins


def get_pgs_score_ids(ids=None):
    """Pull scores from the PGS catalog."""
    # I'm not sure how to get the "next" page of results easily using the swagger codegen api bindings.
    # Just call it manually for now.
    url = "https://www.pgscatalog.org/rest/score/all/"
    if ids:
        params = {"filter_ids": ids}
    else:
        params = {}
    response = requests.get(url, params=params).json()
    done = False
    scores = []
    while not done:
        scores = scores + [{"id": score["id"], "n_variants": score["variants_number"]} for score in response["results"]]
        next_url = response["next"]
        if next_url:
            time.sleep(1)
            print(f"Getting next page: {next_url}")
            response = requests.get(next_url).json()
        else:
            done = True
    return scores

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create files containing PGS catalog score ids")
    parser.add_argument("--output-dir", type=str, help="Directory in which to save the files", required=True)
    parser.add_argument("--variants-per-batch", type=int, help="Number of variants to include per batch", default=5000000)
    parser.add_argument("--score_ids", type=str, help="Comma-separated list of score ids to include", default=None)

    args = parser.parse_args()

    scores = get_pgs_score_ids(ids=args.score_ids)

    # Now begin binning the scores.
    bins = pack(scores, lambda x: x["n_variants"], args.variants_per_batch)

    # Write the bins to files
    os.makedirs(args.output_dir, exist_ok=True)
    for i in range(len(bins)):
        filename = f"{args.output_dir}/score_ids_{i}.txt"
        with open(filename, "w") as f:
            for score in bins[i].items:
                f.write(f"{score['id']}\n")
        print(f"Batch {i} written to {filename}")
