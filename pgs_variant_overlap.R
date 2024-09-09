# R script to identify overlap between the PGS catalog and a list of variants.

library(tidyverse)
library(httr)
# library(argparser)

# # Create a parser
# p <- arg_parser("Identify overlap percentage between a list of variants and scores in the PGS catalog.")
# # Add command line arguments
# p <- add_arguemnt(p, "--variant-file", help="file containing the list of variants to check", type="string")
# p <- add_argument(p, "--scores", help="comma-separated list of PGS scores to check", type="string")
# # Parse the command line arguments
# argv <- parse_args(p)

# For testing.
argv <- list(
    "variant_file"="bb_ref_overlap_20240906.txt.gz",
    "scores"=NA
)

# Prepare in the file of variants.
# Read as character type for joining later.
variants <- readr::read_tsv(argv$variant_file, col_types=cols(.default = "c")) %>%
    setNames(c("variant")) %>%
    separate(variant, into=c("chr", "pos", "ref", "alt"), sep=":") %>%
    mutate(
        pos=as.integer(pos),
        sorted_alleles=paste(pmin(ref, alt), pmax(ref, alt), sep="/")
    )

# Query the API for all scores.
done <- FALSE

api_url <- "https://www.pgscatalog.org/rest/score/all"
if (!is.na(argv$scores)) {
    response <- GET(api_url, query=list(filter_ids=argv$scores))
} else {
    response <- GET(api_url)
}

i = 1
while (!done) {
    print(i)
    scores <- content(response)$results
    # Subset to the just the first couple scores for testing.
    scores <- scores[1:2]

    results_list = list()
    for (score in scores) {
        # Read in the scoring file.
        # Read all columns as character type for joining later.
        score_variants <- readr::read_tsv(
            score$ftp_harmonized_scoring_files$GRCh38$positions,
            comment="#",
        ) %>%
            mutate(
                sorted_alleles=paste(pmin(effect_allele, other_allele), pmax(effect_allele, other_allele), sep="/")
            ) %>%
            select(chr=hm_chr, pos=hm_pos, sorted_alleles) %>%
            mutate(
                chr=as.character(chr)
            )
        overlap <- inner_join(score_variants, variants, by=c("chr", "pos", "sorted_alleles"))
        results_list[[score$id]] <- tibble(
            n_variants=nrow(score_variants),
            n_overlap=nrow(overlap)
        )
    }

    if (is.null(content(response)[["next"]])) {
        done <- TRUE
    } else {
        response <- GET(content(response)[["next"]])
        i = i + 1
    }
}

results <- bind_rows(results_list, .id="score_id") %>%
    mutate(overlap_fraction = n_overlap / n_variants)
results

write_tsv(results, "pgs_variant_overlap.tsv")
