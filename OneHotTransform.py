import sys
import re
import numpy as np

fileName = sys.argv[1]
numSample = int(sys.argv[2])
BASE_FILE_DIR = "./"
readObj = open(BASE_FILE_DIR+"/"+fileName+".fa")



def baseToOnehot(base):
	if base == 'A':
		return np.array([1, 0, 0, 0])
	elif base == 'G':
		return np.array([0, 1, 0, 0])
	elif base == 'C':
		return np.array([0, 0, 1, 0])
	elif base == 'T':
		return np.array([0, 0, 0, 1])
	else:
		return np.array([0, 0, 0, 0])


all_samples = np.zeros((numSample,1000,4))
current_sample = np.zeros((1000,4))
sample_count = 0
new_seq_flag = False
for line in readObj:
	line = line.strip('\r\n')
	if re.search(ur'>',line):
		sample_count += 1
		if sample_count % 1000 == 0:
			print sample_count
	else:
		line = line.upper()
		first_base = True
		base_count = 0
		for base in line:
			if first_base == True:
				first_base = False
				current_sample = np.zeros((1000,4))
				current_sample[base_count] = baseToOnehot(base)
				base_count += 1
			else:							
				current_sample[base_count] = baseToOnehot(base)
				base_count += 1
		all_samples[sample_count-1] = current_sample

all_samples = np.rollaxis(all_samples,2,1)
np.save(BASE_FILE_DIR+"/"+fileName+".npy", all_samples)
print fileName + " Done."
