version 1.0

workflow map_pubmed_ids_to_pgs_catalog {
    input {
        File pubmed_id_file
        String pmid_column = "PMID"
    }
    call query_pubs {
        input:
            pubmed_id_file=pubmed_id_file,
            pmid_column=pmid_column
    }
    output {
        #File mapping_results_file = map_pubs.mapping_results_file
        File mapping_report = query_pubs.report_file
    }
    meta {
        author: "Adrienne Stilp"
        email: "amstilp@uw.edu"
    }

}


task query_pubs {
    input {
        File pubmed_id_file
        String pmid_column = "PMID"
    }
    command <<<
        # Query PGS catalog and save output.
        python3 /usr/local/primed-pgs-queries/query_pgs_by_pmids.py \
            --pmid-file ~{pubmed_id_file} \
            --pmid-header ~{pmid_column} \
            --outdir "output"
        # Render the report.
        cp /usr/local/primed-pgs-queries/query_pgs_by_pmids.qmd ./
        R -e "rmarkdown::render('query_pgs_by_pmids.qmd', params=list(results_directory='output'))"
    >>>
    output {
        #File mapping_results_file = "mapping_results.tsv"
        File report_file = "query_pgs_by_pmids.html"
    }
    runtime {
        # Pull from DockerHub
        docker: "uwgac/primed-pgs-queries:0.3.0"
    }
}
