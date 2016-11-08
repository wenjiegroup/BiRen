import numpy as np 
import sys

fileName = sys.argv[1]

BASE_DIR = "."

readObj = open(BASE_DIR+"/"+fileName+".bed")

sampleMaps = []

for line in readObj:
	line = line.strip('\r\n')
	temps = line.split('\t')
	element_chr = temps[0]
	element_start = int(temps[1])
	element_end = int(temps[2])
	start = element_start
	end = element_start + 200
	while end < element_end:
		dataMap = {}
		dataMap['chr'] = element_chr
		dataMap['start'] = start - 400
		dataMap['end'] = end + 400
		start += 200
		end += 200
		sampleMaps.append(dataMap)


outObj_sample = open(BASE_DIR+"/"+fileName+"_1k.bed", 'w')



for currMap in sampleMaps:
	outObj_sample.write(currMap['chr']+"\t"+str(currMap['start'])+"\t"+str(currMap['end'])+"\n")

outObj_sample.close()

