# primed-pgs-queries

This repository contains PRIMED queries of the [PGS Catalog](https://www.pgscatalog.org/) using the [PGS Catalog API](https://www.pgscatalog.org/rest-api).

## Available workflows

### Map PubmedIDs to the PGS catalog

The `map_pubmed_ids_to_pgs_catalog` directory contains code to map a list of PubmedIDs to the PGS catalog.

The `query_pgs_by_pmids.py` python script can be used to map a list of PubmedIDs to the PGS catalog.
The script requires either a csv file containing a list of PubmedIDs (one per line) or a URL pointing to such a file.
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
rmarkdown::render("map_pubmed_ids_to_pgs_catalog/query_pgs_by_pmids.Rmd", params=input)
```

A [WDL workflow](https://dockstore.org/workflows/github.com/UW-GAC/primed-pgs-queries/map_pubmed_ids_to_pgs_catalog:main?tab=info) is also provided on Dockstore and as a .WDL file.


### Calculate overlap between PGS Catalog scores and a set of variants

The `pgs_variant_overlap` directory contains code to calculate the overlap between PGS Catalog scores and a set of variants.
The code relies on PGS Catalog utilities provided by [pygscatalog](https://github.com/PGScatalog/pygscatalog).

If you would like to calculate overlap with all scores, the `create_score_files.py` script will query PGS catalog for scores and group the scores into bins with the specified number of variants. Scores can be optionally included or excluded by passing the `--include` or `--exclude` arguments.

```bash
python3 create_score_files.py --output-dir test_output --variants-per-batch 1000
```

To calculate overlap for a set of scores:

1. Download the scoring files from the PGS catalog and combine them.

    ```bash
    pgscatalog-download --pgs PGS000004 PGS000005 --build GRCh38 --outdir output_dir
    pgscatalog-combine -s test_output/PGS*.txt.gz -t GRCh38 -o test_output/combined.txt.gz
    ```
1. Match variants in set of input variants to the combined scoring file. The target variants file must be in .bim format.

    ```bash
    pgscatalog-match --dataset primed --target <input_variants> --scorefiles test_output/combined.txt.gz --outdir output_dir --only_match
    ```
1. Calculate overlap between the set of input varants and the variants in the scoring files using the `calculate_overlap.Rmd` Rmarkdown document.

    ```r
    rmarkdown::render(
        "calculate_overlap.Rmd",
        params=list(
            matches_file="test_output/0.ipc.zst",
            combined_scoring_file="test_output/combined.txt.gz",
            output_file="test_output/overlap_fraction.txt"
        )
    )
    ```
1. Render a report of overlaps using `overlap_report.Rmd` Rmarkdown file using the output.

    ```r
    rmarkdown::render(
        "overlap_report.Rmd",
        params=list(
            overlap_file="test_output/overlap_fraction.txt"
        )
    )
    ```

A [WDL workflow](https://dockstore.org/workflows/github.com/UW-GAC/primed-pgs-queries/pgs_variant_overlap:variant-overlap?tab=info) is also provided on Dockstore and as a .WDL file.


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
