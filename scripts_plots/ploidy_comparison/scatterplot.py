import sys
import re
import matplotlib.pyplot as plt

def read_ploidy_f(f):
    dic = {}
    with open(f, "r") as fh:
        for l in fh:
            a = l.rstrip().split("\t")
            # extract the leaf id
            id = re.findall(r'\d+', a[0]) 
            dic[id[0]] = float("{0:.4f}".format(float(a[1])))
    fh.close()
    return dic

def scatterplot(gt, pre, c, ylim_l, ylim_h, xlim_l, xlim_h, xticks, yticks):
    #plt.tight_layout()
    plt.ylim(ylim_l, ylim_h)
    plt.xlim(xlim_l, xlim_h)
    x = []
    y = []
    for i in gt[c].keys():
        if i in pre[c].keys():
            # only when keys are the same
            x.append(gt[c][i])
            y.append(pre[c][i])
    plt.scatter(x, y, c=c)
    plt.xticks(xticks)
    plt.yticks(yticks)
    #plt.show()
    #plt.savefig(fig_file, dpi=400)


def scatterplot_all(gt, pre):
    #plt.tight_layout()
    plt.ylim(0, 6)
    plt.xlim(0, 6)
    ax = plt.subplot(3, 2, 1)
    ax.set_aspect('equal')
    for c in gt.keys():
        x = []
        y = []
        for i in gt[c].keys():
            if i in pre[c].keys():
                # only when keys are the same
                x.append(gt[c][i])
                y.append(pre[c][i])
                #print "Add color " + c + " for number " + str(gt[c][i]) + " and " + str(pre[c][i])
        plt.scatter(x, y, c=c)
    plt.xticks([2, 3, 4, 5, 6])
    plt.yticks([2, 3, 4, 5, 6])
    #axs.show()
    #plt.savefig(fig_file, dpi=400)

def read_meta_f(f):
    gt = {}
    pre = {}
    # colors, each color stand for one ploidy set
    cs = []
    with open(f, "r") as fh:
        for l in fh:
            a = l.rstrip().split("\t")
            gt_f = a[0]
            pre_f = a[1]
            col = a[2]
            cs.append(col)

            gt[col] = read_ploidy_f(gt_f)
            pre[col] = read_ploidy_f(pre_f)

    fh.close()
    return gt, pre, cs
            
 
if len(sys.argv) <= 1:
    print("""
    Given two files, each has two columns, the first the cell id, the second the ploidy of the cell, scatter plot the ploidies. 
    Usage: python
    """ + sys.argv[0] + """ [meta_f:gt,predicted,col in each row] [fig_file_in_full_path]""")
    sys.exit(0)

meta_f = sys.argv[1]
fig_file = sys.argv[2]

gt, pre, cs = read_meta_f(meta_f)

plt.subplots(3, 2, figsize=(6, 8))
plt.subplots_adjust(wspace = 0.3)
scatterplot_all(gt, pre)

i = 0
j = 0
ylim_l = 0
ylim_h = 0
xlim_l = 0
xlim_h = 0
xticks = []
yticks = []
for c in cs:
    j += 1
    if j == 2:
        i += 1
        j = 0
    if i == 0 and j == 1:
        ylim_l = 1.65
        ylim_h = 1.85
        xlim_l = ylim_l
        xlim_h = ylim_h
        ax = plt.subplot(3, 2, 2)
        ax.set_aspect('equal')
        xticks = [1.70, 1.75, 1.80]
        yticks = xticks
    elif i == 1 and j == 0:
        ylim_l = 2.10
        ylim_h = 2.24
        xlim_l = ylim_l
        xlim_h = ylim_h
        ax = plt.subplot(3, 2, 3)
        ax.set_aspect('equal')
        xticks = [2.12, 2.16, 2.2]
        yticks = xticks
    elif i == 1 and j == 1:
        ylim_l = 2.9
        ylim_h = 3.1
        xlim_l = ylim_l
        xlim_h = ylim_h
        ax = plt.subplot(3, 2, 4)
        ax.set_aspect('equal')
        xticks = [2.95, 3.00, 3.05]
        yticks = xticks
    elif i == 2 and j == 0:
        ylim_l = 3.6
        ylim_h = 4
        xlim_l = ylim_l
        xlim_h = ylim_h
        ax = plt.subplot(3, 2, 5)
        ax.set_aspect('equal')
        xticks = [3.7, 3.8, 3.9]
        yticks = xticks
    elif i == 2 and j == 1:
        ylim_l = 4.8
        ylim_h = 5.1
        xlim_l = 5.8
        xlim_h = 6.1
        ax = plt.subplot(3, 2, 6)
        ax.set_aspect('equal')
        xticks = [5.80, 5.95, 6.1]
        yticks = [4.80, 4.95, 5.1]

    scatterplot(gt, pre, c, ylim_l, ylim_h, xlim_l, xlim_h, xticks, yticks)

#plt.show()

plt.savefig(fig_file, dpi=400)
