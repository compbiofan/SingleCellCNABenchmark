import sys
sys.path.insert(1, '/home/xf2/github/SingleCellCNABenchmark/')
import gen_tree
import re

if len(sys.argv) <= 1:
    print("""
    Given a SegCopy file, calculate the ploidy for each cell. The output is with two columns, the first the leaf id, the second the ploidy. The cells will be sorted increasingly. 
    Usage: python
    """ + sys.argv[0] + """ [SegCopy] [prefix]""")
    sys.exit(0)

f = sys.argv[1]
prefix = sys.argv[2]

dic = []
leaf_ids = []
total_l = 0
with open(f, "r") as fh:
    for l in fh:
        a = l.split("\t")
        if a[0] != "CHR":
            total_l += 1
            for i in range(len(a)):
                leaf_id = i - 3
                if leaf_id >= 0:
                    if len(dic) - 1 < leaf_id:
                        dic.append(0)
                    dic[leaf_id] += int(a[i])
        else:
            for i in range(len(a)):
                leaf_id = i - 3
                if leaf_id >= 0:
                    str_ = a[i]
                    match = re.search(prefix + '(\d+)', str_)
                    if match:
                        leaf_ids.append(int(match.group(1)))
                    else:
                        print "no " + prefix + " followed by a number in " + l
    
sorted_id = sorted(range(len(leaf_ids)), key=lambda k: leaf_ids[k])
for i in sorted_id:
    # this is where the current leaf can be found
    dic[i] /= float(total_l)
    print "leaf" + str(leaf_ids[i]) + "\t" + str(dic[i])

