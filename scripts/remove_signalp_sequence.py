#!/usr/bin/env python

import sys, re
from Bio import SeqIO




def remove_signalp(filename):
    inputfilename=open(filename)

    for record in SeqIO.parse(inputfilename, "fasta"):
        seqid=record.description
        sequence=str(record.seq)
        match=re.search(r' --NNCleavageSite=\d+ ', seqid)
        if match:
            cleavage_point=match.group(0).strip().split("=")[1]; cleavage_point=int(cleavage_point) - 1

        print ">" + seqid
        print sequence[cleavage_point:]


if __name__=="__main__":
    remove_signalp(sys.argv[1])

exit(0)
