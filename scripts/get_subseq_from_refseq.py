#!/usr/bin/env python
#usage: python scriptname refseq.fasta protein_sequence.fasta
import sys

from Bio import SeqIO

inputfasta=open(sys.argv[1])

basefilename=sys.argv[2].replace(".fasta", "")



def get_positions(filename):
    inputseqids=open(filename)
    subseq_positions=dict()
    for line in inputseqids:
        line=line.rstrip()
        if line=="": continue
        array=line.split()
        seqid=array[0]
        positionX=array[1]
        positionY=array[2]

        if seqid in subseq_positions.keys():
            subseq_positions[seqid].append((positionX, positionY))
        else:
            subseq_positions[seqid]=[(positionX, positionY)]

    return subseq_positions

#print subseq_positions
subseq_positions=get_positions(basefilename + "_full_length.txt")
multiple_hits_subseq_positions=get_positions(basefilename + "_multiple.txt")
supersequence=open(basefilename + "_supersequence.fasta", "w")
full_length_hits_sequences=open(basefilename + "_full_length_90bp_upstream.fasta", "w")
multiple_hits_sequences=open(basefilename+"_multiplehits.fasta", "w")

super_concat_sequence=""

upstream=90
downstream=0
for record in SeqIO.parse(inputfasta, "fasta"):
    seqid=record.description
    ntseq=str(record.seq)

    #get subsequence now
    if seqid in subseq_positions.keys():
        for positions in subseq_positions[seqid]:
            minpos=int(positions[0])
            maxpos=int(positions[1])
            if minpos > maxpos:
                minpos, maxpos=maxpos, minpos

            #print ">" + seqid
            if minpos - upstream < 0:
                super_concat_sequence+=ntseq[:maxpos+downstream] + "N"
                full_length_hits_sequences.write(">"+seqid+"\n"+ntseq[:maxpos+downstream]+"\n")
            else:
                super_concat_sequence+=ntseq[minpos-upstream:maxpos+downstream]+"N"
                full_length_hits_sequences.write(">"+seqid+"\n"+ntseq[minpos-upstream:maxpos+downstream]+"\n")


    if seqid in multiple_hits_subseq_positions.keys():
        for position in multiple_hits_subseq_positions[seqid]:
            minpos=int(positions[0])
            maxpos=int(positions[1])
            if minpos > maxpos:
                minpos, maxpos=maxpos, minpos
            multiple_hits_sequences.write(">"+seqid+"\n")
            multiple_hits_sequences.write(ntseq[minpos:maxpos] + "\n")


supersequence.write(">SuperSequence\n")
supersequence.write(super_concat_sequence + "\n")
#print ">SuperSequence"
#print super_concat_sequence
multiple_hits_sequences.close()
supersequence.close()
full_length_hits_sequences.close()
exit(0)
