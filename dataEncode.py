import numpy as np 
import os
import sys
import commands

fileName = sys.argv[1]
genome = sys.argv[2]
evolutionaryConservation = sys.argv[3]

# Check argv length
if len(sys.argv) != 4:
	print "Miss required parameter"
	print "Usage :"
	print "	python example genome.fa EvolutionaryConservation.bw"
	os._exit(0)
else:
	pass

# Check files exists
if os.path.exists("./"+fileName+".bed") and os.path.exists("./"+genome) and os.path.exists("./"+evolutionaryConservation):
	pass
else:
	print "Usage :"
	print "	python example genome.fa EvolutionaryConservation.bw"
	os._exit(0)

# Check example.bed legality
# Each region should be larger than 200bp but not beyond 8000bp
checkObj = open("./"+fileName+".bed")
for line in checkObj:
	line = line.strip("\r\n")
	temps = line.split("\t")
	start = int(temps[1])
	end = int(temps[2])
	length = end - start
	if length < 200 and length <= 8000:
		print "Line : "
		print "	"+line
		print "Each region should be larger than 200bp but not beyond 8000bp."
		os._exit(0)
checkObj.close()

# Build folder
outdir = "./"+fileName
if os.path.exists(outdir):
	pass
else:
	os.mkdir(outdir)


# Build 1k format bed
os.system("python transformTo1Kformat.py "+fileName)
print "Build 1k format bed Done."

# getfasta
os.system("bedtools getfasta -fi ./"+genome+" -bed "+fileName+"_1k.bed -fo "+fileName+"_1k.fa")
print fileName+" getfasta Done."

# One-hot transform
numSample = commands.getstatusoutput("wc -l "+fileName+"_1k.bed")[1].split(" ")[0]
os.system("python OneHotTransform.py "+fileName+"_1k "+numSample)
print "One-hot transform Done."

# DeepSEA Encode
os.system("luajit DeepSEA.lua --dataset "+fileName+"_1k")
print "DeepSEA encode Done."


# Add EvolutionaryConservation Score
os.system("python ExtractCoreRegion.py "+fileName)
os.system("bigWigAverageOverBed "+evolutionaryConservation+" "+fileName+"_200.bed "+fileName+".tab -bedOut="+fileName+".cons.bed")
numSample = commands.getstatusoutput("wc -l "+fileName+".cons.bed")[1].split(" ")[0]
os.system("python SortConsBed.py "+fileName+" "+numSample)
os.system("python AddConsToDeepSeaRes.py "+fileName)
os.system("python RNNDataFormat.py "+fileName)
os.system("rm "+fileName+".cons")
os.system("rm "+fileName+".cons.bed")
os.system("rm "+fileName+".tab")
os.system("rm "+fileName+"_1k.bed")
os.system("rm "+fileName+"_1k.fa")
os.system("rm "+fileName+"_1k.npy")
os.system("rm "+fileName+"_1k_deepsea.npy")
os.system("rm "+fileName+"_200.bed")
os.system("rm "+fileName+"_deepsea_cons.npy")
print "Add EvolutionaryConservation Score and RNN data format Done."
print "..."
print "Data Encode Done."