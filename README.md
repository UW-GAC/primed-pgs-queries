# primed-pgs-queries

This repository contains PRIMED queries of the [PGS Catalog](https://www.pgscatalog.org/) using the [PGS Catalog API](https://www.pgscatalog.org/rest-api).

## Usage

### Mapping PubmedIDs to the PGS catalog

The `map_pmids.py` python script can be used to map a list of PubmedIDs to the PGS catalog.
The script requires a csv file containing a list of PubmedIDs (one per line).
The script will output a tsv file containing the PubmedIDs and the corresponding PGS PGP_IDs, PGS_IDs and PGS type (development or evaluation).

The script can be run using the following command:

```
python3 map_pmids.py --pmid-file test_input.csv --outfile test_output.tsv
```

Once you have the mapping output file, you can generate a report about the matches.

```
quarto render mapping_report.qmd -P mapping_results_file:test_output.tsv
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
