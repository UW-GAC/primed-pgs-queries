from __future__ import print_function
import os
import argparse
import json
import time

import pandas as pd
from progressbar import progressbar

import pgs_catalog_client


def write_to_json(results, filename):
    # Note: you can recreate the model instance with Model(**record.to_dict())
    # eg: Score(**score.to_dict())
    with open(filename, "w") as f:
        f.write(json.dumps([x.to_dict() for x in results], default=str, indent=2))

def get_publication_records(pmids):
    # Create an instance of the API class.
    publication_api = pgs_catalog_client.PublicationEndpointsApi()
    publication_records = []
    for pmid in progressbar(pmids):
        time.sleep(0.5)
        response = publication_api.search_publications(pmid=pmid)
        publication_records = publication_records + response.results
    return publication_records

def get_pgs_records(pgs_ids):
    # Create an instance of the API class.
    score_api = pgs_catalog_client.ScoreEndpointsApi()
    response = score_api.get_all_scores(filter_ids=",".join(pgs_ids))
    if response.next:
        raise NotImplementedError("Pagination not implemented")
    return response.results

def get_metrics_records(pmids):
    # Create an instance of the API class.
    metrics_api = pgs_catalog_client.PerformanceMetricEndpointsApi()
    metrics_records = []
    for pmid in progressbar(pmids):
        time.sleep(0.5)
        response = metrics_api.search_performance_metrics(pmid=pmid)
        metrics_records = metrics_records + response.results
    return metrics_records

if __name__ == "__main__":
    # Parse arguments.
    parser = argparse.ArgumentParser()
    parser.add_argument("--pmid-file", type=str, help="CSV file with PMIDs in a column")
    parser.add_argument("--pmid-header", type=str, default="PMID", help="Header for PMID column in pmid-file")
    parser.add_argument("--outdir", help="Directory in which output will be stored", default=".")

    args = parser.parse_args()

    pubs = pd.read_csv(args.pmid_file)
    pmids = pubs[args.pmid_header].tolist()

    # Read in the file and get PMIDs.
    pubs = pd.read_csv(args.pmid_file)
    pmids = pubs[args.pmid_header].tolist()

    # get PGP records associated with each PMID
    print("Checking for publication records associated with PMIDs...")
    pubs_records = get_publication_records(pmids)

    pgs_ids = []
    for record in pubs_records:
        try:
            pgs_ids = pgs_ids + record.associated_pgs_ids.development
        except AttributeError:
            pass
        try:
            pgs_ids = pgs_ids + record.associated_pgs_ids.evaluation
        except AttributeError:
            pass
    pgs_ids = set(pgs_ids)

    # Get PGS records associated with each publication.
    print("Checking for metrics records...")
    pgs_records = get_pgs_records(pgs_ids)

    # Get any metrics associated with a publication.
    print("Checking for PGS metrics...")
    metrics_records = get_metrics_records(pmids)

    # Write output to a json file.
    os.makedirs(args.outdir, exist_ok=True)
    write_to_json(pubs_records, os.path.join(args.outdir,"records_pubs.json"))
    write_to_json(pgs_records, os.path.join(args.outdir, "records_pgs.json"))
    write_to_json(metrics_records, os.path.join(args.outdir,"records_metrics.json"))
