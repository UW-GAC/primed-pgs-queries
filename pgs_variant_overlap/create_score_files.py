import argparse
import os
import sys

import pgs_catalog_client

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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create files containing PGS catalog score ids")
    parser.add_argument("--output-dir", type=str, help="Directory in which to save the files", required=True)
    parser.add_argument("--variants-per-batch", type=int, help="Number of variants to include per batch", default=100000)
    args = parser.parse_args()

    # Pull scores from the catalog
    # This does not handle the "next" parameter yet.
    score_api = pgs_catalog_client.ScoreEndpointsApi()
    response = score_api.get_all_scores()
    scores = [{"id": score.id, "n_variants": score.variants_number} for score in response.results]

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
