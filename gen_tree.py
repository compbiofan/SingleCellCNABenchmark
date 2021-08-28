#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# add copy number, each branch has a copy number variation
# assume the genome is diploid, and not go aneuploid
"""
@authors: Xian Fan Mallory
Contacting email: fan@cs.fsu.edu
"""
# generate tree, along with copy number variation happening to the branches. write the final fasta for each leaf to a file.
# this file is a wrapper from Beta_Splitting_Model.py as of 09052018

# -*- coding: utf-8 -*- 
from anytree import Node, RenderTree
import numpy as np
import graphviz as gv
import sys
import re
from anytree.dotexport import RenderTreeGraph
from CN import CN
from Gen_Ref_Fa import gen_ref, init_ref, write_ref, read_ref

nuc_array = ['A', 'B', 'C', 'D']
# for test purpose
random = 1
cn_list1 = [0, 309, 1282, 381, 176, 1242, 13, 29, 631]
cn_list2 = [744, 319, 1292, 389, 186, 1252, 23, 39, 641]
if_del_list = [0, 1, 0, 0, 1, 1, 1, 1, 1]
allele_list = [0, 1, 0, 1, 1, 0, 1, 0, 1]
amp_num_list = [1, 0, 3, 3, 0, 0, 0, 0, 0]
#cn_list1 = [1139, 1358, 821]
#cn_list2 = [1149, 1368, 831]
#if_del_list = [1, 0, 0]
#allele_list = [0, 1, 1]
#amp_num_list = [0, 3, 1]
#cn_list1 = [203, 211, 359, 72, 638]
#cn_list2 = [213, 219, 369, 82, 648]
#if_del_list = [0, 0, 1, 0, 0]
#allele_list = [1, 1, 0, 1, 1]
#amp_num_list = [2, 1, 0, 1, 1]
#cn_list1 = [443, 712, 731]
#cn_list2 = [453, 722, 741]
#if_del_list = [0, 0, 0]
#allele_list = [1, 0, 0]
#amp_num_list = [1, 1, 2]
#cn_list1 = [398, 432, 392, 396, 641, 659]
#cn_list2 = [408, 442, 402, 406, 649, 669]
#if_del_list = [1, 1, 0, 1, 0, 1]
#allele_list = [1, 0, 1, 1, 0, 1]
#amp_num_list = [0, 0, 1, 0, 2, 0]
#cn_list1 = [10,35,8]
#cn_list2 = [20,45,40]
#if_del_list = [1,1]


# definition of one SNV
class MySNV():
    def __init__(self, ale, chr, pos, ori_nuc, new_nuc):
        #MySNV.__init__(self, ale, chr, pos, ori_nuc, new_nuc)
        self.ale = ale
        self.chr = "NA"
        self.pos = pos
        self.ori_nuc = ori_nuc
        self.new_nuc = new_nuc

class corres_coord():
    def __init__(self, r1, r2, g1, g2):
        #corres_coord.__init__(self, r1, r2, g1, g2)
        self.ref = [r1, r2]
        self.gen = [g1, g2]

class MyNode(Node):
    def __init__(self, name, parent=None):
        Node.__init__(self, name, parent)
        self.id = 0
        self.name = name
        self.parent=parent
        self.tuple=[]
        self.is_dead=False
        self.edge_length = 0
        # alelle length for each chromosome, root has the same as reference
        self.cn=[]
        self.chrlen=[]
        self.ref=[]
        self.snvs=[]
        self.corres=[]
        self.cn_summary={}
        self.cn_detail=[]
        self.parentID = -1
    def getTuple(self):
        return self.tuple
    def setDead(self):
        self.is_dead=True
    def getID(self):
        return self.id

def get_range(chr_len, min_cn_size, exp_theta, CN_LIST_ID):
    # get pos1 and pos2 for the copy number. 
    # skip the first and last "skip" nucleotides (CN does not happen in that range) 
    if random == 0:
        # no randomness
        return cn_list1[CN_LIST_ID], cn_list2[CN_LIST_ID]
        
    else:
        skip = 0
        #skip = 5000000 
        # not try any more if cannot find a good one, just use the end
        trials = 0
        max_n = 10
        cn_size = np.random.exponential(exp_theta) + min_cn_size
        p1 = np.random.uniform(skip, chr_len - skip)
        # make sure p2 not out of boundary
        while chr_len - p1 - skip - cn_size < 0 and trials < max_n:
            p1 = np.random.uniform(skip, chr_len - skip)
            trials = trials + 1
        if p1 + cn_size > chr_len - skip:
            p2 = chr_len - skip - 1
        else:
            p2 = p1 + cn_size
        return int(p1), int(p2)
    
def binary_search(x, array, l, r):
    # find the index i where x < array[i] and x > array[i-1]
    t = l + int((r - l)/2)
    if r > l:
        if x < array[t]:
            r = t
            return binary_search(x, array, l, r)
        else:
            l = t + 1
            return binary_search(x, array, l, r)
    return r

def get_chr(chrlen_array):
    # draw a chromosome with the chance linear to the chromosome length
    acum = []
    for i in range(len(chrlen_array)):
        if i == 0:
            acum.append(chrlen_array[i])
        else:
            acum.append(acum[i-1] + chrlen_array[i])
    # randomly draw a position from the whole genome
    x = np.random.uniform(1, acum[len(chrlen_array)-1])
    return binary_search(x, acum, 0, len(chrlen_array) - 1)

# given a nucleotide, randomly draw a new nucleotide
def get_new_nuc(nuc):
    while True:
        p = abs(int(np.random.uniform(0, 4, 1) - 0.0001))
        new_nuc = nuc_array[p]
        if nuc != new_nuc:
            return new_nuc


    
# given an array of len, find which chr and pos the p on the whole genome corresponds to
def wg2chr(chrlen, p):
    num = 0
    for l in range(len(chrlen)):
        p_ = p - chrlen[l]
        if p_ < 0:
            return num, p
        p = p_
        num = num + 1

    return "NA", -1


# given reference fasta, chrlen, snp_rate, branch length, add snvs by specifying its chr, position and change
def add_SNV(chrlen, ref, snv_rate, length):
    ret_ref = [row[:] for row in ref]
    for ale in range(len(chrlen)):
        # decide how many snvs to be added according to snv_rate and length
        mean = snv_rate * length
        # make it to be a Poisson distribution
        num = np.random.poisson(mean, 1)
        total_l = 0
        for chr in range(len(chrlen[ale])):
            total_l = total_l + chrlen[ale][chr]
        # random over the accumulation of chromosomes, then figure out which chromomome it is
        snv_n = 0
        # dictionary for the ps on the whole genome to avoid duplicated draw
        snv_ps = []
        # to store all the snvs
        snvs = []
        while snv_n < num:
            # draw a snv
            p_tmp = np.random.uniform(1, total_l, 1)
            p = int(p_tmp[0])
            if p not in snv_ps:
                chr, pos = wg2chr(chrlen[ale], p)
                print(chr, pos, ret_ref[ale][chr][pos])
                if ret_ref[ale][chr][pos] != 'N':
                    # add to dictionary
                    snv_ps.append(p)
                    # randomly find a non-N nucleotide and randomly find an alternative for SNV
                    nuc = ret_ref[ale][chr][pos]
                    new_nuc = get_new_nuc(nuc)
                    snvs.append(MySNV(ale, chr, pos, nuc, new_nuc))
                    ret_ref[ale][chr][pos] = new_nuc
        return ret_ref, snvs


def add_CN(chrlen, cn_num, del_rate, min_cn_size, exp_theta, amp_p, corres, CN_LIST_ID):
    # for each branch, the copy number change happens on only one allele
    CN_array = []
    # a variable used only for fixing CN, for test
    new_chrlen = [row[:] for row in chrlen]
    new_corres = [row[:] for row in corres]
    if random == 0:
        CN_Tot = 9
    else:
        CN_Tot = int(np.random.poisson(cn_num, 1))
    for i in range(CN_Tot):
        # allele
        if random == 0:
            CN_Ale = allele_list[i] 
        else:
            CN_Ale = np.random.binomial(1, 0.5)
        # deletion versus amplification 
        if random == 0:
            CN_Del = if_del_list[i]
        else:
            CN_Del = np.random.binomial(1, del_rate)
        CN_chromosome = get_chr(new_chrlen[CN_Ale])
        #print CN_Ale, CN_chromosome
        CN_p1, CN_p2 = get_range(new_chrlen[CN_Ale][CN_chromosome], min_cn_size, exp_theta, i)
        # to protect from str to int, int to str, make it not dividable by 10
        if CN_p1 % 10 == 0:
            CN_p1 = CN_p1 + 1
        if CN_p2 % 10 == 0:
            CN_p2 = CN_p2 - 1
# think about how to get the actual coordinates given the previous ones.
        CN_amp_num = 0
        #print new_chrlen
        #print "before changing:"
        #print chrlen, new_chrlen
        if CN_Del == 0:
            # get amplification copy number
            # starting from 0
            while 1:
                CN_amp_num_ = np.random.geometric(amp_p, 1)
                CN_amp_num = int(CN_amp_num_[0])
                if CN_amp_num >= 1:
                    break;
            if random == 0:
                CN_amp_num = amp_num_list[i]
            #CN_amp_num = int(np.random.geometric(amp_p, 1) - 1)
            #print CN_amp_num, CN_p2, CN_p1
            new_chrlen[CN_Ale][CN_chromosome] = new_chrlen[CN_Ale][CN_chromosome] + CN_amp_num * (CN_p2 - CN_p1)
            #print new_chrlen
        else:
            new_chrlen[CN_Ale][CN_chromosome] = new_chrlen[CN_Ale][CN_chromosome] - (CN_p2 - CN_p1)
            #print new_chrlen
        #print "after changing:"
        #print chrlen, new_chrlen
        # corresp is the corresponding interval of ref and genome
        new_CN = CN(CN_Ale, CN_Del, CN_chromosome, CN_p1, CN_p2, CN_amp_num, new_corres)
        new_corres = get_new_corres(new_CN, new_corres)
        #print_corrs(new_corres)
        CN_array.append(new_CN)
    return CN_array, new_chrlen, new_corres

def print_corrs(corres):
    # print out the correspondence to check its correctness
    for i in range(len(corres)):
        print("allele: " + str(i))
        for j in range(len(corres[i])):
            print("chromosome: " + str(j))
            for k in range(len(corres[i][j])):
                corr = corres[i][j][k]
                ref = corr.ref
                gen = corr.gen
                print("ref: " + str(ref))
                print("gen: " + str(gen))


def print_hash(hash_):
    for key in sorted(hash_):
        print(str(key) + " " + str(hash_[key]))

# given a hash, break all overlapping keys into non-overlapping ones and preserve the value for each segment, key is in start.end
def break_overlap(hash_):
    #bps = sorted(hash_)
    bps = list(hash_.keys())
    # hash that takes in the start or end breakpoint, with the value indicating the cn and status
    ret_hash = {}
    bp_hash = {}
    for i in range(len(bps)):
        bp_s, bp_e = str(bps[i]).split(".")
        bp_s = int(bp_s)
        bp_e = int(bp_e)
        bp_hash[bp_s] = 1
        bp_hash[bp_e] = 1
    bp_array = sorted(bp_hash)
    # make a pair of neighboring bps
    pair_array = []
    for i in range(len(bp_array) - 1):
        pair_array.append(".".join([str(bp_array[i]), str(bp_array[i + 1])]))
    # for each neighboring bp (j), see which intervals (i) contain it
    for i in range(len(bps)):
        cn = hash_[bps[i]]
        i_s, i_e = bps[i].split(".")
        i_s = int(i_s)
        i_e = int(i_e)
        for j in pair_array:
            # check if j is in i, if yes, add i's cn to j
            j_s, j_e = j.split(".")
            j_s = int(j_s)
            j_e = int(j_e)
            # j must be smaller than i
            if j_s >= i_s and j_e <= i_e:
                #key = float(j)
                key = j
                if key in list(ret_hash.keys()):
                    ret_hash[key] = ret_hash[key] + cn
                else:
                    ret_hash[key] = cn 
                            
    return ret_hash
        
# given the correspondence, summarize for each segment, the number of copies (for each allele), and a summary of deletion and amplification (merge neighbors if they are of the same copy number)
def get_cn_from_corres(corres, ref_len):
    cn_detail = []
    for i in range(len(corres)):
        # which allele
        cn_detail_ = []
        for j in range(len(corres[i])):
            # which chromosome 
            hash_ = {}
            #cn_detail_ = []
            for k in range(len(corres[i][j])):
                ref_se = corres[i][j][k].ref
                ref_s = ref_se[0]
                ref_e = ref_se[1]
                key = str(ref_s) + "." + str(ref_e)
                #key = float(key)
                if key in list(hash_.keys()):
                    hash_[key]= hash_[key] + 1
                else:
                    hash_[key] = 1
            # in case some key in hash_ overlap with others, need to break them into nonoverlapping ones
            hash_ = break_overlap(hash_)
            cn_detail_.append(get_cn_detail(hash_, ref_len[j]))
            #print "At allele " + str(i) + ", chromosome " + str(j)
            #print_hash(hash_)
        cn_detail.append(cn_detail_)
    #cn_summary = get_cn_summary(cn_detail)
    cn_summary = get_cn_summary_(cn_detail)
    return cn_detail, cn_summary

# given the detailed cn (abnormal ones) on each allele and each chromosome, summarize by merging alleles, giving the correct answer that the CNV detectors are trying to find
# can deal with collapsed start and end positions
def get_cn_summary_(cn_detail):
     # exchange allele and chromosome
    tmp_range = range(len(cn_detail[0]))
    cn_detail_ = []
    for i in tmp_range:
        cn_detail__ = []
        for j in range(len(cn_detail)):
            cn_detail__.append(0) 
        cn_detail_.append(cn_detail__)

    for i in range(len(cn_detail)):
        for j in range(len(cn_detail[i])):
            cn_detail_[j][i] = cn_detail[i][j]

    ret_summary = {}
    # now starts with chromosome
    for i in range(len(cn_detail_)):
        # a hash table with only the breakpoints, forgetting other info
        bp = {}
        # get the breakpoint hash
        # allele
        for j in range(len(cn_detail_[i])): 
            # chr
            for key in cn_detail_[i][j]:
                s, e = key.split(".")
                s = int(s)
                e = int(e)
                bp[s] = 1
                bp[e] = 1
        # now segment for each neighbor
        bps = sorted(bp)
        pair_bp = {}
        for k in range(len(bps) - 1):
            pair_bp[str(bps[k]) + "." + str(bps[k + 1])] = 1

        # get the copy number for each pair, this will include those that are not CN, will filtered out later on
        ret_summary_ = {}
        pair_bps = list(pair_bp.keys())
        pair_bps.sort(key=natural_keys) 
        for pair in pair_bps:
            pair_s, pair_e = pair.split(".")
            pair_s = int(pair_s)
            pair_e = int(pair_e)
            cn = 0
            tag = 0
            # see which big ones it belong to, if it belongs to nothing, there's no CNV 
            for j in range(len(cn_detail_[i])):
                # each allele get counted once and once only; if not counted, it means that allele is normal, need to add 1 there
                for key in cn_detail_[i][j]:
                    s, e = key.split(".")
                    s = int(s)
                    e = int(e)
                    if pair_s >= s and pair_e <= e:
                        # add the cn of this interval 
                        cn = cn + cn_detail_[i][j][key]
                        tag = tag + 1
            # have to enter each allele if the allele has a cnv, otherwise the cn there is 1
            if tag == 1:
                cn = cn + 1
            elif tag == 0:
                cn = 2
            if cn != 2:
                # only record CNV
                ret_summary_[pair] = cn
        ret_summary[i] = ret_summary_
    return ret_summary
            
# given the detailed cn (abnormal ones) on each allele and each chromosome, summarize by merging alleles, giving the correct answer that the CNV detectors are trying to find
def get_cn_summary(corres):
    cn_summary = {}
    corres_ = []

    # exchange allele and chromosome
    tmp_range = range(len(corres[0]))
    for i in tmp_range:
        corres__ = []
        for j in range(len(corres)):
            corres__.append(0) 
        corres_.append(corres__)

    for i in range(len(corres)):
        for j in range(len(corres[i])):
            corres_[j][i] = corres[i][j]

    for chr in range(len(corres_)):
        union_hash = {}
        # for each chromosome
        cn_summary_ = {}
        for allele in range(len(corres_[chr])):
            # conclude all breakpoints
            tmp_hash = corres_[chr][allele]
            # union the two alleles' cnv
            for key in tmp_hash:
                s, e = key.split(".")
                # make it string with allele
                # record both allele and start and end info in key (s: 0; e: 1; in the second digit after dot)
                key_ = str(s) + "." + str(allele) + str(1) 
                union_hash[key_] = ".".join([str(tmp_hash[key]), str(allele), "s"])
                key_ = str(e) + "." + str(allele) + str(0)
                union_hash[key_] = ".".join([str(tmp_hash[key]), str(allele), "e"])

        # summarize this chromosome
        #bps = sorted(union_hash)
        bps = list(union_hash.keys())
        bps.sort(key=natural_keys)
        prev_SorE = "NA"
        prev_prev_SorE = "NA"
        prev_cn = -1
        prev_prev_cn = -1
        prev_allele = -1
        prev_prev_allele = -1
        for i in range(len(bps)):
            bp = bps[i]
            cn, allele, SorE = union_hash[bp].split(".")
            cn = int(cn)
            bp = int(float(bp))
            if SorE == "s":
                # start
                if prev_SorE == "s":
                    # start for previous, two different alleles, conclude the previous one 
                    if prev_bp != bp:
                        key_ = ".".join([str(prev_bp), str(bp)])
                        cn_ = prev_cn + 1
                        cn_summary_[key_] = cn_
                elif prev_SorE == "e":
                    # can be either from the same or a different allele
                    #if prev_allele != allele:
                        # different, nothing
                    if prev_allele == allele:
                        # same, need to see the previous previous, if it is an s from a different allele, need to take that into account
                        # must have the prev prev as the previous is e
                        if prev_prev_SorE == "s" and prev_prev_allele != allele:
                            if prev_bp != bp:
                                key_ = ".".join([str(prev_bp), str(bp)])
                                cn_ = prev_prev_cn + 1
                                cn_summary_[key_] = cn_
            else:
                # end
                if prev_SorE == "e":
                    # the same, conclude the second e
                    if prev_bp != bp:
                        key_ = ".".join([str(prev_bp), str(bp)])
                        cn_ = cn + 1
                        cn_summary_[key_] = cn_
                elif prev_SorE == "s":
                    # check the previous previous bp
                    if prev_prev_SorE == "s":
                        # s ----------------
                        #        s --- e
                        # or
                        #        s ---------
                        # s ---------- e
                        if prev_bp != bp:
                            key_ = ".".join([str(prev_bp), str(bp)])
                            cn_ = prev_prev_cn + prev_cn
                            cn_summary_[key_] = cn_
                    elif prev_prev_SorE == "e":
                        # e
                        #        s --- e
                        # or
                        # e      s --- e
                        key_ = ".".join([str(prev_bp), str(bp)])
                        cn_ = cn + 1
                        cn_summary_[key_] = cn_
                    elif prev_prev_SorE == "NA":
                        key_ = ".".join([str(prev_bp), str(bp)])
                        cn_ = cn + 1
                        cn_summary_[key_] = cn_
            prev_bp = bp
            prev_prev_allele = prev_allele
            prev_allele = allele
            prev_prev_cn = prev_cn
            prev_cn = cn
            prev_prev_SorE = prev_SorE
            prev_SorE = SorE 
        cn_summary[chr] = cn_summary_
    return cn_summary
           
# human sort to get rid of the problem of having 0 at the end (string to float will miss this info)
def natural_keys(text):
    #return [ atof(c) for c in re.split(r'[+-]?([0-9]+(?:[.][0-9]*)?|[.][0-9]+)', text) ]
    return float(text)

# given a hash table listing the copies of each segment in a chromosome and an allele, as well as the ref length on this chromosome, combine those neighboring segments with the same copy number, find the gap (deletion), return a list with the segments that have CNVs, along with the copy number
def get_cn_detail(hash_, ref_len_):
    ret_dict = {}
    prev_e = -1
    rem_s = -1
    rem_e = -1
    keys_ = list(hash_.keys())
    keys_.sort(key=natural_keys)
    #for key in sorted(hash_):
    for key in keys_:
        s, e = key.split(".")
        s = int(s)
        e = int(e)
        cn = hash_[key]
        # first check if there is a gap
        if prev_e != -1 and prev_e == s:
            # continuous, no gap
            if cn != 1:
                # this is a CNV
                # check if the same as the previous one, if yes, merge
                if prev_cn == cn:
                    rem_e = e
                elif prev_cn != 1:
                    # if previous is also CNV, conclude it
                    seg = ".".join([str(rem_s), str(rem_e)])
                    ret_dict[seg] = prev_cn
                    # start a new one
                    rem_s = s
                    rem_e = e
                else:
                    # prev_cn == 2
                    rem_s = s
                    rem_e = e
            elif prev_cn != 1:
                # this is not a CNV, but the previous is
                # conclude it
                seg = ".".join([str(rem_s), str(rem_e)])
                ret_dict[seg] = prev_cn
                rem_s = -1
                rem_e = -1
        elif prev_e == -1:
            # just started, check if s = 1:
            if s != 0:
                # a gap
                rem_s = 0
                rem_e = s
                # conclude it
                seg = ".".join([str(rem_s), str(rem_e)])
                ret_dict[seg] = 0
            if cn != 1:
                # check if this is a CNV
                rem_s = s
                rem_e = e
        else:
            # there is a gap, record it
            # see first if there's any remnant
            if rem_s != -1:
                seg = ".".join([str(rem_s), str(rem_e)])
                ret_dict[seg] = prev_cn
            seg = ".".join([str(prev_e), str(s)])
            ret_dict[seg] = 0
            if cn != 1:
                rem_s = s
                rem_e = e
        prev_s = s
        prev_e = e
        prev_cn = cn
    # the last part missing
    if prev_e != ref_len_:
        seg = ".".join([str(prev_e), str(ref_len_)])
        ret_dict[seg] = 0
        # the previous previous one hasn't been done yet
        if rem_s != -1:
            seg = ".".join([str(rem_s), str(rem_e)])
            ret_dict[seg] = prev_cn 
    elif rem_e != -1:
        seg = ".".join([str(rem_s), str(rem_e)])
        ret_dict[seg] = prev_cn
    return ret_dict 

# given two positions on the genome, and whether it is a deletion, get the corresponding positions on the reference
def get_correspond_pos(p1, p2, if_del, new_corres, amp_num):
    # this is a list of correspondence
    ret_corres = []
    cnv_sz = p2 - p1
    amp_num = amp_num + 1
    #if len(new_corres) == 1:
    #    # there is only one, meaning that there have never been any CNV happened before
    #    corres = new_corres[0]
    #    r1, r2 = corres.ref
    #    g1, g2 = corres.gen
    #    if if_del == 1:
    #        # break into two
    #        # check if all delete
    #        if g2 - cnv_sz < 0:
    #            print "Not any left after deleting " + p1 + ", " + p2
    #            sys.exit(0)
    #        # p1 not included, always [a, b), including cnv ranges
    #        ret_corres.append(corres_coord(0, p1, 0, p1))
    #        ret_corres.append(corres_coord(p2, r2, p1, g2 - cnv_sz)) 
    #    else:
    #        # break into two, in which a part of ref belongs to both segments
    #        ret_corres.append(corres_coord(0, p2, 0, p2))
    #        ret_corres.append(corres_coord(p1, r2, p1, g2))
    #else:
    i_start = 0
    gen_off = 0
    # there are some segments already there
    for i in range(len(new_corres)):
        r1, r2 = new_corres[i].ref
        g1, g2 = new_corres[i].gen
        if p1 >= g1 and p1 < g2:
            # get p1's ref pos
            p1_ref = p1 - g1 + r1
            if if_del == 1:
                gen_off = - cnv_sz
                # a deletion, get p2
                if p2 <= g2:
                    # simply within this range of correspondence, no other ranges are involved
                    # made into to segments
                    # r1 ---- |  p1_ref  | ---- r2
                    # g1 ---- | p1 -- p2 | ---- g2
                    #ret_corres.append(corres_coord(r1, p1_ref - 1, g1, p1 - 1))
                    #ret_corres.append(corres_coord(p1_ref, r2, p2, g2))
                    #if p1 == g1 and p2 == g2:
                        # just delete this correspondence, not add anything, but everything following need to be updated on gen side
                    if p1 != g1 or p2 != g2:
                        if p1 == g1:
                            # notice on the genome side, it is the coordinate after the deletion, as we are looking at the correspondence of the genome after the deletion
                            ret_corres.append(corres_coord(p1_ref, r2, g1, g1 + (r2 - p1_ref))) 
                        elif p2 == g2:
                            ret_corres.append(corres_coord(r1, r2 - cnv_sz, g1, g2 - cnv_sz)) 
                        else:
                            # the middle part taken, broken into two
                            ret_corres.append(corres_coord(r1, p1_ref, g1, p1))
                            ret_corres.append(corres_coord(p1_ref + cnv_sz, r2, p1, p1 + (r2 - p1_ref - cnv_sz)))
                    # stop and record where it is
                    i_start = i + 1
                    break
                else:
                    # now there are two correspondences involved, thus the deletion is broken into two or more (depending on how many correspondences it involves) on the reference
                    # for this correspondence, there is only one correspondence left
                    # r1 ----| p1_ref 
                    # g1 --- | p1 
                    # see anything left for the header
                    if p1 > g1:
                        ret_corres.append(corres_coord(r1, p1_ref, g1, p1))
                    p2_ref = r2
                    # get the rest of the correspondences
                    i = i + 1
                    r1, r2 = new_corres[i].ref
                    g1, g2 = new_corres[i].gen 
                    while p2 > g2:
                        i = i + 1
                        r1, r2 = new_corres[i].ref
                        g1, g2 = new_corres[i].gen 
                    # all of these are deleted until the rest of the correspondence
                    # r1 ---- (deleted) ---- p2_ref -- r2
                    # g1 ---- (deleted) ---- p2 ------ g2
                    if p2 != g2:
                        p2_ref = r1 + p2 - g1 
                        ret_corres.append(corres_coord(p2_ref, r2, p1, p1 + g2 - p2))
                    i_start = i + 1
                    break
            else:
                # an amplification
                # amp_num includes the original copy, but the shift is just what was added to the genome, so minus 1
                gen_off = cnv_sz * (amp_num - 1)
                #print "g2: " + str(g2) + ", p2: " + str(p2)
                # an amplification, get p2
                if p2 <= g2:
                    # simply within this range of correspondence, no other ranges are involved
                    # made into to segments
                    # r1 ---- |  p1_ref  | ---- r2
                    # g1 ---- | p1 -- p2 | ---- g2
                    #ret_corres.append(corres_coord(r1, p1_ref - 1, g1, p1 - 1))
                    #ret_corres.append(corres_coord(p1_ref, r2, p2, g2))
                    if p1 == g1 and p2 == g2:
                        for j in range(amp_num):
                            ret_corres.append(corres_coord(r1, r2, g1 + j * cnv_sz, g2 + j * cnv_sz))
                        # just delete this correspondence, not add anything, but everything following need to be updated on gen side
                    else:
                        if p1 == g1:
                            # notice on the genome side, it is the coordinate after the deletion, as we are looking at the correspondence of the genome after the deletion
                            for j in range(amp_num):
                                ret_corres.append(corres_coord(r1, r1 + cnv_sz, g1 + j * cnv_sz, g1 + (j + 1) * cnv_sz)) 
                            ret_corres.append(corres_coord(r1 + cnv_sz, r2, g1 + amp_num * cnv_sz, g1 + amp_num * cnv_sz + (r2 - p1_ref))) 
                        elif p2 == g2:
                            ret_corres.append(corres_coord(r1, r2 - cnv_sz, g1, g2 - cnv_sz)) 
                            for j in range(amp_num):
                                ret_corres.append(corres_coord(r2 - cnv_sz, r2, g2 - cnv_sz + j * cnv_sz, g2 - cnv_sz + (j + 1) * cnv_sz))
                        else:
                            # the middle part taken, broken into two
                            ret_corres.append(corres_coord(r1, p1_ref, g1, p1))
                            for j in range(amp_num):
                                ret_corres.append(corres_coord(p1_ref, p1_ref + cnv_sz, p1 + j * cnv_sz, p1 + (j + 1) * cnv_sz))
                            ret_corres.append(corres_coord(p1_ref + cnv_sz, r2, p1 + amp_num * cnv_sz, p1 + amp_num * cnv_sz + (r2 - p1_ref - cnv_sz)))
                    # stop and record where it is
                    i_start = i + 1
                    break
                else:
                    # now there are two correspondences involved, thus the deletion is broken into two or more (depending on how many correspondences it involves) on the reference
                    # for this correspondence, there is only one correspondence left
                    # r1 ----| p1_ref 
                    # g1 --- | p1 
                    # see anything left for the header
                    current_i = i
                    if p1 > g1:
                        ret_corres.append(corres_coord(r1, p1_ref, g1, p1))
                        end = p1
                    elif p1 == g1:
                        end = g1
                    # to keep this value as in the for loop, it will change
                    r2_ori = r2
                    # repeated amp_num times
                    for j in range(amp_num):
                        i = current_i
                        ret_corres.append(corres_coord(p1_ref, r2_ori, end, end + r2_ori - p1_ref))
                        end = end + r2_ori - p1_ref

                        i = i + 1
                        r1, r2 = new_corres[i].ref
                        g1, g2 = new_corres[i].gen
                        
                        while p2 > g2:
                            # deal with the last
                            ret_corres.append(corres_coord(r1, r2, end, end + r2 - r1))
                            end = end + r2 - r1
                            i = i + 1
                            r1, r2 = new_corres[i].ref
                            g1, g2 = new_corres[i].gen

                        # get the residual
                        ret_corres.append(corres_coord(r1, r1 + p2 - g1, end, end + p2 - g1))
                        end = end + p2 - g1

                    # get the residual for the rest of this segment
                    ret_corres.append(corres_coord(r1 + p2 - g1, r2, end, end + r2 - r1 - p2 + g1))
                    i_start = i + 1
                    break
        elif p1 >= g2:
            # not yet
            ret_corres.append(corres_coord(r1, r2, g1, g2))
        # for the rest, p1 < g1, has been taken care of in the while loops above and the following for loop
    # see if there are left to shift on the gen side
    if i_start != 0 and i_start != len(new_corres):
        #print "i_start" + str(i_start)
        for j in range(len(new_corres) - i_start):
            k = j + i_start
            r1, r2 = new_corres[k].ref
            g1, g2 = new_corres[k].gen
            ret_corres.append(corres_coord(r1, r2, g1 + gen_off, g2 + gen_off))

    return ret_corres
        
 
def add_whole_amp(chrlen, whole_amp_rate, whole_amp_num, corres, amp_num_geo_par):
    new_chrlen = [row[:] for row in chrlen]
    new_corres = [row[:] for row in corres]
    # like CN
    wholeamp = []
    for i in range(len(chrlen)):
        # allele
        for j in range(len(chrlen[i])):
            # chromosome
            random_ = np.random.uniform(0.0,1.0)
            if random_ < whole_amp_rate:
                # chosen to be amplified
                # get the amplification number
                # geometric distribution's mean is 1/p = 1.
                amp_num = whole_amp_num * np.random.geometric(amp_num_geo_par)
                while amp_num < 1:
                    amp_num = whole_amp_num * np.random.geometric(amp_num_geo_par)
                new_CN = CN(i, 0, j, 0, new_chrlen[i][j], amp_num, new_corres)
                new_chrlen[i][j] = new_chrlen[i][j] * (amp_num + 1)
                new_corres = get_new_corres(new_CN, new_corres) 
                wholeamp.append(new_CN)
    return wholeamp, new_chrlen, new_corres

def get_new_corres(CN, corres):
    # generate the new correspondence between reference and each allele in the genome 
    ale = CN.CN_Ale
    if_del = CN.CN_Del
    chr = CN.CN_chromosome
    p1 = CN.CN_p1
    p2 = CN.CN_p2
    amp_num = CN.CN_amp_num
    new_corres = [row[:] for row in corres]
    # where the CNA occurs
    c = corres[ale][chr]
    # find where p1 and p2 correspond to on the reference
    ret_corres = get_correspond_pos(p1, p2, if_del, c, amp_num)
    # replace the original new_corres[ale][chr]
    new_corres[ale][chr] = ret_corres
    # return this
    return new_corres
    
    

def is_in(a, mytuple):
    if float(a)>float(mytuple[0]) and float(a)<=float(mytuple[1]):
        return True
    return False

def print_chr_len(chrlen_array):
    print("chr len:")
    print(chrlen_array)
    return ""

# root_mult is the multiplier of the mean CNV on root branch than those on the leaves
# whole_amp: if there's whole chromosome amplification
# whole_amp_rate: rate of an allele on a chromosome chosen to be amplified. 
# whole_amp_num: the mean of the number of copies added
def gen_tree(n, Beta, Alpha, Delta, Output, cn_num, del_rate, min_cn_size, exp_theta, amp_p, template_ref, outfile, fa_prefix, snv_rate, root_mult, whole_amp, whole_amp_rate, whole_amp_num, amp_num_geo_par):
    #n = 4
    #Beta = 0.5
    #Alpha = 0.5
    #Delta = 0
    #Output = "test"
    #cn_num = 1
    #del_rate = 0.5
    #min_cn_size = 200000
    ## exponential distribution
    ## smaller exp_theta means larger chance to get larger CNV 
    #exp_theta = 0.000001
    ## geometric distribution
    ## like simulated annealing, lower amp_p means larger chance to get large CN amp
    #amp_p = 0.5
    ##template_ref = "ref.fasta"
    #template_ref = "/home1/03626/xfan/reference/hg19.fa"
    #outfile = "/work/03626/xfan/lonestar/std.out"
    #fa_prefix = "/work/03626/xfan/lonestar/ref"
    
    ref_array = []
    chr_name_array = []
    chr_sz = []
    #n = int(raw_input("n:"))
    #Beta = float(raw_input("beta:"))
    #Alpha = float(raw_input("alpha:"))
    #Delta = float(raw_input("delta:"))
    #Output = raw_input("output file:")
    #cn_num = int(raw_input("mean copy number:"))
    #del_rate = float(raw_input("deletion rate [0, 1]:"))
    #min_cn_size = int(raw_input("minimum copy number size, recommend > 2000000:"))
    #exp_theta = float(raw_input("parameter for copy number size:"))
    #amp_p = float(raw_input("parameter for amplification allele #:"))
    #template_ref = raw_input("template fasta file:")
    #outfile = raw_input("Output file name:")
    #fa_f_prefix = raw_input("fasta prefix:")
    
    f = open(outfile, "w")
    
    
    
    
    
    #n= int(n)
    #Alpha = float(Alpha)
    #Beta = float(Beta)
    #Delta = float(Delta)
    # add a root (node 0) to the tree
    # edge length (there are at most 2*n - 1))
    #           root
    #            | CN0
    #          node 0
    #        / CN1   \ CN2
    #    node 1    node 2
    ti = np.random.exponential(1,2*n-1)
    #print len(ti)
    Ui = np.random.uniform(0.0,1.0,n-1)
    Vi = np.random.uniform(0.0,1.0,n-1)
    Di = np.random.uniform(0.0,1.0,n-1)
    Bi = np.random.beta(float(Alpha+1),float(Beta+1),n-1)
    
    #Normalizing the branch lengths
    summation = 0
    for t in ti:
        summation += t
    
    for T in range(0,len(ti)):
        ti[T]=float(ti[T])/float(summation)
    
    #print ti
    
    
    #Contructing the phylogeny
    # by default chromosome size
    # from hg19, Navin's 2012 paper
    #chr_sz = [249250621, 243199373, 198022430, 191154276, 180915260, 171115067, 159138663, 146364022, 141213431, 135534747, 135006516, 133851895, 115169878, 107349540, 102531392, 90354753, 81195210, 78077248, 59128983, 63025520, 48129895, 51304566, 155270560, 59373566]
    
    # root is the node before node 0 in tree
    
    root=MyNode("0: [0,1]")
    root.tuple=[0,1]
    ref_array, chr_name_array, chr_sz = init_ref(template_ref)
    chr_sz1 = []
    # data structure for corresponding coordinates for calculating the actual CNV on reference
    # copy so that the two arrays of allele length are independent
    corres2 = []
    for i in chr_sz:
        chr_sz1.append(i)
        corres = corres_coord(0, i, 0, i)
        corres2.append([corres])
        # each corres contains two alleles, each alleles contains all chromosomes, each chromosome contains a list of corres_coord data struture, which has the four tuple of ref1, ref2, gen1, gen2
    root.chrlen=[chr_sz1, chr_sz1]
    root.corres = [corres2, corres2]
    #print chr_sz
    root.id = -1
    
    Tree = []
    Tree.append(MyNode("0: [0,1]"))
    Tree[0].tuple=[0,1]
    Tree[0].id = 0
    CN_LIST_ID = 0
    # whole chromosome amplification
    if whole_amp == 1:
        Tree[0].cn, Tree[0].chrlen, Tree[0].corres = add_whole_amp(root.chrlen, whole_amp_rate, whole_amp_num, root.corres, amp_num_geo_par)
    # assume most of the CN happens on the root branch
        cn_array2, Tree[0].chrlen, Tree[0].corres = add_CN(Tree[0].chrlen, (cn_num * root_mult), del_rate, min_cn_size, exp_theta, amp_p, Tree[0].corres, CN_LIST_ID)
        for x in cn_array2:
            Tree[0].cn.append(x)
    else:
        Tree[0].cn, Tree[0].chrlen, Tree[0].corres = add_CN(root.chrlen, (cn_num * root_mult), del_rate, min_cn_size, exp_theta, amp_p, root.corres, CN_LIST_ID)
    Tree[0].cn_detail, Tree[0].cn_summary = get_cn_from_corres(Tree[0].corres, chr_sz)
    #print "Node 0:"
    #print Tree[0].chrlen
    Tree[0].parent=root
    Tree[0].edge_length = np.random.exponential(1,1)
    
    # update the reference on the node
    #Tree[0].ref = gen_ref(ref_array, Tree[0].cn)
    #tmp_ref = gen_ref(ref_array, Tree[0].cn)
    # memory issue, write it to a file
    #fa_f_prefix = fa_prefix + str(0) + "_"
    #write_ref(tmp_ref, chr_name_array, fa_f_prefix)
    #Tree[0].ref, Tree[0].snvs = add_SNV(Tree[0].chrlen, Tree[0].ref, snv_rate, Tree[0].edge_length)
    
    Tree.append(MyNode(str(1)+":[0,"+"{0:.2f}".format(Bi[0])+"]"+","+"{0:.4f}".format(ti[0])))
    Tree.append(MyNode(str(2)+":["+"{0:.2f}".format(Bi[0])+",1]"+","+"{0:.4f}".format(ti[1])))
    # add copy number
    Tree[1].cn, Tree[1].chrlen, Tree[1].corres = add_CN(Tree[0].chrlen, cn_num, del_rate, min_cn_size, exp_theta, amp_p, Tree[0].corres, CN_LIST_ID)
    Tree[1].cn_detail, Tree[1].cn_summary = get_cn_from_corres(Tree[1].corres, chr_sz)
    #print "Node 1:"
    #print Tree[1].chrlen
    Tree[2].cn, Tree[2].chrlen, Tree[2].corres = add_CN(Tree[0].chrlen, cn_num, del_rate, min_cn_size, exp_theta, amp_p, Tree[0].corres, CN_LIST_ID)
    Tree[2].cn_detail, Tree[2].cn_summary = get_cn_from_corres(Tree[2].corres, chr_sz)
    #print "Node 2:"
    #print Tree[2].chrlen
    
    # update the reference
    #Tree[1].ref = gen_ref(Tree[0].ref, Tree[1].cn)
    #Tree[2].ref = gen_ref(Tree[0].ref, Tree[2].cn)
    # memory issue. at one time at most 2.5 references, each is 6gb (2 alleles). 
    #parent_ref = read_ref(fa_prefix + str(0) + "_")
    #tmp_ref = gen_ref(parent_ref, Tree[1].cn)
    #fa_f_prefix = fa_prefix + str(1) + "_"
    #write_ref(tmp_ref, chr_name_array, fa_f_prefix)
    #tmp_ref = gen_ref(parent_ref, Tree[2].cn)
    #fa_f_prefix = fa_prefix + str(2) + "_"
    #write_ref(tmp_ref, chr_name_array, fa_f_prefix)
    
    Tree[1].parent=Tree[0]
    Tree[2].parent=Tree[0]
    # set parent ID
    Tree[1].parentID = 0
    Tree[2].parentID = 0
    Tree[1].id = 1
    Tree[2].id = 2
    Tree[1].tuple=[0,Bi[0]]
    Tree[2].tuple=[Bi[0],1]
    Tree[1].edge_length = ti[0]
    Tree[2].edge_length = ti[1]
    #Tree[1].ref, Tree[1].snvs = add_SNV(Tree[1].chrlen, Tree[1].ref, snv_rate, Tree[1].edge_length)
    #Tree[2].ref, Tree[2].snvs = add_SNV(Tree[2].chrlen, Tree[2].ref, snv_rate, Tree[2].edge_length)
    
    node_number=2
    j=1
    
    while j<n-1:
        if Vi[j] < Delta :
            for tr in Tree:
                if tr.is_leaf and is_in(Di[j], tr.getTuple()):
                    if (not tr.is_dead):
                        tr.name = tr.name+"*"
                    tr.setDead()
                    break
        else:
            for tree in Tree:
                if tree.is_leaf and is_in(Ui[j], tree.getTuple()) and (not tree.is_dead) :
                    # get the reference of this node, as it is a parent of the following two
                    this_id = tree.getID()
                    #parent_ref = read_ref(fa_prefix + str(this_id) + "_")

                    #print "the node from " + str(node_number + 1) + " to " + str(node_number+2) + "s' parent id: " + str(tree.getID())
                    a,b = tree.getTuple()
                    node_number+=2
                    #Two new children are born here
                    middle = float(Bi[j])*float((float(b)-float(a)))+float(a)
                    Tree.append(MyNode(str(node_number-1)+":["+"{0:.4f}".format(a)+","+"{0:.4f}".format(middle)+"]"+","+"{0:.4f}".format(ti[node_number-1]), parent=tree))
                    Tree.append(MyNode(str(node_number)+":["+"{0:.4f}".format(middle)+","+"{0:.4f}".format(b)+"]"+","+"{0:.4f}".format(ti[node_number]), parent=tree))
    
                    #The new intervals are assigned here
                    Tree[node_number-1].tuple=[a,middle]
                    Tree[node_number].tuple=[middle,b]
                    Tree[node_number-1].edge_length = ti[node_number-1]
                    Tree[node_number].edge_length = ti[node_number]
                    #add copy number
                    this_chrlen = tree.chrlen[:]
                    #print this_chrlen
                    #print node_number, tree.getID()
                    #print "node " + str(node_number - 1)
                    Tree[node_number-1].cn, Tree[node_number-1].chrlen, Tree[node_number-1].corres = add_CN(this_chrlen, cn_num, del_rate, min_cn_size, exp_theta, amp_p, tree.corres, CN_LIST_ID)
                    Tree[node_number-1].cn_detail, Tree[node_number-1].cn_summary = get_cn_from_corres(Tree[node_number-1].corres, chr_sz)
                    this_chrlen = tree.chrlen[:]
                    #print this_chrlen
                    #print node_number, tree.getID()
                    #print "node " + str(node_number)
                    Tree[node_number].cn, Tree[node_number].chrlen, Tree[node_number].corres = add_CN(this_chrlen, cn_num, del_rate, min_cn_size, exp_theta, amp_p, tree.corres, CN_LIST_ID)
                    Tree[node_number].cn_detail, Tree[node_number].cn_summary = get_cn_from_corres(Tree[node_number].corres, chr_sz)
                    this_chrlen = tree.chrlen[:]
                    #print this_chrlen
                    #print node_number, tree.getID()
    
                    # add reference
                    # memory issue
                    #Tree[node_number-1].ref = gen_ref(tree.ref, Tree[node_number-1].cn) 
                    #Tree[node_number].ref = gen_ref(tree.ref, Tree[node_number].cn) 
                    # now do not calculate the ref anyway, as it takes lots of hard disk space. Just get the tree with cn, then at the leaf, trace back all the cns up to root, and apply it to each leaf. This will solve both the memory and hard disk issue. 
                    #tmp_ref = gen_ref(parent_ref, Tree[node_number-1].cn)
                    #fa_f_prefix = fa_prefix + str(node_number-1) + "_"
                    #write_ref(tmp_ref, chr_name_array, fa_f_prefix)
                    #tmp_ref = gen_ref(parent_ref, Tree[node_number].cn)
                    #fa_f_prefix = fa_prefix + str(node_number) + "_"
                    #write_ref(tmp_ref, chr_name_array, fa_f_prefix)

                    # set parent id
                    Tree[node_number].parentID = this_id
                    Tree[node_number-1].parentID = this_id
                    # add snvs
                    #Tree[node_number-1].ref, Tree[node_number-1].snvs = add_SNV(Tree[node_number-1].chrlen, Tree[node_number-1].ref, snv_rate, Tree[node_number-1].edge_length)
                    #Tree[node_number].ref, Tree[node_number].snvs = add_SNV(Tree[node_number].chrlen, Tree[node_number].ref, snv_rate, Tree[node_number].edge_length)
    
                    # set id
                    Tree[node_number-1].id = node_number - 1
                    Tree[node_number].id = node_number
    
                    break
    
        j+=1
    
    #Changing names of the leaves
    #leaf_name=0
    #for nd in Tree:
    #    if nd.is_leaf:
    #        nd.name = leaf_name
    #        leaf_name+=1
    
    #for pre, fill, node in RenderTree(Tree[0]):
    #    print("%s%s" % (pre, node.name))
    
    # record the chromosome length for each leaf on the tree
    leaf_chrlen = []
    # record which are leaves
    leaf_index = []
    f.write("Before the tree, chromosomomal length is " + str(root.chrlen) + "\n")
    for i in range(len(Tree)):
        f.write("node %d: \n" % i)
        f.write("    parent = %d\n" % Tree[i].parent.getID())
        f.write("    name = " + str(Tree[i].name) + "\n")
    for i in range(len(Tree)):
        if Tree[i].is_leaf:
            leaf_index.append(i)
            leaf_chrlen.append(Tree[i].chrlen)
        cn = Tree[i].cn
        f.write("node %d from %d: total CN # = %d\n" % (i, Tree[i].parent.getID(), len(cn)))
        for j in range(len(cn)):
            f.write("    copy number %d: allele: %d, is del: %d, chromosome: %d, position: [%d, %d], amplification #: %d\n" % (j, cn[j].CN_Ale, cn[j].CN_Del, cn[j].CN_chromosome, cn[j].CN_p1, cn[j].CN_p2, cn[j].CN_amp_num))
        # write the copy number summary (on the reference coordinate
        cn_summary = Tree[i].cn_summary
        for chr in sorted(cn_summary):
            f.write("At chromosome %s\n" % (chr))
            cn_summary_ = cn_summary[chr]
            for each_summary in sorted(cn_summary_):
                f.write("   %s, %d\n" % (each_summary, cn_summary_[each_summary]))
        #snvs = Tree[i].snvs
        #for j in range(len(snvs)):
            #f.write("    snv %d: chr: %d, pos: %d, ref_nuc: %s, new_nuc: %s", snvs[j].chr, snvs[j].pos, snvs[j].nuc, snvs[j].new_nuc)
            
        f.write("    " + str(Tree[i].chrlen) + "\n")
            #print_chr_len(Tree[i].chrlen)
    #RenderTreeGraph(Tree[0]).to_picture(str(Output))
    
    
    # generate reference for each leaf
    # memory issue, already written.
    #for i in range(len(Tree)):
    #    fa_f_prefix = fa_prefix + str(i) + "_"
    #    write_ref(Tree[i].ref, chr_name_array, fa_f_prefix)
    
    f.close()
    return leaf_chrlen, leaf_index, chr_name_array, Tree
