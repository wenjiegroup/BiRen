==============================================================
DEPENDENCIES:

OS: Linux


1. Installing torch and basic package dependencies following instructions from 
http://torch.ch/docs/getting-started.html
You may need to install cmake if you do not have it already. It is highly recommended to link against OpenBLAS or other optimized BLAS library when building torch.


2. npy4th
	A package to load/save numpy files for troch7
	Requirements:
		torch7
		xlua
	Installation:
		git clone https://github.com/htwaijry/npy4th.git
		cd npy4th
		luarocks make


3. Python 2.7.x, numpy, pandas, scipy, scikit-learn


4. Installing Theano and basic package dependencies following instructions from http://deeplearning.net/software/theano/install.html


5. Installing Lasagne and basic package dependencies following instructions from https://github.com/Lasagne/Lasagne or http://lasagne.readthedocs.org/en/latest/user/installation.html


6. bedtools (>= 2.25.0)
	make sure the bedtools has already exported to PATH

7. bigWigAverageOverBed



===============================================================
USAGE:

STEP 1: Data preprocessing

Example run:

	python dataEncode.py example genome.fa EvolutionaryConservation.bw


step1 must contain the following files:

	dataEncode.py
	transformTo1Kformat.py
	genome.fa
	OneHotTransform.py
	DeepSEA.lua
	deepsea.cpu
	ExtractCoreRegion.py
	bigWigAverageOverBed
	EvolutionaryConservation.bw
	SortConsBed.py
	AddConsToDeepSeaRes.py
	RNNDataFormat.py


In this step, the predict target should be .BED format (example.bed), each region should be large than 200bp.

genome.fa is the Human(hg19) whole genome seuqnece which can be obtained from UCSC Genome Browser,please merge all chromosome and rename "genome.fa",or you can download from:

	ftp://123.56.134.57/data/genome.fa

EvolutionaryConservation.bw was taken from the vertebrate phastCons44way track from USCS Genome Browser, or you can download from: 

	ftp://123.56.134.57/data/EvolutionaryConservation.bw

deepsea.cpu is DeepSEA trained model, you can download from:

	ftp://123.56.134.57/data/deepsea.cpu


output files will be under "example" folder:

	example_data.npy
	example_mask.npy  


STEP 2: Prediction procedure

step2 must contain the following files:
	
	BiRen.py
	BiRen_trained_model.npy

Example run:

	python BiRen.py example

output files will be under ./example :
	example.out

Here is a minnimal example:

	chr20	2719208	2719789	0.220106445764

	chr5	2112055	2113430	0.859481014407

The four columns are chromosome, start position, end position and enhancer probabiliy score.



