# primed-pgs-queries

This repository contains PRIMED queries of the [PGS Catalog](https://www.pgscatalog.org/) using the [PGS Catalog API](https://www.pgscatalog.org/rest-api).

## Usage

### Mapping PubmedIDs to the PGS catalog

The `map_pmids.py` python script can be used to map a list of PubmedIDs to the PGS catalog.
The script requires a csv file containing a list of PubmedIDs (one per line).
The script will output three json files in the specified output directory (`--outdir`), which contain the PGS catalog information for the records:
- `pubs_records.json`: A list of publications that have been mapped to the input PubmedIDs.
- `score_records.json`: A list of PGS scores that have been mapped to the input PubmedIDs.
- `metrics_records.json`: A list of PGS metrics that have been mapped to the input PubmedIDs.

The script can be run using the following command:

```
python3 query_pgs_by_pmids.py --pmid-file test_input.csv --outdir test_output
```

Once you have the mapping output, you can generate a report about the matches in R.

```{r}
input <- list(
    "score_records_file" = "test_output/score_records.json",
    "metrics_records_file" = "test_output/metrics_records.json",
    "publication_records_file" = "test_output/pubs_records.json"
)
rmarkdown::render("query_pgs_by_pmids.Rmd", params=input)
```

A [WDL workflow](https://dockstore.org/workflows/github.com/UW-GAC/anvil-util-workflows/backup_data_tables:main?tab=info) is also provided on Dockstore and as a .WDL file.


## Developer info

### Generating the API client

1. Install [swagger-codegen](https://swagger.io/tools/swagger-codegen/).
1. Generate the client.
1. Copy the client to the top-level directory
1. Make sure to include the client requirements in the project requirements file.

The following code can be used:
```bash
# Generate.
swagger-codegen generate -i https://www.pgscatalog.org/static/rest_api/openapi/openapi-schema.yml -l python -o tmp --config swagger_codegen_config.json

# Copy
cp -r tmp/pgs_catalog_client .

# Update requirements.
cp tmp/requirements.txt requirements/client-requirements.in
```

### Building and pushing the docker image

1. Push all changes to the repository. Note that the Docker image will build off the "main" branch on GitHub.

1. Build the image. Make sure to include no caching, or else local scripts will not be updated.

    ```bash
    docker build --no-cache -t uwgac/primed-pgs-queries:X.Y.Z .
    ```

1. Push the image to Docker Hub.

    ```bash
    docker push uwgac/primed-pgs-queries:X.Y.Z
    ```
