import sys
import numpy as np 

fileName = sys.argv[1]
numSample = int(sys.argv[2])

SampleMap = {}
SampleReadObj = open("./"+fileName+".cons.bed")
for line in SampleReadObj:
	line = line.strip('\r\n')
	temps = line.split('\t')
	elemId = int(temps[3])
	conScore = float(temps[4])
	SampleMap[elemId] = conScore
outObj = open("./"+fileName+".cons",'w')
for i in range(numSample):
	count = i + 1
	outObj.write(str(SampleMap[count])+"\n")


