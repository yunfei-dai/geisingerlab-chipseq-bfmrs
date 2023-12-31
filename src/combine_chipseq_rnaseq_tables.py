#! /usr/bin/python3

## This script connects the average peak table with RNAseq tables
## There are 3 RNAseq tables
## Input chipseq table is .nearest_orf.tsv

## to do : update input 
import os
import sys
import pandas as pd

def read_rnaseq_table(file):
    df = pd.read_excel(file)
    df = df.set_index("gene_id")
    return df

def main():
    infile = sys.argv[1]
    outfile = sys.argv[2]
    rna_seq_tables = sys.argv[3]
    
    rnaseq_table = {}
    rnaseq_table.update({"BfmRS_WT" : read_rnaseq_table(rnaseq_bfmRS)})
    rnaseq_table.update({"BfmR_WT" : read_rnaseq_table(rnaseq_bfmR)})
    rnaseq_table.update({"BfmS_WT" : read_rnaseq_table(rnaseq_bfmS)})

    test_table = read_rnaseq_table(rnaseq_bfmRS)

    df_chipseq = pd.read_csv(infile, sep='\t')
    df_chipseq = df_chipseq.set_index("locus_tag")

    col_names = ["log2(fold_change)", "significant", "protein_id", "product"]

    for i,j in rnaseq_table.items():
        df_rnaseq = j
        for row, column in df_chipseq.iterrows():
            for k in col_names:
                new_column_name = i + "_" + k
                try:
                    df_chipseq.loc[row, new_column_name] = df_rnaseq.loc[row,k]
                except:
                    pass
    df_chipseq.to_csv(outfile, sep='\t')

if __name__ == "__main__":
        main()
