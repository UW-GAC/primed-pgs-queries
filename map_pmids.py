import argparse
import time

import pandas as pd
import requests


parser = argparse.ArgumentParser()
#parser.add_argument("--pmids", nargs="+", type=int)
parser.add_argument("--pmid-file", type=str, help="CSV file with PMIDs in a column")
parser.add_argument("--pmid-header", type=str, default="PMID", help="Header for PMID column in pmid-file")
args = parser.parse_args()

pubs = pd.read_csv(args.pmid_file)
pmids = pubs[args.pmid_header].tolist()

pgp_url = "https://www.pgscatalog.org/rest/publication/search?pmid={pmid}"
count = 0
for pmid in pmids:
    time.sleep(1) # API is rate-limited at 1000 requests per minute.
    url = pgp_url.format(pmid=pmid)
    response = requests.get(url)
    print(response.json())
    if response.json()['count'] > 0:
        count += 1

print("Pubs associated with a PGP in PGS Catalog: {}/{}".format(count, len(pmids)))
