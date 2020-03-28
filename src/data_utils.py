import os
import pandas as pd
import numpy as np  
import h5py
import json

from config import *


# input: 	string path to h5 file
# output: 	pandas dataframe with frames as rows and depth samples as columns
def read_data(path):
	f = h5py.File(path, 'r')
	data = np.squeeze(f['data'][:,:,:])
	if (len(data.shape) != 2):
		print('Data has invalid shape: ' + path)
		return
	index = [i for i in range(data.shape[0])]

	return pd.DataFrame(data=data, index=index)

# returns a dict of metadata
def read_meta(path):
	f = h5py.File(path, 'r')
	meta = json.loads(str(f['session_info'][...]))
	meta2 = json.loads(str(f['sensor_config_dump'][...]))
	meta.update(meta2)
	return meta



# input:	pandas dataframe with columns of iq data in complex numbers
# output:	two pandas dataframea with columns for each depth sample's amplitude and phase
def amplitude(input):
	return input.apply(np.absolute)

def phase(input):
	return input.apply(np.angle)

def polar(input):
	return amplitude(input), phase(input)

def real(input):
	return input.apply(np.real)

def imag(input):
	return input.apply(np.imag)

def rect(input):
	return real(input), imag(input)