directory "results"

namespace :tblastnMap do
  file "results/CCG_in_AA_20-60_tblastn.out" => ["results", "results/CCG_in_AA_20-60.fasta"] do
    sh "source blast+-2.2.28; tblastn -db /tsl/data/assemblies/fairheas/final_assembly -max_hsps_per_subject 1 -outfmt 6 -max_target_seqs 1 -out results/CCG_in_AA_20-60_tblastn.out -query results/CCG_in_AA_20-60.fasta"
  end
  task :run_tblastn => ["results/CCG_in_AA_20-60_tblastn.out"]
end

namespace :get_positions do

  file "results/CCG_in_AA_20-60.txt" => ["tblastnMap:run_tblastn"] do
    sh "python scripts/get_mapped_nucleotide_sequence_from_refseq.py results/CCG_in_AA_20-60.fasta results/CCG_in_AA_20-60_tblastn.out"
  end

  task :run => ["results/CCG_in_AA_20-60.txt"]
end

namespace :get_supersequence do
  file "results/CCG_in_AA_20-60_supersequence.fasta" => ["get_positions:run"] do
    sh "python scripts/get_subseq_from_refseq.py /tsl/data/assemblies/fairheas/final_assembly.fasta results/CCG_in_AA_20-60.fasta"
  end

  task :run => ["results/CCG_in_AA_20-60_supersequence.fasta"]
end


task :default => ["get_supersequence:run"]
