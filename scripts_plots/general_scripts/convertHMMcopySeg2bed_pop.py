import os
from os import walk 
import numpy as np 
import sys
#import argparse

class cn():

	def __init__(self, cn, chr, s, e):
		self.cn = cn 
		self.chr = chr 
		self.s = s
		self.e = e


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


#path="./"

if len(sys.argv) <= 1:
        print("""
        Given a path of the hmmcopy csv files, convert them to bed files and save in the same folder with suffix hmminferred.bed.
        Usage: python convertHMMcopySeg2bed_pop.py <hmmcopy_folder>
        """)
        sys.exit(0)

path=sys.argv[1]

sorted_samples = []
list_f = open(path+"/leaves.txt","w")
for root, directories, filenames in os.walk(path):
        print root
	for filename in filenames:
		#### Extract the name of the sample
		if "csv" in filename:
			
			file_path = os.path.join(root, filename)
			cell_id = filename.strip().split('.')[0]
			sorted_samples.append(int(cell_id.replace("leaf","")))
			print cell_id
			cn_array = []
			for i in range(24):
				cn_array.append([])
			### for each line create an instance of the cn class 
			with open(file_path, "r") as f:
				next(f)
				for line in f:
					split_line = line.strip().split(',')
					if "e" in split_line[1]:
						split_line[1] = str(int(float(split_line[1])))
					if "e" in split_line[2]:
						split_line[2] = str(int(float(split_line[2])))
					
					cn_array[chr_extract(split_line[0])-1].append(cn(split_line[3],split_line[0],split_line[1], split_line[2]))
					#cn_array[split_line[0]-1].append(cn(split_line[3],split_line[0],split_line[1], split_line[2]))
			#### now, write the information into the inferred.bed file 
			sample_f = os.path.join(root,cell_id+".inferred.bed")
			print sample_f
			file = open(sample_f, "w")
			for Chr in range(len(cn_array)):
				for seg in range(len(cn_array[Chr])):
					if cn_array[Chr][seg].cn!="2":
							str_ = ""
							str_ = str("\t".join([cn_array[Chr][seg].chr+"\t"+ cn_array[Chr][seg].s+"\t"+ cn_array[Chr][seg].e+"\t"+cn_array[Chr][seg].cn]))+"\n"
							file.write(str_)

			file.close()
sorted_samples = sorted(sorted_samples)
for i in range(len(sorted_samples)):
	list_f.write(str(sorted_samples[i])+"\n")
list_f.close()


