#!/bin/bash

source blast+-2.2.28

srun tblastn -db /tsl/data/assemblies/fairheas/final_assembly -max_hsps_per_subject 1 -outfmt 6 -max_target_seqs 1 -out results/rxlr_in_secretome_no_signalp_tblastn.out -query results/rxlr_in_secretome_no_signalp.fasta
