import numpy as np
import sys

fileName = sys.argv[1]

BASE_DIR = "."

SampleBedObj = open(BASE_DIR+"/"+fileName+".bed")

SampleArr = []



SamplePredict = np.load(BASE_DIR+"/"+fileName+"_deepsea_cons.npy")

for line in SampleBedObj:
	count = 0
	line = line.strip('\r\n')
	temps = line.split('\t')
	element_chr = temps[0]
	element_start = int(temps[1])
	element_end = int(temps[2])
	start_Sample = element_start
	end_Sample = element_start + 200
	while end_Sample < element_end:
		count += 1
		end_Sample += 200
	SampleArr.append(count)



SampleCount = len(SampleArr)

maxLen = 40


SampleDataArr = []
SampleMaskArr = []


start_idx = 0
for i in range(SampleCount):
	data = SamplePredict[start_idx:start_idx+SampleArr[i]]
	SampleDataArr.append(data)
	start_idx = start_idx + SampleArr[i]
	mask = [0] * maxLen
	for j in range(SampleArr[i]):
		mask[j] = 1
	SampleMaskArr.append(mask)


data_x = np.zeros((SampleCount, maxLen, 920))
data_mask = np.zeros((SampleCount, 40))
for i in range(len(SampleArr)):
	x = SampleDataArr[i]
	xnpy = np.zeros((40, 920))
	len_x = x.shape[0]
	xnpy[0:len_x] = x 
	data_x[i] = xnpy
	data_mask[i] = SampleMaskArr[i]

np.save(BASE_DIR + "/" + fileName + "/" + fileName + ".data.npy",data_x)
np.save(BASE_DIR + "/" + fileName + "/" + fileName + ".mask.npy",data_mask)


