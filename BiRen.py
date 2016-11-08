import numpy as np 

import theano
import theano.tensor as T 
import lasagne
from sklearn import metrics

import os
import sys
import time


def iterate_read_batch_index(inputs, batchsize):
	indexArr = []
	num_samples = inputs.shape[0]
	index_start = 0
	index_end = 0
	while index_start < num_samples:
		index_end = index_start + batchsize
		if index_end < num_samples:
			indexArr.append((index_start,index_end))
		else:
			indexArr.append((index_start,num_samples))
			break
		index_start += batchsize
	return indexArr


fileName = sys.argv[1]

PARAM_DATA_DIR = "./"+fileName
PARAM_OUTPUT_DIR = "./"+fileName


DIM_INPUT = 920

READ_BATCH = 100

# Workspace
DATA_DIR = PARAM_DATA_DIR
OUTPUT_DIR = PARAM_OUTPUT_DIR
teX = np.load(DATA_DIR+"/"+fileName+".data.npy")
teM = np.load(DATA_DIR+"/"+fileName+".mask.npy")

print "Data Load."


n_te_sample = teX.shape[0]
MAX_LENGTH = teX.shape[1]

PARAM_TRAINED_MODEL = "./BiRen_trained_model.npy"
# Reload trained model parameters
TRAINED_MODEL = np.load(PARAM_TRAINED_MODEL)

#######
load_W_in_to_updategate_1 = TRAINED_MODEL[0]
load_W_hid_to_updategate_1 = TRAINED_MODEL[1]
load_b_updategate_1 = TRAINED_MODEL[2]
load_W_in_to_resetgate_1 = TRAINED_MODEL[3]
load_W_hid_to_resetgate_1 = TRAINED_MODEL[4]
load_b_resetgate_1 = TRAINED_MODEL[5]
load_W_in_to_hidden_update_1 = TRAINED_MODEL[6]
load_W_hid_to_hidden_update_1 = TRAINED_MODEL[7]
load_b_update_1 = TRAINED_MODEL[8]
load_hid_init_1 = TRAINED_MODEL[9]

load_W_in_to_updategate_2 = TRAINED_MODEL[10]
load_W_hid_to_updategate_2 = TRAINED_MODEL[11]
load_b_updategate_2 = TRAINED_MODEL[12]
load_W_in_to_resetgate_2 = TRAINED_MODEL[13]
load_W_hid_to_resetgate_2 = TRAINED_MODEL[14]
load_b_resetgate_2 = TRAINED_MODEL[15]
load_W_in_to_hidden_update_2 = TRAINED_MODEL[16]
load_W_hid_to_hidden_update_2 = TRAINED_MODEL[17]
load_b_update_2 = TRAINED_MODEL[18]
load_hid_init_2 = TRAINED_MODEL[19]

load_dense_W = TRAINED_MODEL[20]
load_dense_b = TRAINED_MODEL[21]
#######

N_HIDDEN = load_W_in_to_updategate_1.get_value().shape[1]


# Recurrent layers expect input of shape
# (batch size, max sequence length, number of features)
l_in = lasagne.layers.InputLayer(shape=(None, MAX_LENGTH, DIM_INPUT))

l_mask = lasagne.layers.InputLayer(shape=(None, MAX_LENGTH))

h1_forward = lasagne.layers.GRULayer(
	l_in, N_HIDDEN, mask_input=l_mask,
	only_return_final=True)

h1_forward.W_in_to_updategate = load_W_in_to_updategate_1
h1_forward.W_hid_to_updategate = load_W_hid_to_updategate_1
h1_forward.b_update = load_b_update_1
h1_forward.W_in_to_resetgate = load_W_in_to_resetgate_1
h1_forward.W_hid_to_resetgate = load_W_hid_to_resetgate_1
h1_forward.b_resetgate = load_b_resetgate_1
h1_forward.W_in_to_hidden_update = load_W_in_to_hidden_update_1
h1_forward.W_hid_to_hidden_update = load_W_hid_to_hidden_update_1
h1_forward.b_update = load_b_update_1
h1_forward.hid_init = load_hid_init_1


h1_backward = lasagne.layers.GRULayer(
	l_in, N_HIDDEN, mask_input=l_mask,
	only_return_final=True,
	backwards=True)

h1_backward.W_in_to_updategate = load_W_in_to_updategate_2
h1_backward.W_hid_to_updategate = load_W_hid_to_updategate_2
h1_backward.b_update = load_b_update_2
h1_backward.W_in_to_resetgate = load_W_in_to_resetgate_2
h1_backward.W_hid_to_resetgate = load_W_hid_to_resetgate_2
h1_backward.b_resetgate = load_b_resetgate_2
h1_backward.W_in_to_hidden_update = load_W_in_to_hidden_update_2
h1_backward.W_hid_to_hidden_update = load_W_hid_to_hidden_update_2
h1_backward.b_update = load_b_update_2
h1_backward.hid_init = load_hid_init_2


l_concat = lasagne.layers.ConcatLayer([h1_forward, h1_backward])


l_out = lasagne.layers.DenseLayer(
	l_concat, num_units=1, W=load_dense_W, b=load_dense_b, nonlinearity=lasagne.nonlinearities.sigmoid)
target_values = T.matrix('target_output')
network_output = lasagne.layers.get_output(l_out)
cost = lasagne.objectives.binary_crossentropy(network_output, target_values)
cost = cost.mean()

predict_fn = theano.function([l_in.input_var, l_mask.input_var], network_output)


### Do Predict Results  ###
# TestSet Predict
test_predict_result = np.zeros((n_te_sample,1))
batchIndexArr = iterate_read_batch_index(teX, READ_BATCH)
for (start, end) in batchIndexArr:
	batch_x = teX[start:end]
	batch_m = teM[start:end]
	batch_res = predict_fn(batch_x,batch_m)
	test_predict_result[start:end] = batch_res


readObj = open("./"+fileName+".bed")
outputObj = open("./"+fileName+"/"+fileName+".out",'w')
for i,line in enumerate(readObj):
	line = line.strip("\r\n")
	temps = line.split("\t")
	pos = temps[0]
	start = temps[1]
	end = temps[2]
	score = test_predict_result[i][0]
	outputObj.write(pos+"\t"+start+"\t"+end+"\t"+str(score)+"\n")
readObj.close()
outputObj.close()

print "BiRen predict Done."
