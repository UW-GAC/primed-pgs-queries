import argparse
import time

import pandas as pd
import progressbar
import requests


parser = argparse.ArgumentParser()
parser.add_argument("--pmid-file", type=str, help="CSV file with PMIDs in a column")
parser.add_argument("--pmid-header", type=str, default="PMID", help="Header for PMID column in pmid-file")
parser.add_argument("--outfile", help="Output tsv file with pmid, pgp_id, pgs_type, and pgs_id")
args = parser.parse_args()

pubs = pd.read_csv(args.pmid_file)
pmids = pubs[args.pmid_header].tolist()

pgp_url = "https://www.pgscatalog.org/rest/publication/search?pmid={pmid}"
pgs_url = "https://www.pgscatalog.org/rest/score/{pgs_id}"
results_list = []
for pmid in progressbar.progressbar(pmids):
    # Loop over pmids to see if they have an associated PGP record.
    time.sleep(1) # API is rate-limited at 1000 requests per minute.
    pgp_response = requests.get(pgp_url.format(pmid=pmid))
    for result in pgp_response.json()["results"]:
        df = (
            pd.concat(pd.DataFrame({'pgs_type':k, 'pgs_id':v}) for k, v in result["associated_pgs_ids"].items())
            .reset_index()
            .drop(columns=["index"])
        )
        # Add PMID and pgp_id to each row.
        df.insert(0, "pm_id", pmid)
        df.insert(1, "pgp_id", result["id"])
        results_list.append(df)

df = pd.concat(results_list)

# Get additional info associated with each PGS
pgs_ids = df["pgs_id"].unique()
results_list = []
for pgs_id in progressbar.progressbar(pgs_ids):
    time.sleep(1) # API is rate-limited at 1000 requests per minute.
    pgs_response = requests.get(pgs_url.format(pgs_id=pgs_id))
    # Note that some PGS have more than one entry in the samples_variants list.
    # assert len(pgs_response.json()["samples_variants"]) == 1
    if len(pgs_response.json()["samples_variants"]) > 1:
        ancestry_broad = "MULTIPLE"
    elif len(pgs_response.json()["samples_variants"]) == 0:
        ancestry_broad = "UNKNOWN"
    else:
        ancestry_broad = pgs_response.json()["samples_variants"][0]["ancestry_broad"]
    results_list.append({
            "pgs_id": pgs_id,
            "trait_reported": pgs_response.json()["trait_reported"],
            "ancestry_broad": ancestry_broad,
    })

df_scores = pd.DataFrame(results_list)

# Combine with publication data.
df = df.merge(df_scores, on="pgs_id", how="left")

# Write to the output file.
df.to_csv(args.outfile, sep="\t", index=False)
