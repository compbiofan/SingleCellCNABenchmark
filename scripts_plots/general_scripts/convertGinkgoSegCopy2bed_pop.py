import sys
import os
if len(sys.argv) <= 1:
    print("""
    Read a bed formatted file, find the start and end for continuous non-2 copy numbers from the fourth (0-based) column and output the bed formatted file, with the fourth column the copy number. Each column from the fourth column will form a new bed file, representing a new sample. The bed file name is the column name in the header plus .inferred.bed. The files will be generated in the folder where the input file is.  
    Usage: python 
    """ + sys.argv[0] + """ [input] """) 
    sys.exit(0)


class cn():
    def __init__(self, cn, chr, s, e):
        self.cn = cn
        self.chr = chr
        self.s = s
        self.e = e
    
        
input_f = sys.argv[1]
path = os.path.dirname(input_f)
prev_value = "0"
prev_chr = "chr0"
prev_start = -1
prev_end = -1
sample_names = []
list_f = open(path + "/leaves.txt","w")
sorted_samples = []
# for storing the CNs for each sample
cn_array = []
with open(input_f, "r") as f:
    for l in f:
        # values = l.rstrip().split()
        values = l.strip().split()
        if values[0] == "CHR":
            # header
            for j in range(len(values) - 3):
                # sample_names.append(values[j + 3])
                print values[j+3].split('.')
                leaf_name_array = values[j+3].split('.')
                for k in range(len(leaf_name_array)):
                    if "leaf" in leaf_name_array[k]:
                        sample_names.append(leaf_name_array[k])
                #if len(values[j+3].split('.')) >= 3:
                #    sample_names.append(values[j+3].split('.')[-3])
                #else:
                #    sample_names.append(values[j+3])
        else:
            # record everything there
            cn_array_ = []
            for j in range(len(values) - 3):
                cn_array_.append(cn(values[j + 3], values[0], values[1], values[2]))
            cn_array.append(cn_array_)

cn_alt = []
# get each sample while looping cn_array
for j in range(len(sample_names)):
    cn_alt_ = []
    for i in range(len(cn_array)):
        cn_alt_.append(cn_array[i][j])
    cn_alt.append(cn_alt_)

for i in range(len(sample_names)):
    # for each sample
    print "processing "+sample_names[i]+" ..."
    sample_f = path + "/" + sample_names[i] + ".inferred.bed"
    sorted_samples.append(int(sample_names[i].replace("leaf","")))
    f = open(sample_f, "w")
    prev_value = "0"
    prev_chr = "chr0"
    prev_start = -1
    prev_end = -1

    for j in range(len(cn_alt[i])):
        cn_ = cn_alt[i][j].cn
        chr_ = cn_alt[i][j].chr
        s_ = cn_alt[i][j].s
        e_ = cn_alt[i][j].e
    
        # treat the first line specifically, or a change of chromosome
        if j == 0 or prev_chr != chr_:
            if prev_chr != chr_ and j != 0 and prev_value != "2":
                # conclude the one from the previous chromosome
                str_ = str("\t".join([prev_chr, prev_start, prev_end, prev_value])) + "\n"
                f.write(str_)
            # start a new session
            if cn_ == "2":
                prev_value = "2"
            else:
                prev_chr = chr_
                prev_start = s_
                prev_end = e_
                prev_value = cn_
            continue

        if cn_ != "2" and cn_ != prev_value:
            # a new CNV occurs, conclude the previous one if the prev_value is not 2
            if prev_value != "2":
                str_ = str("\t".join([prev_chr, prev_start, prev_end, prev_value])) + "\n"
                f.write(str_)
            # if prev_value is 2, then nothing to report 
            # refresh the start and chr now
            prev_chr = chr_
            prev_start = s_
            prev_end = e_
            prev_value = cn_
        elif cn_ == "2" and cn_ != prev_value:
            # the previous value is not 2, so now end the previous CNV
            str_ = str("\t".join([prev_chr, prev_start, prev_end, prev_value])) + "\n"
            f.write(str_)
            prev_value = "2"
        elif cn_ == prev_value:
            if prev_value != "2":
                # only update the end
                prev_end = e_

    if prev_value != "2":
        # make it end
        str_ = str("\t".join([prev_chr, prev_start, prev_end, prev_value])) + "\n"
        f.write(str_)

    f.close()
sorted_samples = sorted(sorted_samples)
for i in range(len(sorted_samples)):
    list_f.write(str(sorted_samples[i])+"\n")
list_f.close()
