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

def scatterplot(gt, pre, c, ylim_l, ylim_h, xlim_l, xlim_h, xticks, yticks, size, xlabel, ylabel):
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
    plt.scatter(x, y, c=c, s=size)
    plt.xticks(xticks)
    plt.yticks(yticks)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    
    #plt.show()
    #plt.savefig(fig_file, dpi=400)


def scatterplot_all(gt, pre, size, rect_scatter, t, xlabel, ylabel):
    ax_scatter = plt.axes(rect_scatter)
    plt.text(0, 8.5, t, fontsize=12)
    #plt.tight_layout()
    plt.ylim(1, 8)
    plt.xlim(1, 8)
    #ax = plt.subplot(3, 4, 1)
    #ax.set_aspect('equal')
    for c in gt.keys():
        x = []
        y = []
        for i in gt[c].keys():
            if i in pre[c].keys():
                # only when keys are the same
                x.append(gt[c][i])
                y.append(pre[c][i])
                #print "Add color " + c + " for number " + str(gt[c][i]) + " and " + str(pre[c][i])
        plt.scatter(x, y, c=c, s=size)
    plt.xticks([1, 2, 3, 4, 5, 6, 7])
    plt.yticks([1, 2, 3, 4, 5, 6, 7])
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
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

# s
size = 3

gt, pre, cs = read_meta_f(meta_f)

#plt.subplots(3, 4, figsize=(6, 8))
#plt.subplots_adjust(wspace = 0.3)
plt.figure(figsize=(7, 7))

i = 0
j = 1
ylim_l = 1
ylim_h = 8
xlim_l = 1
xlim_h = 8
xticks = [1, 2, 3, 4, 5, 6, 7]
yticks = [1, 2, 3, 4, 5, 6, 7]
fig_num = 3
w = 0.2
h = 0.2
space1 = 0.01
space = 0.1
w_hist = 0.08

b1 = 0.1
b2 = b1 + h + space
b3 = b2 + h + space
l1 = b1
l2 = l1 + w + space1 + w_hist + space
# draw the total one
rect_scatter = [l1, b3, w, h]
t = "(a)"
xlabel = "actual"
ylabel = "predicted"
scatterplot_all(gt, pre, size, rect_scatter, t, xlabel, ylabel)

for c in cs:
    # scatterplot
    if fig_num == 3:
        l = l2
        b = b3 
        t = "(b)"
    elif fig_num == 5:
        l = l1
        b = b2
        t = "(c)"
    elif fig_num == 7:
        l = l2
        b = b2
        t = "(d)"
    elif fig_num == 9:
        l = l1
        b = b1
        t = "(e)"
    elif fig_num == 11:
        l = l2
        b = b1 
        t = "(f)"
    rect_scatter = [l, b, w, h]
    #ax = plt.subplot(3, 4, fig_num)
    ax_scatter = plt.axes(rect_scatter)
    #ax.set_aspect('equal')
    scatterplot(gt, pre, c, ylim_l, ylim_h, xlim_l, xlim_h, xticks, yticks, size, xlabel, ylabel)
    plt.text(0, 8.5, t, fontsize=12)
    # histogram
    fig_num += 1
    hist_scatter = [l + w + space1, b, w_hist, h] 
    #ax = plt.subplot(3, 4, fig_num)
    ax_histy = plt.axes(hist_scatter)
    ax_histy.hist(pre[c].values(), orientation="horizontal")
    ax_histy.set_ylim(ax_scatter.get_ylim())
    ax_histy.tick_params(labelleft=False)
    fig_num += 1

#plt.show()

#plt.text(-4, 9, "(a)", fontsize=12)

plt.savefig(fig_file, dpi=400)
