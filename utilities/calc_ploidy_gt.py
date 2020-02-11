import sys
import gen_tree
import numpy

if len(sys.argv) <= 1:
    print("""
    Given a folder that contains the ground truth files, a npy file containing the leaf ids, output a file with the first column the leaf name, the second the average ploidy. The ground truth files have the prefix and postfix string as their names.  
    Usage: python
    """ + sys.argv[0] + """ [gt_sep_folder] [leaf.id] [prefix] [postfix]""")
    sys.exit(0)

folder = sys.argv[1]
leaf_npy = sys.argv[2]
prefix = sys.argv[3]
postfix = sys.argv[4]

# hg19 from /projects/nakhleh/xf2/reference/hg19.fa.fai (sum of column 1)
genome_len = 3095677412

def ploidy(f):
    total_length = 0
    p = 0
    with open(f, "r") as fh:
        for l in fh:
            a = l.split("\t")
            length = int(a[2]) - int(a[1])
            total_length += length
            p += length * int(a[3])
    p += (genome_len - total_length) * 2 
    p = float(p)
    p /= genome_len
    fh.close()
    return p

# read the leaf file
leaves = numpy.load(leaf_npy, allow_pickle=True)

# fow each leaf, identify the ground truth file in the folder
for l in leaves:
    leafname = prefix + str(l) + postfix
    file_ = folder + "/" + leafname
    # read the file, get the average ploidy
    p = ploidy(file_)
    print leafname + "\t" + str(p)


