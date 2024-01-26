# primed-pgs-queries

This repository contains PRIMED queries of the [PGS Catalog](https://www.pgscatalog.org/) using the [PGS Catalog API](https://www.pgscatalog.org/rest-api).

## Mapping PubmedIDs to the PGS catalog

The `map_pmids.py` python script can be used to map a list of PubmedIDs to the PGS catalog.
The script requires a csv file containing a list of PubmedIDs (one per line).
The script will output a tsv file containing the PubmedIDs and the corresponding PGS PGP_IDs, PGS_IDs and PGS type (development or evaluation).

The script can be run using the following command:

```
python3 map_pmids.py --input test_input.csv --output test_output.tsv
```

A WDL workflow is also provided.
