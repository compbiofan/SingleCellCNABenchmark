import sys
import re
import os
if len(sys.argv) <= 1:
    print("""
    Read AneuFinder CNV bed file. For each header with leaf number, make a new file named $prefix${number}.bed, in which the header is CHR, START, END, $prefix${number}, separated by tab, the lines are chromsome, start, end and the absolute copy number. Along with the profile for each leaf, it also outputs a leaves.txt file holding all the leaf numbers (numbers only), one per line. 
    Usage: python
    """ + sys.argv[0] + """ [aneufinder_input] [filename_prefix]""")
    sys.exit(0)

class cn():
    def __init__(self, cn, chr, s, e):
        self.cn = cn
        self.chr = chr
        self.s = s
        self.e = e

l_out = open("leaves.txt", "w")
input_f = sys.argv[1]
prefix = sys.argv[2]
path = os.path.dirname(input_f)
# claim the file handle
f_out = open("tmp", "w")
with open(input_f, "r") as f:
    for l in f:
        if l.find("CNV state") != -1:
            # get the leaf number
            match = re.search(prefix + '(\d+)', l)
            if match:
                leaf_name = prefix + match.group(1)
                l_out.write(match.group(1) + "\n")
            if not f_out.closed:
                f_out.close()
            f_out = open(leaf_name + ".aneufinder.txt", "w")
            f_out.write("\t".join(["CHR", "START", "END", leaf_name]) + "\n")
        else:
            values = l.split()
            values[3] = values[3].replace('-somy', '')
            output_str = "\t".join([values[0], values[1], values[2], values[3]]) + "\n"
            f_out.write(output_str)
 
f.close()
f_out.close()
l_out.close()

# read out the leaf names
with open("leaves.txt", "r") as l_in:
    for l_ in l_in:
        leaf_num = l_.rstrip()
        file_name = prefix + leaf_num + ".aneufinder.txt"
        out_file_name = prefix + leaf_num + ".inferred.bed"
        f_out = open(out_file_name, "w")
        prev_chr = "chr0"
        prev_start = -1
        prev_end = -1
        prev_cn = "0"
        with open(file_name, "r") as f_in:
            # select only those that differ from 2
            j = 0
            for l in f_in:
                values = l.strip().split()
                if values[0] == "CHR":
                    f_out.write(l)
                else:
                    chr_ = values[0]
                    start_ = values[1]
                    end_ = values[2]
                    cn_ = values[3]
                    if cn_ != "2":
                        # aneufinder already concatenate all segments together. only output those non-2's. 
                        f_out.write(l)
                    
        f_out.close()
        f_in.close()
l_in.close()
