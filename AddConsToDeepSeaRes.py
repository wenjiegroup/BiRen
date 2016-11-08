import numpy as np
import sys

fileName = sys.argv[1]

Sample_data = np.load("./"+fileName+"_1k_deepsea.npy")

num_Sample = Sample_data.shape[0]
newPosData = np.zeros((num_Sample,920))
SampleConsReadObj = open("./"+fileName+".cons")


count = 0
for line in SampleConsReadObj:
	line = line.strip('\r\n')
	conScore = float(line)
	newPosData[count][0:919] = Sample_data[count]
	newPosData[count][919] = conScore
	count += 1	

np.save("./"+fileName+"_deepsea_cons.npy",newPosData)

