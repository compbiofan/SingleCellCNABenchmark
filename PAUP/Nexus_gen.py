import numpy as np
import os 
import sys
from os import walk 


class UnAcceptedCSVLine(Exception):
	def __init__(self, data):
		self.data = data
	def __str__(self):
		return repr(self.data)

def checkEqualto2(arr):
	# return list(set(arr))==["2"] 
	return len(set(arr))<=1

def Nexus_state(the_string):
	#### The input must be an integer 
	#### The output is the character suitable for PAUP
	cut = 15
	alphabets = ["0","1","2","3","4","5","6","7","8","9","A","B","C","D","E","F"]
	state = None
	if int(the_string)<=cut-1:
		state = alphabets[int(the_string)]
	else:
		state = alphabets[-1]
	return state
def stateExtract(label):
	stateString = ""
	for i in label:
		if i.isdigit():
			stateString += i
	return int(stateString)

def to_Nexus(bin_array, samples, output_address):
	output_f = open(output_address,"w")
	output_f.write("#NEXUS"+'\n')
	output_f.write("begin taxa;"+"\n"+"\t")
	#### Add one to the number of samples to account for the normal/diploid cell 
	output_f.write("dimensions ntax="+str(len(samples)+1)+";"+"\n"+"\t")
	output_f.write("\t"+"taxlabels"+"\n")
	for cell in samples:
		output_f.write(cell+"\n")
	##### Add one more taxon as the diploid/normal cell 
	output_f.write("diploid"+"\n")
	output_f.write(";"+"\n"+"end"+";"+"\n")
	output_f.write("begin characters;"+"\n"+"\t"+"dimensions nchar="+str(bin_array.shape[1])+";"+"\n"+"\t")
	output_f.write("format datatype=standard symbols=\"0~9 A~F\";"+"\n"+"\t")
	output_f.write("matrix"+"\n")
	for i in range(bin_array.shape[0]):
		output_f.write(samples[i]+"\t")
		for j in range(bin_array.shape[1]):
			output_f.write(str(bin_array[i][j]))
		output_f.write('\n')
	##### Add the diploid cell to the matrix with all the bins' states equal to 2
	##### Specify the number of best trees 
	nbest = 10
	swapping = "TBR"
	treelist = [i+1 for i in range(nbest)]
	output_f.write("diploid"+"\t")
	for j in range(bin_array.shape[1]):
		output_f.write(str(2))
	output_f.write('\n')
	output_f.write(";"+"\n"+"end;"+"\n")
	output_f.write("begin paup;"+"\n")
	output_f.write("\t"+"outgroup diploid;"+"\n")
	output_f.write("\t"+"set criterion=parsimony;"+"\n")
	output_f.write("\t"+"Hsearch nbest="+str(nbest)+";"+"\n")
	output_f.write("\t"+"Hsearch swap="+swapping+";"+"\n")
	output_f.write("\t"+"RootTrees;"+"\n")
	output_f.write("\t"+"DescribeTrees /xout=Both plot=none brLens=yes;"+"\n")
	output_f.write("\t"+"log start file=logfile.log;"+"\n")
	output_f.write("\t"+"DescribeTrees "+' '.join(map(str,treelist))+" /root=outgroup;"+"\n")
	output_f.write("\t"+"log stop;"+"\n")
	output_f.write("end;")
	output_f.close()
	return 

def Parse_Ginkgo(address):
	sample_names = None
	bin_arr = []
	with open(address,"r") as f:
		for line in f:
			line = line.strip()
			if "CHR" in line:
				raw_names = line.split()[3:]
				sample_names = [name.split('.')[-3] for name in raw_names]
			else:
				raw_states = line.split()[3:]
				if checkEqualto2(raw_states):
					print(line)
				else:
					# print len(set(raw_states))
					##### any state greater than or equal to 15 will be named as "F"
					##### states from 10 to 14 are named as "A" to "E"
					bin_arr.append([Nexus_state(state) for state in raw_states])
	bin_arr = np.array(bin_arr)
	return (bin_arr.T,sample_names)

def Parse_HMMcopy(address):
	return Parse_Ginkgo(address)

def main():

	infile = sys.argv[1]
	outfile = sys.argv[2]
	(bin_array,samples) = Parse_Ginkgo(address=infile)
	to_Nexus(bin_array=bin_array,samples=samples,output_address=outfile)
	print(bin_array.shape)

if __name__ == "__main__":
	main()
