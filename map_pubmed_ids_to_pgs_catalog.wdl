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
    call run_pubs_report {
        input:
            score_records_file=query_pubs.score_records_file,
            metrics_records_file=query_pubs.metrics_records_file,
            publication_records_file=query_pubs.publication_records_file
    }
    output {
        #File mapping_results_file = map_pubs.mapping_results_file
        File score_records_file = query_pubs.score_records_file
        File metrics_records_file = query_pubs.metrics_records_file
        File publication_records_file = query_pubs.publication_records_file
        File pubs_report = run_pubs_report.report_file
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
    >>>
    output {
        #File mapping_results_file = "mapping_results.tsv"
        File score_records_file = "output/score_records.json"
        File metrics_records_file = "output/metrics_records.json"
        File publication_records_file = "output/pubs_records.json"
    }
    runtime {
        # Pull from DockerHub
        docker: "uwgac/primed-pgs-queries:0.3.0"
    }
}


task run_pubs_report {
    input {
        File score_records_file
        File metrics_records_file
        File publication_records_file
    }
    command <<<
        cp /usr/local/primed-pgs-queries/query_pgs_by_pmids.qmd ./
        R -e "rmarkdown::render('query_pgs_by_pmids.qmd', params=list(score_records_file='~{score_records_file}', metrics_records_file='~{metrics_records_file}', publication_records_file='~{publication_records_file}'))"
    >>>
    output {
        File report_file = "query_pgs_by_pmids.html"
    }
    runtime {
        docker: "uwgac/primed-pgs-queries:0.3.0"
    }
}
