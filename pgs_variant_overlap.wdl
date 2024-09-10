version 1.0

workflow pgs_variant_overlap {

    call match_variants {}

    meta {
        author: "Adrienne Stilp"
        email: "amstilp@uw.edu"
    }
}

task match_variants {
    command <<<
        set -e -o pipefail
        mkdir tmp output
        # Download the scoring files
        pgscatalog-download --pgs PGS000822 PGS001229 --build GRCh38 -o tmp/
        # Combine the scoring files
        pgscatalog-combine -s tmp/PGS*.txt.gz -t GRCh38 -o combined.txt.gz
        # Calculate the overlap.
        pgscatalog-match --dataset primed --scorefiles combined.txt.gz --target inputs/bb_ref_overlap_20240906.bim --outdir output --only_match
        # Call a script to process overlap.
        cp pgs_variant_overlap/calculate_overlap.Rmd .
        R -e "rmarkdown::render('calculate_overlap.Rmd', params=list(matches_file='output/0.ipc.zst', combined_scoring_file='combined.txt.gz'))"
    >>>
    output {
        File overlap_file = "output/overlap.tsv"
    }
    runtime {
        # Pull from DockerHub
        docker: "uwgac/primed-pgs-queries:0.4.0"
    }
}
