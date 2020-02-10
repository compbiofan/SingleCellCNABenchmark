#!/usr/bin/python$
import numpy
from gen_tree import gen_tree 
from Gen_Ref_Fa import getlen_ref
from gen_tree import get_cn_from_corres
import CN
import argparse
import sys

# a new function added in Feb. 2020
# output a matrix, in which the entry of (i, j) represents the number of events between these two profiles (here assume i and j are both leaves)
def get_pairwise_diff_matrix(tree):
    leaves = get_leafid_array(tree)
    for i in range(len(leaves)):
        for j in range(len(leaves)):
            x = get_pairwise_diff(tree, leaves[i], leaves[j])
            print str(x) + "\t",
        print ""
    

# a new function added in Feb. 2020
# for two leaf cells, output their difference (different event #)
def get_pairwise_diff(tree, i, j):
    p = LCA(tree, i, j)
    #print "LCA of " + str(i) + " and " + str(j) + " is " + str(p)
    e_num_i = get_event_num_path(tree, i, p)
    e_num_j = get_event_num_path(tree, j, p)
    return e_num_i + e_num_j
    
# augmentary function
# given two nodes, get the least common ancestor
def LCA(tree, i, j): 
    P_i = get_path(tree, i)
    P_j = get_path(tree, j)
    for x in P_i:
        for y in P_j:
            if x == y:
                return x
     
# augmentary function
# given the tree and a node, find the path bottom up till it reaches the root
def get_path(tree, i):
    p = tree[i].parent.id
    P = [i]
    while p != -1:
        P.append(p)
        #print p
        p = tree[p].parent.id
    return P 
 
# augmentary funciton
# given a tree, two nodes, one is the ancestor of the other, calculate the total event number from the ancestor to the node
def get_event_num_path(tree, i, p):
    cn_array_num = 0
    while i != p:
        cn_array_num += len(tree[i].cn)
        i = tree[i].parent.id
    return cn_array_num

# a new function added in Jan. 2020
# for each daughter cell compared with a parent cell, output its new CNAs
def get_event_num(tree):
    for t in tree:
        ID = t.id
        cn_array = t.cn
        print str(ID) + "\t" + str(len(cn_array)) + "\t" + str(t.is_leaf)


def get_leaf(tree):
    for t in tree:
        if t.is_leaf:
            print t.id

def get_leafid_array(tree):
    a = []
    for t in tree:
        if t.is_leaf:
            a.append(t.id)
    return a


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


parser = argparse.ArgumentParser(description='Read a tree and output specific items of it. ')
parser.add_argument('-l', '--leaf', action='store_true')  
parser.add_argument('-s', '--summary', action='store_true')  
parser.add_argument('-m', '--make-summary', action='store_true')
parser.add_argument('-r', '--ref', default="")
parser.add_argument('-f', '--file', default="") 
parser.add_argument('-e', '--event', action='store_true')
parser.add_argument('-d', '--pairdist', action='store_true')

args = parser.parse_args()
if_leaf = args.leaf
event_num = args.event
pairdist = args.pairdist
if_summary = args.summary
make_summary = args.make_summary
ref_f = args.ref
npy_f = args.file

# main starts here
if npy_f == "": 
    print("""
    Given a tree in npy format, output its leaf index or the CNV summary. 
    Usage: python read_tree.py -l -s -f -e -d [tree.npy]
        -l  (--leaf)    Print leaf index, one per line. (default: off)
        -s  (--summary) Print CNV summary, one per line (chr, start, end, CN). (default: off)
        -m  (--make-summary)    When the tree does not have CNV summary info but the correspondence, make it and print the CNV info, like -s. Need the -r info to retrieve the info back. (default: off)
        -r  (--ref)     Reference file in .fa. Necessary only when -m is turned on. 
        -f  (--file)    The npy file storing the tree. (mandatory)
        -e  (--event)   Get the number of events (col 2) for each node (col 1) and indicate whether it is a leaf node or not (col 3). 
        -d  (--pairdist)    Get the pairwise distance between all leaf cells. Output the matrix to the stdout. (default: off) 
        """)
    sys.exit(0)


tree = numpy.load(npy_f, allow_pickle=True)
if if_leaf:
    get_leaf(tree)

if if_summary:
    get_summary(tree) 

if make_summary:
    make_summary_func(tree, ref_f)

if event_num:
    get_event_num(tree)

if pairdist:
    get_pairwise_diff_matrix(tree)
    
