import numpy as np 
import comparison_module
from comparison_module import *
import sys
import os
from os import walk
from matplotlib import pyplot as plt 

prefix="SRR"
HMM_suffix = ".inferred_hmm.bed"
Ginkgo_suffix=".inferred.bed"
CN_r_name = "cn_file"

Thr = int(sys.argv[1])
HMM_path = sys.argv[2]
Ginkgo_path = sys.argv[3]
CN_path = sys.argv[4]
sample_name = None
if Ginkgo_path.endswith('/'):
	lst_path = Ginkgo_path+"leaves.txt"
	sample_name = Ginkgo_path.split("/")[-2]
else:
	lst_path = Ginkgo_path+"/leaves.txt"
	sample_name = Ginkgo_path.split("/")[-1]

Ginkgo_bps = [[] for i in range(24)]
HMMcopy_bps = [[] for i in range(24)]
Copynumber_bps = None
CN_file = CN_path+CN_r_name

diploid_counter = 0
cell_counter = 0
###### Collect all the breakpoints of CopyNumber on one array
Copynumber_bps = [[] for i in range(24)]
Copynumber_bps = Parse_copynumber(Copynumber_bps,CN_file)
##### Collect the breakpoints of Ginkgo and HMMcopy in separate lists/sets 
##### Here the directions of the breakpoints do not matter
##### Only the chromosome and the position is considered 
with open(lst_path,"r") as f:
	for line in f:
		cell_counter+=1
		tmp_arr_hmm = [[] for i in range(24)]
		tmp_arr_ginkgo = [[] for i in range(24)]
		line = line.strip()
		HMM_file = HMM_path+prefix+line+HMM_suffix
		Gingko_file = Ginkgo_path+prefix+line+Ginkgo_suffix
		####### This line would be different when we one wants to remove the cells reported as diploid by HMMcopy
		if os.stat(Gingko_file).st_size!=0 and os.stat(HMM_file).st_size!=0:
			tmp_arr_hmm = comparison_module.Parse(bp_array=tmp_arr_hmm,address=HMM_file,file_type="result",analysis_type="qual")
			tmp_arr_ginkgo = comparison_module.Parse(bp_array=tmp_arr_ginkgo,address=Gingko_file,file_type="result",analysis_type="qual")
			tmp_arr_hmm = np.array(tmp_arr_hmm)
			tmp_arr_ginkgo = np.array(tmp_arr_ginkgo)
			for Chr in range(24):
				if len(HMMcopy_bps[Chr])>0:
					for tmp_bp in tmp_arr_hmm[Chr]:
						flag = False
						for hmm_bp in HMMcopy_bps[Chr]:
							if hmm_bp.chr==tmp_bp.chr and hmm_bp.pos==tmp_bp.pos:
								flag = True
								break
						if flag:
							continue
						else:
							HMMcopy_bps[Chr].append(tmp_bp)
				else:
					HMMcopy_bps[Chr]= tmp_arr_hmm[Chr]
				if len(Ginkgo_bps[Chr])>0:
					for tmp_bp in tmp_arr_ginkgo[Chr]:
						flag = False
						for ginkgo_bp in Ginkgo_bps[Chr]:
							if ginkgo_bp.chr==tmp_bp.chr and ginkgo_bp.pos==tmp_bp.pos:
								flag=True
								break
						if flag:
							continue
						else:
							Ginkgo_bps[Chr].append(tmp_bp)
				else:
					Ginkgo_bps[Chr] = tmp_arr_ginkgo[Chr]
			if os.stat(HMM_file).st_size==0:
				print len(tmp_arr_hmm[0])
		if os.stat(HMM_file).st_size==0:
			diploid_counter+=1
values = comparison_module.compare3(HMMcopy_bps,Ginkgo_bps,Copynumber_bps,Thr)
print sample_name+","+str(values)[1:-1]



