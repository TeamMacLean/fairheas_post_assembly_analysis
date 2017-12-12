#!/usr/bin/env python

#program to get the sequences that mapped entire protein sequence length and then extract the DNA from the refseq
#usage: python scriptname protein_sequence.fasta tblastn.out
import os, sys

basefilename=sys.argv[1].replace(".fasta", "")

def get_sequence_length(filename):

    os.system(" cat " + filename + " | awk '{if(NR%2==1){gsub(/^>/, \"\", $1); record_id=$1} else if(NR%2==0){print record_id\"\t\"length($0)} }' " + " > " + filename + ".length")


def contruct_length_dictionary(filename):

    lengths=dict()
    get_sequence_length(sys.argv[1])
    length_filename=open(filename + ".length")
    for line in length_filename:
        line=line.rstrip()
        seqid=line.split()[0]
        length=line.split()[1]
        lengths[seqid]=length

    return lengths

def get_full_mapped_sequences(protein_sequence, tblastn_out):
    # get the sequences that mapped full length from tblastn output results
    length_dictionary = contruct_length_dictionary(protein_sequence)
    query_added=[]

    full_length_sequences=open(basefilename + "_full_length.txt", "w")
    multiple=open(basefilename + "_multiple.txt", "w")

    tblastn_filename=open(tblastn_out)
    for line in tblastn_filename:
        line=line.rstrip()
        array=line.split()
        query=array[0]
        subject=array[1]
        query_map_start = array[6]
        query_map_end = array[7]
        subject_map_start = array[8]
        subject_map_end = array[9]
        if query_map_start == '1':

            if query_map_end == length_dictionary[query]:
                if query not in query_added:
                    #print "\t".join(array) + "  full length "  # full length sequences
                    query_added.append(query)
                    full_length_sequences.write("\t".join([subject, subject_map_start, subject_map_end, query, query_map_start, query_map_end]) + "\n")
                else:
                    #print "\t".join(array)  #already added
                    multiple.write("\t".join([subject, subject_map_start, subject_map_end, query, query_map_start, query_map_end]) + "\n")

            #else:
            #    if query not in query_added:
            #        #print "\t".join(array) + "  not full length" # not full length, but occurred only once
            #        query_added.append(query)

            #    else:
            #        continue
        #elif query_map_end == length_dictionary[query]:
        #    print "\t".join(array) + " ends at same length"

        else:
            continue
    full_length_sequences.close()
    multiple.close()



if __name__== "__main__":

    get_full_mapped_sequences(sys.argv[1], sys.argv[2])


exit(0)
