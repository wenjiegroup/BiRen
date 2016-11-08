import sys

fileName = sys.argv[1]

SampleReader = open("./"+fileName+"_1k.bed")
SampleWriter = open("./"+fileName+"_200.bed",'w')

count = 1
for line in SampleReader:
	line = line.strip('\r\n')
	temps = line.split('\t')
	chromosome = temps[0]
	start = int(temps[1])
	end = int(temps[2])
	SampleWriter.write(chromosome+'\t'+str(start+400)+'\t'+str(end-400)+'\t'+str(count)+'\n')
	count += 1
SampleReader.close()
SampleWriter.close()
