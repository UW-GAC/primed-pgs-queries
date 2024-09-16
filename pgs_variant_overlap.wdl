version 1.0

workflow pgs_variant_overlap {

    input {
        File target_variant_file
        String? score_ids
    }

    call create_score_id_files {
        input:
            score_ids=score_ids
    }

    scatter (file in create_score_id_files.score_ids_files) {
        call calculate_overlap {
            input:
                target_variant_file=target_variant_file,
                score_ids_file=file
        }
    }

    call combine_overlap_files {
        input:
            files=calculate_overlap.overlap_file
    }

    call render_overlap_report {
        input:
            overlap_file=combine_overlap_files.combined_overlap_file
    }

    output {
        File overlap_file = combine_overlap_files.combined_overlap_file
        Array[File] match_report = calculate_overlap.match_report
        File overlap_report = render_overlap_report.report
    }

    meta {
        author: "Adrienne Stilp"
        email: "amstilp@uw.edu"
    }
}

task create_score_id_files {
    input {
        String? score_ids
    }

    command <<<
        python3 /usr/local/primed-pgs-queries/pgs_variant_overlap/create_score_files.py \
            --output-dir output \
            --variants-per-batch 100000 \
            ~{"--score_ids "  + score_ids}
    >>>
    output {
        Array[File] score_ids_files = glob("output/score_ids_*.txt")
    }
    runtime {
        # Pull from DockerHub
        docker: "uwgac/primed-pgs-queries:0.4.0"
    }
}

task calculate_overlap {
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
    >>>
    output {
        File overlap_file = "overlap_fraction.tsv"
        File match_report="calculate_overlap.html"
    }
    runtime {
        # Pull from DockerHub
        docker: "uwgac/primed-pgs-queries:0.4.0"
        memory: "16 G"
    }
}

task combine_overlap_files {
    input {
        Array[File] files
    }
    command <<<
        # Combine files with the header row from only the first.
        # Stack overflow: xhttps://stackoverflow.com/questions/40027867/how-to-concatenate-multiple-files-with-same-header-some-of-the-files-only-have-h
        awk 'FNR>1 || NR==1' ~{sep=" " files} > overlap_fraction_combined.txt
    >>>
    output {
        File combined_overlap_file = "overlap_fraction_combined.txt"
    }
    runtime {
        # Pull from DockerHub
        docker: "uwgac/primed-pgs-queries:0.4.0"
    }
}

task render_overlap_report {
    input {
        File overlap_file
    }
    command <<<
        cp /usr/local/primed-pgs-queries/pgs_variant_overlap/overlap_report.Rmd .
        R -e "rmarkdown::render('overlap_report.Rmd', params=list(overlap_file='~{overlap_file}'))"
    >>>
    output {
        File report = "overlap_report.html"
    }
    runtime {
        # Pull from DockerHub
        docker: "uwgac/primed-pgs-queries:0.4.0"
    }
}
