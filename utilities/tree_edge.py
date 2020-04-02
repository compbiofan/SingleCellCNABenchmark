#!/usr/bin/python$
import numpy as np
import argparse
import sys
import re

def read_segcopy_f(f):
    fh = open(f, "r")
    first = True
    m = {}
    n = 1
    # a dictionary recording which line each chromosome starts
    chr_starts = {}
    for line in fh:
        if first:
            first = False
            continue
        n += 1
        a = re.split(r'\s+', line.rstrip())
        if a[0] not in m.keys():
            m[a[0]] = []
            chr_starts[a[0]] = n
        m[a[0]].append(int(a[1]))
    fh.close()
    return m, chr_starts
        
    
def query_single_loc_from_segcopy(m, str_, chr_starts): 
    [chr, pos] = str_.split(":")
    pos = int(pos)
    if chr in m.keys():
        for i in range(len(m[chr]) - 1):
            if m[chr][i] <= pos and m[chr][i + 1] > pos:
                print pos, m[chr][i], m[chr][i+1]
                return chr_starts[chr] + i 
    return "NA"

def query_single_loc_print_columns(m, str_, chr_starts, afile, flank, issegcopy):
    line_num = query_single_loc_from_segcopy(m, str_, chr_starts)
    b = line_num - 1 - flank
    if b < 0:
        b = 0
    # read the columns from line_num - flank to line_num + flank on f, for all lines 
    fh = open(afile, "r")
    # parameters for segcopy format
    n = 0
    out_m = []
    for line in fh:
        if not issegcopy:
            a = re.split('\s+', line)
            e = line_num + flank
            if e > len(a):
                e = len(a)
            c = [str(x) for x in a[b:e]]
            print " ".join(c)
        else:
            if n < b:
                n += 1
                continue
            e = line_num + flank
            if n >= e:
                break
            n += 1
            a = re.split('\s+', line)
            out_m.append(a[3:])
    # output the matrix after the t transformation
    if issegcopy:
        for i in np.transpose(np.array(out_m)):
            y = [str(x) for x in i]
            print " ".join(y)
    fh.close() 


parser = argparse.ArgumentParser(description='Using SegCopy file, make query of genomic locations.')
parser.add_argument('-s', '--str', default="")  
parser.add_argument('-f', '--file', default="") 
parser.add_argument('-n', '--line-number-only', action='store_true')
parser.add_argument('-a', '--afile', default="") 
parser.add_argument('-F', '--flank', default=10) 
parser.add_argument('-l', '--is-segcopy', action='store_true') 


args = parser.parse_args()
str_ = args.str
segcopy_f = args.file
afile = args.afile
linenumber = args.line_number_only
flank = int(args.flank)
issegcopy = args.is_segcopy

# main starts here
if segcopy_f == "": 
    print("""
    Given a SegCopy file, return the line number of a certain genomic position, or look at the lines(columns) in this region at another file (cell by region, no header) 
    Usage: python tree_edge.py -s [chr:pos] -f [SegCopy]
        -s  (--str) Input of the genomic location in query in the format of chr:pos. 
        -f  (--file)    The SegCopy file in the same reference as the genomic location is referring to. 
        -a  (--afile)   A file of interest for the particular genomic location (format: cell by genomic region). Extract all cells. 
        -l  (--is-segcopy)   The afile is in segcopy format.
        -F  (--flank)   Come together with -a. The padding on the left or right side for output.
        -n  (--line-number-only)  Only extract line number if true. 
        """)
    sys.exit(0)

genome, chr_starts = read_segcopy_f(segcopy_f)
if linenumber:
    print query_single_loc_from_segcopy(genome, str_, chr_starts)

if afile != "":
    query_single_loc_print_columns(genome, str_, chr_starts, afile, flank, issegcopy)

