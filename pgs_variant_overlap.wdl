version 1.0

workflow pgs_variant_overlap {

    input {
        File target_variant_file
    }

    call create_score_id_files {}

    call match_variants {
        input:
            target_variant_file=target_variant_file,
            score_ids_file=create_score_id_files.score_ids_file
    }

    output {
        File overlap_file = match_variants.overlap_file
        File match_report = match_variants.match_report
    }
    meta {
        author: "Adrienne Stilp"
        email: "amstilp@uw.edu"
    }
}

task create_score_id_files {
    command <<<
        # Eventually this will call a python script to generate score id files.
        # For now just create a file with some fixed score ids.
        echo "PGS000822" > score_ids.txt
        echo "PGS001229" >> score_ids.txt
        echo "PGS000011" >> score_ids.txt
        echo "PGS000015" >> score_ids.txt
        echo "PGS000019" >> score_ids.txt
    >>>
    output {
        File score_ids_file = "score_ids.txt"
    }
    runtime {
        # Pull from DockerHub
        docker: "uwgac/primed-pgs-queries:0.4.0"
    }
}

task match_variants {
    input {
        File target_variant_file
        File score_ids_file
    }
    command <<<
        set -e -o pipefail
        mkdir tmp output
        # Download the scoring files
        pgscatalog-download --pgs $(cat ~{score_ids_file}) --build GRCh38 -o tmp/
        # Combine the scoring files
        pgscatalog-combine -s tmp/PGS*.txt.gz -t GRCh38 -o combined.txt.gz
        # Calculate the overlap.
        pgscatalog-match --dataset primed --scorefiles combined.txt.gz --target ~{target_variant_file} --outdir output --only_match
        # Call a script to process overlap.
        cp /usr/local/primed-pgs-queries/pgs_variant_overlap/calculate_overlap.Rmd .
        R -e "rmarkdown::render('calculate_overlap.Rmd', params=list(matches_file='output/0.ipc.zst', combined_scoring_file='combined.txt.gz'))"
        ls
    >>>
    output {
        File overlap_file = "overlap_fraction.tsv"
        File match_report="calculate_overlap.html"
    }
    runtime {
        # Pull from DockerHub
        docker: "uwgac/primed-pgs-queries:0.4.0"
    }
}
