import matplotlib as mpl
mpl.use('agg') 
from matplotlib import pyplot as plt 
import matplotlib_venn as vplt
from matplotlib_venn import venn3
from matplotlib_venn import venn2
from matplotlib_venn import venn3_circles
import sys

sample_names = []
subsets_arr = []
infile = sys.argv[1]
outfile = sys.argv[2]
with open(infile,'r') as f:
	for line in f:
		line = line.strip()
		split_arr = line.split(",")
		sample_names.append(split_arr[0])
		only_ginkgo = int(split_arr[1].strip())
		only_hmm = int(split_arr[2].strip())
		All = int(split_arr[-1].strip())
		if "132" not in split_arr[0] and "152" not in split_arr[0]:
			ginkgo_hmm_no_cn = int(split_arr[3].strip())
			only_cn = int(split_arr[4].strip())
			ginkgo_cn_no_hmm = int(split_arr[5].strip())
			hmm_cn_no_ginkgo = int(split_arr[6].strip())
			subsets_arr.append((only_ginkgo,only_hmm,ginkgo_hmm_no_cn,only_cn,ginkgo_cn_no_hmm,hmm_cn_no_ginkgo,All))
		else:
			subsets_arr.append((only_ginkgo,only_hmm,All))
print sample_names
print subsets_arr
fig, axes = plt.subplots(2,3)
for index, axis in enumerate(axes.reshape(-1)):
	if index < len(sample_names):
		# In case the results of CopyNumber is not available, use venn2 instead of venn3 for plotting the diagrams 
		vd = venn3(subsets=subsets_arr[index],set_labels=('Ginkgo','HMMcopy','CopyNumber'),ax=axis)
		for text in vd.set_labels:
			text.set_fontsize(17)
		for text in vd.subset_labels:
			text.set_fontsize(17)
		axis.set_title(str(sample_names[index].replace("s","S")),fontsize=21)
	else:
		axis.axis('off')
fig.set_size_inches(16,14)
plt.tight_layout()

plt.savefig(outfile,dpi=400)
