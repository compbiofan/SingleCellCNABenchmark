#!/usr/bin/python$
import numpy
from gen_tree import gen_tree 
from Gen_Ref_Fa import getlen_ref
from gen_tree import get_cn_from_corres
import argparse
import sys

def get_leaf(tree):
    for t in tree:
        if t.is_leaf:
            print t.id


def get_summary(tree):
    for t in tree:
        ID = t.id
        summary = t.cn_summary
        for chr in summary:
            for pos in summary[chr]:
                pos_s, pos_e = pos.split(".")
                cn = summary[chr][pos]
                chr_ = chr + 1
                chr_ = "chr" + str(chr_)
                if chr_ == "chr23":
                    chr_ = "chrX"
                if chr_ == "chr24":
                    chr_ = "chrY"
                print "\t".join([chr_, str(pos_s), str(pos_e), str(cn), str(ID)]) 

# in case the tree does not have the cn summary 
def make_summary_func(tree, ref):
    tmp_name_array, chr_sz = getlen_ref(ref)
    for i in tree:
        i.cn_detail, i.cn_summary = get_cn_from_corres(i.corres, chr_sz)
        ID = i.id
        for chr in i.cn_summary:
            for pos in i.cn_summary[chr]:
                pos_s, pos_e = pos.split(".")
                cn = i.cn_summary[chr][pos]
                chr_ = chr + 1
                chr_ = "chr" + str(chr_)
                if chr_ == "chr23":
                    chr_ = "chrX"
                if chr_ == "chr24":
                    chr_ = "chrY"
                print "\t".join([chr_, str(pos_s), str(pos_e), str(cn), str(ID)]) 


# main starts here
if len(sys.argv) <= 0:
    print("""
    Given a tree in npy format, output its leaf index or the CNV summary. 
    Usage: python read_tree.py -l -s -f [tree.npy]
        -l  (--leaf)    Print leaf index, one per line. (default: off)
        -s  (--summary) Print CNV summary, one per line (chr, start, end, CN). (default: off)
        -m  (--make-summary)    When the tree does not have CNV summary info but the correspondence, make it and print the CNV info, like -s. Need the -r info to retrieve the info back. (default: off)
        -r  (--ref)     Reference file in .fa. Necessary only when -m is turned on. 
        -f  (--file)    The npy file storing the tree. (mandatory)
        """)
    sys.exit(0)

parser = argparse.ArgumentParser(description='Read a tree and output specific items of it. ')
parser.add_argument('-l', '--leaf', action='store_true')  
parser.add_argument('-s', '--summary', action='store_true')  
parser.add_argument('-m', '--make-summary', action='store_true')
parser.add_argument('-r', '--ref', default="")
parser.add_argument('-f', '--file', default="") 

args = parser.parse_args()
if_leaf = args.leaf
if_summary = args.summary
make_summary = args.make_summary
ref_f = args.ref
npy_f = args.file

tree = numpy.load(npy_f)
if if_leaf:
    get_leaf(tree)

if if_summary:
    get_summary(tree) 

if make_summary:
    make_summary_func(tree, ref_f)


