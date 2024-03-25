from __future__ import print_function
import pgs_catalog_client
import argparse
import json
import pandas as pd


def write_to_json(results, filename):
    # Note: you can recreate the model instance with Model(**record.to_dict())
    # eg: Score(**score.to_dict())
    with open(filename, "w") as f:
        f.write(json.dumps([x.to_dict() for x in results], default=str, indent=2))


if __name__ == "__main__":
    # Parse arguments.
    parser = argparse.ArgumentParser()
    parser.add_argument("--pmid-file", type=str, help="CSV file with PMIDs in a column")
    parser.add_argument("--pmid-header", type=str, default="PMID", help="Header for PMID column in pmid-file")
    parser.add_argument("--outfile", help="Output tsv file with pmid, pgp_id, pgs_type, and pgs_id")
    args = parser.parse_args()

    pubs = pd.read_csv(args.pmid_file)
    pmids = pubs[args.pmid_header].tolist()

    # Create an instance of the API class.
    score_api = pgs_catalog_client.ScoreEndpointsApi()
    pubs_api = pgs_catalog_client.PublicationEndpointsApi()
    metrics_api = pgs_catalog_client.PerformanceMetricEndpointsApi()

    # Read in the file and get PMIDs.
    pubs = pd.read_csv(args.pmid_file)
    pmids = pubs[args.pmid_header].tolist()
    print(pmids)

    # get PGP records associated with each PMID
    # No need - we can just search for the scores/metrics associated with each PMID.

    # Get PGS records associated with each PMID
    # These are PGS scores that are developed in the publication. It does not include evaluation/metrics.
    pgs_records = []
    for pmid in pmids:
        response = score_api.search_scores(pmid=pmid)
        pgs_records = pgs_records + response.results

    # Write output to a json file.
    # Note: you can recreate the score instance with Score(**record.to_dict())
    write_to_json(pgs_records, "records_pgs.json")

    # Get any metrics associated with a publication.
    metrics_records = []
    for pmid in pmids:
        response = metrics_api.search_performance_metrics(pmid=pmid)
        metrics_records = metrics_records + response.results

    # Write output to a json file.
    write_to_json(metrics_records, "records_metrics.json")
