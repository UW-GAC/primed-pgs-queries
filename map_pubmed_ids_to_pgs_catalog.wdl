version 1.0

workflow map_pubmed_ids_to_pgs_catalog {
    input {
        File pubmed_id_file
        String pmid_column = "PMID"
    }
    call map_ids {
        input:
            pubmed_id_file=pubmed_id_file,
            pmid_column=pmid_column
    }
    call report {
        input:
            mapping_results_file=map_ids.mapping_results_file
    }
    output {
        File mapping_results_file = map_ids.mapping_results_file
        File mapping_report = report.report_file
    }
    meta {
        author: "Adrienne Stilp"
        email: "amstilp@uw.edu"
    }

}


task map_ids {
    input {
        File pubmed_id_file
        String pmid_column = "PMID"
    }
    command <<<
        python3 /usr/local/primed-pgs-queries/map_pmids.py \
            --pmid-file ~{pubmed_id_file} \
            --pmid-header ~{pmid_column} \
            --outfile mapping_results.tsv
    >>>
    output {
        File mapping_results_file = "mapping_results.tsv"
    }
    runtime {
        # Pull from DockerHub
        docker: "uwgac/primed-pgs-queries:0.2.0"
    }
}


task report {
    input {
        File mapping_results_file
    }
    command <<<
        R -e "rmarkdown::render('/usr/local/primed-pgs-queries/mapping_report.qmd', params=list(mapping_results_file='~{mapping_results_file}'))"
        cp /usr/local/primed-pgs-queries/mapping_report.html ./
    >>>
    output {
        File report_file = "mapping_report.html"
    }
    runtime {
        # Pull from DockerHub
        docker: "uwgac/primed-pgs-queries:0.2.0"
    }
}
