import os
from os import walk 
import numpy as np 
import matplotlib as mpl  
import sys
import pandas as pd
import seaborn as sns
import matplotlib.transforms as transforms
import pandas as pd

mpl.use('agg')

import matplotlib.pyplot as plt
### Define a class for the breakpoints 

def set_box_color(bp, color):
    plt.setp(bp['boxes'], color=color)
    plt.setp(bp['whiskers'], color=color)
    plt.setp(bp['caps'], color=color)
    plt.setp(bp['medians'], color=color)


class bp():

	def __init__(self, chr, pos, cn, stat):
		
		##### All the values are integers
		##### stat=-2: to be decided,
		##### stat=1: rising edge
		##### stat=-1: falling edge
		self.chr = chr 
		self.pos = pos
		self.cn = cn
		self.stat = stat
		self.flag = 0
	def set_flag(self,state):
		self.flag = state
		return


def chr_extract(chr):
	if chr[-1]=="X" or chr[-1]=="x":
		return 23
	elif chr[-1]=="Y" or chr[-1]=="y":
		return 24
	else:
		chrString = ""
		for i in chr:
			if i.isdigit():
				chrString+=i
		return int(chrString)


##### This function parses the files (ground truth or inferred), labels the breakpoints qualitatively 
##### and saves them into an array
def Parse(bp_array,address,file_type):
	last_chrom=-1
	last_bp=None
	chrom=-1
	start=0
	end=0
	with open(address,"r") as file:
				for l in file:
					if "not_mappable" in l:
						continue
					if file_type=="ref":
						split=l.strip().split('\t')
						chrom=int(chr_extract(split[0]))
						start=int(split[1])
						end=int(split[2])
						copy_number=int(split[3])
					else:
						##### If the file is the inferred bed file, the first block shows the result
						split=l.strip().split('\t')
						chrom=int(chr_extract(split[0]))
						start=int(split[1])
						end=int(split[2])
						copy_number=int(split[3])
					if chrom!=last_chrom:
						### The chromosome has changed 
						if last_bp!=None:
							if last_bp.cn>2:
								#### in the last breakpoint in the previous chromosome, there is a copy number greater than 2
								#### which points to a falling edge because this is the transision from cn>2 to cn=2
								last_bp.stat=-1
							else:
								#### in the last breakpoint of the previous chromosome, there is a copy number less than 2
								#### which points to a rising edge because this is the transition from cn<2 to cn=2
								last_bp.stat=1
							### First, we save the last bp in the array with specified state, then
							### work on the current breakpoint

							#### Quantitative: This breakpoint is assessed based on the cn on the left side
							bp_array[last_chrom-1].append(last_bp)
						### Updating the last chromosome
						last_chrom=chrom
						### Set the state of the current breakpoint to unknown 
						tmp_stat=-2
						if copy_number>2:
							### when we do not have a previous breakpoint and we enter the first chromosome
							### having a breakpoint with cn>2 points to a rising edge
							tmp_stat=1
						else:
							### when we do not have a previous breakpoint and we enter the first chromosome
							### having a breakpoint with cn<2 points to a falling edge
							tmp_stat=-1
						### Updating the last breakpoint with the breakpoint at the end of the current segment 
						### the state of this breakpoint depends on the next segment so it will be temporarily set to -2 (unknowm)
						last_bp=bp(chrom,end,copy_number,-2)
						#### Saving the starting breakpoint of the current segment as the new breakpoint in the array of breakpoints 
						bp_array[chrom-1].append(bp(chrom,start,copy_number,tmp_stat))
					else:
						### We are in the same chromosome
						### Checking the last and the current breakpoints to see if they are consecutive or not
						if (last_bp.pos==(start-1) and file_type=="result") or (last_bp.pos==start and file_type=="ref"):
							if last_bp.cn>copy_number:
								#### in the same chromosome, the observed cn is less than the previous one
								#### which points to a falling edge
								last_bp.stat=-1
							else:
								#### in the same chromosome, the observed cn is greater than the previous one
								#### which points to a rising edge 
								last_bp.stat=1

							#### Save the observed breakpoint in the array of breakpoints 
							bp_array[chrom-1].append(last_bp)
							##### Quantitative: when facing two successive non-diploid, the end of the first segment
							##### and the start of the next segment are counted with their own absolute copynumbers
							#bp_array[chrom-1].append(bp(chrom,start,copy_number,last_bp.stat))
							### the last breakpoint is replaced by ending breakpoint of the current segment with unknown state
							last_bp=bp(chrom,end,copy_number,-2)
							### Updating the last chromosome
							last_chrom=chrom
							### NOTE: since the new segment starts at the ending point of the last segment, 
							### we count the current-starting and previous-ending breakpoints as one breakpoint
						### If the two breakpoints are not consecutive, there is a gap between them with cn=2
						else:
							### the last breakpoint (before the diploid gap) was greater than 2 which means 
							### a falling edge happened
							if last_bp.cn>2:
								last_bp.stat=-1
							else:
							### the last breakpoint before the diploid gap, was less than 2 which means 
							### a rising edge happended at that point
								last_bp.stat=1
							### saving the last breakpoint in the array of breakpoints
							### we are done with the last breakpoint
							bp_array[chrom-1].append(last_bp)

							tmp_stat=-2
							if copy_number>2:
								tmp_stat=1
							else:
								tmp_stat=-1
							### Saving the starting breakpoint of the current segment as a new breakpoint in the 
							### array of breakpoints
							bp_array[chrom-1].append(bp(chrom,start,copy_number,tmp_stat))
							### The ending breakpoint of the current segment will be the last_bp with unknown state
							last_bp=bp(chrom,end,copy_number,-2)
							### Updating the last chromosome
							last_chrom=chrom
				#### Working on the last breakpoint at the end of reading the file:
				#### The rest of the last chromosome must be diploid, so, cn>2 indicates to a falling edge
				if last_bp.cn>2:
					last_bp.stat=-1
				else:
				#### cn<2 points to a rising edge 
					last_bp.stat=1
				#### Save the ending breakpoint of the last segment into the array of breakpoints
				bp_array[last_chrom-1].append(last_bp)

	# return bp_array
	return 

def get_cn_accuracy(Thr,num_ploidy,data_path,exp,rep,gt_freq):
        data_path = "../data/" + exp + "/rep_" + str(rep)
        copynumber_path = data_path + "/copynumber/p"
        ### Path to the directory of ground truth files
        gs_path = data_path + "/gt/p"
        
        ##### Sort the ground truth file and save the sorted version in the working directory
        ploidies = [i+1 for i in range(num_ploidy)]
        threshold = 400000
        copynumber_precision = []
        copynumber_recall = []
        
        for pld in ploidies:
                cn_result = copynumber_path+str(pld)+"/copynumber.output.csv"
                cn_result_mod = copynumber_path+str(pld)+"/copynumber.output.mod.csv"
                gs_path_this = gs_path + str(pld)
                # modify the format of the copy number result
                cmd = "perl -ane 'next if($_ =~ /chrom/); @a = split(/,/, $_); print join(\"\\t\", $a[0], $a[2], $a[3]) . \"\\n\"'"+" "+cn_result+" "+">" + cn_result_mod
                os.system(cmd)
                # remove the overlapping breakpoints if frequency is < a number
                cmd = "env x=gt_freq perl -ane 'print join(\"\\t\", @F[0 .. 2]) . \"\\n\"' " + gs_path_this + "/gt.all.csv | sort | uniq -c | perl -ane 'print join(\"\\t\", @F[1 .. 3]) . \"\\n\" if($F[0] > $ENV{x})' > " + gs_path_this + "/gt.all.forCN.csv"
                os.system(cmd)
                sorting_cmd = "sortBed -i "+gs_path_this+"/gt.all.forCN.csv > "+gs_path_this+"/gt.all.forCN.sorted.csv"
                #os.system(sorting_cmd)
                cmd = "perl ../../general_scripts/comp_cn_gt.pl " + cn_result_mod + " " + gs_path_this + "/gt.all.forCN.sorted.csv " + str(threshold)
                out = os.popen(cmd).readlines()
        
                copynumber_recall.append(100*float(out[0].strip().split()[0]))
                copynumber_precision.append(100*float(out[0].strip().split()[1]))
        return copynumber_recall,copynumber_precision

def get_accuracy(Thr,num_ploidy,ginkgo_path,lst_path,gs_path,prefix,prefix_gt,gs_suffix,gs_suffix_sorted,ginkgo_suffix):
        ploidies = [i+1 for i in range(num_ploidy)]
        # alphas = [0.001,1e-05,1e-10,1e-100]
        TP = []
        tp = []
        Recall = []
        FP = []
        FN = []
        detected=[]
        total=[]
        precision = []
        total_Ginkgo=[0 for i in range(len(ploidies))]
        myDict = {}
        
        ### each row for each scale 
        for pldy in range(len(ploidies)):
        	FP.append([])
        	tp.append([])
        	TP.append([])
        	Recall.append([])
        	FN.append([])
        	total.append([])
        	precision.append([])
        for pldy in range(len(ploidies)):
        	lst = ginkgo_path+str(ploidies[pldy])+"/"+lst_path
        	with open(lst, "r") as f:
        		for line in f:
        			#### Collect the positive and negatives for each cell
        			diploid_flag = False
        			GS_array = []
        			Ginkgo_array=[]
        			for chr in range(24):
        				GS_array.append([])
        				Ginkgo_array.append([])
        
        			line = line.strip()
        			gs = gs_path+str(ploidies[pldy])+"/"+prefix_gt+line+gs_suffix
        			gs_sorted = gs_path+str(ploidies[pldy])+"/"+prefix_gt+line+gs_suffix_sorted
        			cmd = "sortBed -i "+gs+" > "+gs_sorted
        			#print "sorting "+gs+"..."
        			#os.system(cmd)
        			# GS_array[pldy] = Parse(GS_array[pldy],gs_sorted,file_type="ref")
        			Parse(GS_array,gs_sorted,file_type="ref")
        			### for each alpha/parameter
        			Ginkgo_file = ginkgo_path+str(ploidies[pldy]).replace(".","")+"/"+prefix+line+ginkgo_suffix
        			if os.stat(Ginkgo_file).st_size!=0:
        				# Ginkgo_arrays[pldy] = Parse(Ginkgo_arrays[pldy],Ginkgo_file,file_type="result")
        				Parse(Ginkgo_array,Ginkgo_file,file_type="result")
        			else:
        				print "uniform"
        				print line
        				diploid_flag=True
        			if diploid_flag:
        				continue
        			TP_ginkgo=0
        			FP_ginkgo=0
        			FN_ginkgo=0
        			detected_ginkgo=0
        			P = 0
        			for Chr in range(24):
        				#### if there is a copy number variation in any chromosome, count it as True
        				if len(GS_array[Chr])>0:
        					for Tbp in GS_array[Chr]:
        						P+=1
        			for Chr in range(24):
        				if len(GS_array[Chr])==0:
        					if len(Ginkgo_array[Chr])>0:
        						for Bp in Ginkgo_array[Chr]:
        							#### in the current cell and current paramter, there is a 
        							#### variation detected by Ginkgo which does not exist in the ground truth
        							#### Count it as False positive
        							FP_ginkgo+=1
        				if len(GS_array[Chr])>0:
        
        					if len(Ginkgo_array[Chr])>0:
        						#### iterating over the true variations in the current chromosome in the ground truth
        						for Tbp in GS_array[Chr]:
        							#### found_flag is True when we find a breakpoint in the result, within the threshold around the groundtruth 							#### breakpoint with the same status (i.e. they are both rising edge or falling edge). If there is no match for the ground truth breakpoint, this flag will remain False 
        							#### and the false positives or false negatives are added
        							found_flag=False
        							#### Compare each breakpoint in the results with the one in ground truth
        							for Bp in Ginkgo_array[Chr]:
        								if abs(Tbp.pos-Bp.pos)<Thr and Tbp.stat==Bp.stat:
        									if found_flag:
        										FP_ginkgo+=1
        									else:
        										TP_ginkgo+=1
        										found_flag=True
        									Bp.set_flag(1)
        								elif abs(Tbp.pos-Bp.pos)<Thr and Tbp.stat!=Bp.stat:
        									FP_ginkgo+=1
        									Bp.set_flag(1)
        							#### When found_flag is still False at this stage, it means that there is no breakpoint which 
        							#### agrees with the position and status of the ground truth breakpoint, so one false negative is added
        							if not found_flag:
        								FN_ginkgo+=1
        						for Bp in Ginkgo_array[Chr]:
        							if Bp.flag==0:
        								FP_ginkgo+=1
        
        
        					if len(Ginkgo_array[Chr])==0:
        						for Tbp in GS_array[Chr]:
        							FN_ginkgo+=1
        			total = FP_ginkgo+TP_ginkgo
        
        			#### check the total number of calls before saving into the global array
        			if total!=0:
        				tmp_ginkgo = (float(TP_ginkgo)/float(TP_ginkgo+FP_ginkgo))*100
        				precision[pldy].append(tmp_ginkgo)
        				tmp_ginkgo = (float(TP_ginkgo)/float(TP_ginkgo+FN_ginkgo))*100
        				Recall[pldy].append(tmp_ginkgo)
        			else:
        				total_Ginkgo[pldy]+=1
        return Recall, precision

### Path to the directory with subdirectories containing scaled results of HMMcopy
# hmm_path = "/Users/edrisi/Documents/CNV_dataset/Comparison/modal_200k/modal_"
### Path to the directory whose subdirectories contain the results of Ginkgo with different parameters
if(len(sys.argv) <= 1):
	print("""
	Compare ginkgo and hmmcopy results with ground truth (quantitative comparison) on different ploidies and draw the violin plot.
	Usage: python """ + sys.argv[0] + """ <experiment> <rep:1-3> <num_p> <copynumber_gt_freq>
	""")
	sys.exit(0)
exp = sys.argv[1]
rep = sys.argv[2]
data_path = "../data/" + exp + "/rep_" + str(rep)
### Path to the directory of ground truth files
gs_path = data_path + "/gt/p"
### Path to the list of filenames 
lst_path = "leaves.txt"

prefix="leaf"
prefix_gt = "gt"
# HMM_suffix=".inferred_hmm"
ginkgo_suffix = ".inferred.bed"
gs_suffix=".bed"
gs_suffix_sorted = ".gs.sorted.bed"

Thr = 400000
num_ploidy = int(sys.argv[3])
copynumber_gt_freq = int(sys.argv[4])

methods = ["Ginkgo", "HMMcopy", "CopyNumber"]
# claim a dataframe, whose columns are recall, precision, method, and fluc.
#df = pd.DataFrame(columns=["recall", "precision", "method", "fluc"])
df = pd.DataFrame(columns=["recall", "precision", "method", "fluc"])
for met in range(len(methods)):
        ginkgo_path = data_path + "/" + methods[met] + "/p"
        if met != 2:
                Recall, precision = get_accuracy(Thr,num_ploidy,ginkgo_path,lst_path,gs_path,prefix,prefix_gt,gs_suffix,gs_suffix_sorted,ginkgo_suffix)
                # check which cells have low recall and precision for hmmcopy
                if met == 1:
                    for i in range(len(Recall)):
                        for j in range(len(Recall[i])):
                            if Recall[i][j] < 10 and precision[i][j] < 10:
                                print i, j, Recall[i][j], precision[i][j]
        #print Recall
        #print precision
                for i in range(num_ploidy):
                        met_col = np.repeat(methods[met], len(Recall[i]))
                        fluc_col = np.repeat(i, len(Recall[i]))
                        rec_col = np.repeat("recall", len(Recall[i]))
                        prc_col = np.repeat("precision", len(Recall[i]))
                        df1 = pd.DataFrame({'value':Recall[i], 'RECvsPRC':rec_col, 'method':met_col, 'fluc':fluc_col})
                        #df1 = pd.DataFrame({'recall':Recall[i], 'precision':precision[i], 'method':met_col, 'fluc':fluc_col})
                        #df1 = pd.DataFrame({'recall':Recall[i], 'precision':precision[i], 'method':met_col, 'fluc':fluc_col})
                        df = pd.concat([df, df1])
                        df1 = pd.DataFrame({'value':precision[i], 'RECvsPRC':prc_col, 'method':met_col, 'fluc':fluc_col})
                        df = pd.concat([df, df1])
        else:
                Recall, precision = get_cn_accuracy(Thr,num_ploidy,data_path,exp,rep,copynumber_gt_freq)
                for i in range(num_ploidy):
                        #print Recall[i], precision[i]
                        r=3
                        d=1
                        met_col = np.repeat(methods[met], r)
                        fluc_col = np.repeat(i, r)
                        rec_col = np.repeat("recall",r)
                        prc_col = np.repeat("precision",r)
                        df1 = pd.DataFrame({'value':[Recall[i]-d, Recall[i], Recall[i]+d], 'RECvsPRC':rec_col, 'method':met_col, 'fluc':fluc_col})
                        #df1 = pd.DataFrame({'recall':Recall[i], 'precision':precision[i], 'method':met_col, 'fluc':fluc_col})
                        #df1 = pd.DataFrame({'recall':Recall[i], 'precision':precision[i], 'method':met_col, 'fluc':fluc_col})
                        df = pd.concat([df, df1])
                        df1 = pd.DataFrame({'value':[precision[i]-d, precision[i], precision[i]+d], 'RECvsPRC':prc_col, 'method':met_col, 'fluc':fluc_col})
                        df = pd.concat([df, df1])

# with the dataframe, now draw the violin 
rc={'font.size': 24, 'axes.labelsize': 16, 'legend.fontsize': 24.0,'axes.titlesize': 24, 'xtick.labelsize': 16, 'ytick.labelsize': 16}
sns.set(rc=rc)
sns.set(context="paper", palette="colorblind", style="ticks")
g = sns.FacetGrid(df, col="RECvsPRC", sharey=False, size=4, aspect=1)
g = g.map(sns.violinplot, "fluc", "value", "method", cut=0, scale="width", inner=None, split=False, palette="muted", saturation=1).despine(left=True)
# Set axis labels & ticks #
fontsize=12
fontsize1=14
fontsize2=16
g.fig.get_axes()[0].set_xticklabels(["MALBAC", "DOP-PCR", "TnBC", "Bulk"], size=fontsize)
g.fig.get_axes()[1].set_xticklabels(["MALBAC", "DOP-PCR", "TnBC", "Bulk"], size=fontsize)
g.fig.get_axes()[0].set_xlabel("")
g.fig.get_axes()[1].set_xlabel("")
g.fig.get_axes()[0].set_yticks(range(0, 120, 20))
g.fig.get_axes()[0].set_yticklabels(range(0, 120, 20), size=fontsize)
g.fig.get_axes()[0].set_ylabel("Recall", size=fontsize2)
g.fig.get_axes()[1].set_yticks(range(0, 120, 20))
g.fig.get_axes()[1].set_yticklabels(range(0, 120, 20), size=fontsize)
g.fig.get_axes()[1].set_ylabel("Precision", size=fontsize2)
g.fig.get_axes()[0].spines["left"].set_visible(True)
g.fig.get_axes()[1].spines["left"].set_visible(True)
# Set legend #
handles, labels = g.fig.get_axes()[0].get_legend_handles_labels()
g.fig.get_axes()[0].legend([handles[0], handles[1], handles[2]], ["Ginkgo", "HMMcopy", "CopyNumber"], loc='upper left', fontsize='large')
# Fixing titles #
g.fig.get_axes()[0].set_title("")
g.fig.get_axes()[1].set_title("")
#plt.show()
fig_file = "../figs/" + exp + "/combined_qual_rep" + str(rep) + ".png"
plt.tight_layout()
plt.savefig(fig_file, dpi=400)
#fig.savefig(fig_file, bbox_inches='tight', dpi=400)

#f, ax = plt.subplots(figsize=(8, 8))
#sns.violinplot(x="fluc", y="recall", hue="method", data=df, palette="muted")

#ax.set_xlabel("Fluctuation",size = 32)
#ax.set_ylabel("Recall (%)",size = 32)
#ax.set_ylim([0,100])
#plt.legend(loc='upper left')
#plt.show()

# df = pd.DataFrame({'Ploidy':[str(i) for i in ploidies],'Precision':precision,'Recall':Recall})
# df = df[['Ploidy','Precision','Recall']]
# dd = pd.melt(df, id_vars=['Ploidy'], value_vars=['Precision','Recall'])
# sns.boxplot(data=dd)
# plt.savefig("ginkgo_bp.png")
#data_to_plot_precision = [precision[i] for i in range(len(ploidies))]
#data_to_plot_recall = [Recall[i] for i in range(len(ploidies))]
#fig, (ax1,ax2) = plt.subplots(nrows=1,ncols=2, figsize=(9,6))
## bp_p = ax1.boxplot(data_to_plot_precision,patch_artist=True, boxprops=dict(facecolor="C0"))
## bp_r = ax2.boxplot(data_to_plot_recall,patch_artist=True, boxprops=dict(facecolor="C2"))
#viline_p = ax1.violinplot(data_to_plot_precision,showmeans=True, showmedians=True,
#        showextrema=True)
#ax1.set_ylim([0,100])
#labels = ['MALBAC', 'DOP-PCR', 'TnBC', 'Bulk']
#ax1.get_xaxis().set_tick_params(direction='out')
#ax1.xaxis.set_ticks_position('bottom')
#ax1.set_xticks(np.arange(1, len(labels) + 1))
#ax1.set_xticklabels(labels)
#ax1.set_xlim(0.25, len(labels) + 0.75)
#ax1.set_xlabel('Coverage Fluctuation')
#ax1.set_ylabel('Precision (%)')
#viline_r = ax2.violinplot(data_to_plot_recall,showmeans=True, showmedians=True,
#        showextrema=True)
#ax2.set_ylim([0,100])
#ax2.get_xaxis().set_tick_params(direction='out')
#ax2.xaxis.set_ticks_position('bottom')
#ax2.set_xticks(np.arange(1, len(labels) + 1))
#ax2.set_xticklabels(labels)
#ax2.set_xlim(0.25, len(labels) + 0.75)
#ax2.set_xlabel('Coverage Fluctuation')
#ax2.set_ylabel('Recall (%)')
#viline_p['cmeans'].set_color('black')
#viline_p['cmedians'].set_color('black')
#viline_p['cmins'].set_color('black')
#viline_p['cmaxes'].set_color('black')
#viline_p['cbars'].set_color('black')
#
#viline_r['cmeans'].set_color('black')
#viline_r['cmedians'].set_color('black')
#viline_r['cmins'].set_color('black')
#viline_r['cmaxes'].set_color('black')
#viline_r['cbars'].set_color('black')
#for pc in viline_p['bodies']:
#    pc.set_facecolor('chocolate')
#    pc.set_edgecolor('black')
#    pc.set_alpha(0.7)
#for pc in viline_r['bodies']:
#    pc.set_facecolor('blueviolet')
#    pc.set_edgecolor('black')
#    pc.set_alpha(0.6)
## set_box_color(bp_p, '#D7191C') # colors are from http://colorbrewer2.org/
## set_box_color(bp_r, '#2C7BB6')
#ax1.set_xlabel('Ploidy')
#ax1.set_ylabel('Precision (%)')
#ax2.set_xlabel('Ploidy')
#ax2.set_ylabel('Recall (%)')
# ax1.legend(bp_p["boxes"][0], 'Precision', loc='upper right')
# ax2.legend(bp_r["boxes"][0], 'Recall', loc='upper right')
# plt.plot([], c='#D7191C', label='Precision(%)')
# plt.plot([], c='#2C7BB6', label='Recall(%)')
# fig.legend()
#plt.tight_layout()

#fig_file = "../figs/" + exp + "/ginkgo_quan_rep" + str(rep) + ".png"
#fig.savefig(fig_file, bbox_inches='tight', dpi=400)

#fig2, ax = plt.subplots()
#for pldy in range(len(ploidies)):
#	ax.scatter(precision[pldy],Recall[pldy],s=3 ,marker='o',label='ploidy: '+str(ploidies[pldy]));
#ax.set_title('precision vs recall', fontname="Arial", fontsize=18)
#ax.set_xlabel('precision (%)', fontname="Arial", fontsize=16)
#ax.set_ylabel('recall (%)', fontname="Arial", fontsize=16)
#plt.legend(numpoints=1,fontsize = 'x-small')
## plt.xlim(0,1.8);
#plt.savefig('./ploidy_figs/ginkgo_varying_ploidies_quantitative.png', dpi=1200)























