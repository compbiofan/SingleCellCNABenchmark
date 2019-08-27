#!/usr/bin/python
import os
from os import walk 
import numpy as np 
import matplotlib as mpl  
import sys
import csv
import collections

class UnAcceptedCSVLine(Exception):
	def __init__(self, data):
		self.data = data
	def __str__(self):
		return repr(self.data)

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

## Path to the directory containing the .csv files 
if(len(sys.argv) <= 1):
	print("""
        Prepare the input file for CopyNumber given the csv file from HMMcopy initialization step. 
        Usage: python """ + sys.argv[0] + """ <folder_csv>
        """)
	sys.exit(0)
rootdir = sys.argv[1]
csv_dict = {}
sample_ids = []
currentChr = -1
line_count = 0
first_csv_read = False
list_f = open(rootdir+"/leaves.txt","w")
sorted_samples = []
## Specify the name of the output
copynumber_csv_input = open(rootdir+"/copynumber.input.csv","w")


try:
	for subdir, dirs, files in os.walk(rootdir):
		for file in files:
			filepath = subdir + os.sep + file
			if filepath.endswith("wig.csv") and "leaf" in filepath:
				#Optional: extract the cell id from the file name
				cell_id = file.strip().split('.')[0].replace("leaf","")
				# Save the cell id in a list 
				sample_ids.append(cell_id)
				print "processing cell "+filepath+"..."
				sorted_samples.append(int(cell_id))
				with open(filepath,"r") as csv_file:
					csv_reader = csv.reader(csv_file, delimiter=',')
					line_count = 0
					for row in csv_reader:
					
						if line_count!=0:
							#### reading the chr, position, and the normalized read count of each bin 
							if chr_extract(row[0]) != currentChr:	
								currentChr = chr_extract(row[0])
							line_count+=1
							if not first_csv_read:

								### The key is the pair of (chromosome, start position) for each bin across all cells
								### Since Copynumber works with probe's position, we can pick either start or end position of a bin 
								### Every new key is accepted when reading the first csv file
								csv_dict[(currentChr,int(row[1]))]=[int(row[6])]
							else:
								### We assume all the sets of bins are the same for all the cells
								### when the first csv has been read, any new pair of (chr, pos) raises an exception 
								if (currentChr,int(row[1])) not in csv_dict:
									raise UnAcceptedCSVLine("An extra bin has been observed. Please ensure that the binning is the same across all the cells")
								else:
									csv_dict[(currentChr,int(row[1]))].append(int(row[6]))
								
						else:
							#### reading the labels in the first row of each csv 
							line_count+=1
				first_csv_read=True

except UnAcceptedCSVLine as e:
	print ("Received Error:", e.data)
#### All the csv files have been read, write the output for copynumber
#### Write the labels
copynumber_csv_input.write("Chrom,Median.bp,")
for i in range(len(sample_ids)):
	if i==len(sample_ids)-1:
		copynumber_csv_input.write(sample_ids[i]+"\n")
	else:
		copynumber_csv_input.write(sample_ids[i]+",")

### Sort the dictionary of (chr,pos) pairs by the chromosome and the positions
ordereddict = collections.OrderedDict(sorted(csv_dict.items()))
for item in ordereddict:
	copynumber_csv_input.write(str(item[0])+","+str(item[1])+",")
	for i in range(len(ordereddict[item])):
		if i==len(ordereddict[item])-1:
			copynumber_csv_input.write(str(ordereddict[item][i])+"\n")
		else:
			copynumber_csv_input.write(str(ordereddict[item][i])+",")
copynumber_csv_input.close()
sorted_samples = sorted(sorted_samples)
for i in range(len(sorted_samples)):
    list_f.write(str(sorted_samples[i])+"\n")
list_f.close()
			
						
