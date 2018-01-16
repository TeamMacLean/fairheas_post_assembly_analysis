directory "results"

namespace :tblastnMap do
  file "results/WYs_tblastn.out" => ["results", "results/WYs.fasta"] do
    sh "source blast+-2.2.28; tblastn -db /tsl/data/assemblies/fairheas/final_assembly -max_hsps_per_subject 1 -outfmt 6 -max_target_seqs 1 -out results/WYs_tblastn.out -query results/WYs.fasta"
  end
  task :run_tblastn => ["results/WYs_tblastn.out"]
end

namespace :get_positions do

  file "results/WYs.txt" => ["tblastnMap:run_tblastn"] do
    sh "python scripts/get_mapped_nucleotide_sequence_from_refseq.py results/WYs.fasta results/WYs_tblastn.out"
  end

  task :run => ["results/WYs.txt"]
end

namespace :get_supersequence do
  file "results/WYs_supersequence.fasta" => ["get_positions:run"] do
    sh "python scripts/get_subseq_from_refseq.py /tsl/data/assemblies/fairheas/final_assembly.fasta results/WYs.fasta"
  end

  task :run => ["results/WYs_supersequence.fasta"]
end


task :default => ["get_supersequence:run"]
