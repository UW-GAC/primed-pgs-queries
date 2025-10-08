version 1.0

workflow filter_pgs_catalog_scores {

    input {
        Array[String] trait_ids = []
        Array[String] cohort_short_names = []
    }

    call filter_scores {
        input:
            trait_ids=trait_ids,
            cohort_short_names=cohort_short_names
    }

    output {
        File all_score_records_file = filter_scores.all_score_records_file
        File? trait_records_file = filter_scores.trait_records_file
        File? cohort_records_file = filter_scores.cohort_records_file
        File filtered_score_id_file = filter_scores.filtered_score_id_file
    }
    meta {
        author: "Adrienne Stilp"
        email: "amstilp@uw.edu"
    }

}


task filter_scores {
    input {
        Array[String] trait_ids = []
        Array[String] cohort_short_names = []
    }

    Array[String] trait_param = prefix("--trait-id ", trait_ids)
    Array[String] remove_param = prefix("--remove ", cohort_short_names)

    command <<<
        python3 /usr/local/primed-pgs-queries/filter_pgs_catalog_scores/filter_pgs_catalog_scores.py \
            ~{sep=" " trait_param} \
            ~{sep=" " remove_param} \
            --outdir "output"

        >>>
    output {
        File all_score_records_file = "output/score_records.json"
        File? trait_records_file = "output/trait_records.json"
        File? cohort_records_file = "output/cohort_records.json"
        File filtered_score_id_file = "output/filtered_score_ids.txt"
    }
    runtime {
        # Pull from DockerHub
        docker: "uwgac/primed-pgs-queries:0.5.1"
    }
}
