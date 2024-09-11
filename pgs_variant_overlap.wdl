version 1.0

workflow pgs_variant_overlap {

    input {
        File target_variant_file
    }

    call match_variants {
        input:
            target_variant_file=target_variant_file
    }

    meta {
        author: "Adrienne Stilp"
        email: "amstilp@uw.edu"
    }
}

task match_variants {
    input {
        File target_variant_file
    }
    command <<<
        set -e -o pipefail
        mkdir tmp output
        # Download the scoring files
        pgscatalog-download --pgs PGS000822 PGS001229 --build GRCh38 -o tmp/
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
    }
    runtime {
        # Pull from DockerHub
        docker: "uwgac/primed-pgs-queries:0.4.0"
    }
}
