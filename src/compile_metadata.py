import os
import pandas as pd
import numpy as np
import h5py
import json

from config import BASE_DIR


def add_files_from_dir(data_path):
	columns = ['angle', 'distance', 'label', 'temp', 'timestamp', 'range_start_m', 'range_length_m', 'data_length', 'step_length_m', 'mode', 'sensor', 'range_interval', 'profile', 'update_rate', 'sampling_mode', 'repetition_mode', 'downsampling_factor', 'hw_accelerated_average_samples', 'gain', 'maximize_signal_attenuation', 'noise_level_normalization', 'tx_disable']
	df = pd.DataFrame(columns=columns)

	files = os.listdir(data_path)
	for file in files:
		f = h5py.File(data_path + file, 'r')

		intersection = [value for value in columns if value in list(f.keys())] 
		rest = [value for value in columns if value not in list(f.keys())]
		rest.remove('angle')

		if 'angel' in list(f.keys()):
			df.loc[file, 'angle'] = f['angel'][...]
		elif 'angle' in list(f.keys()):
			df.loc[file, 'angle'] = f['angle'][...]

		if 'distance' not in list(f.keys()):
			# df.loc[file, 'distance'] = f['distance'][...]
			rest.remove('distance')


		meta = json.loads(str(f['session_info'][...]))
		meta2 = json.loads(str(f['sensor_config_dump'][...]))
		meta.update(meta2)
		
		
		

		for key in intersection:
			df.loc[file, key] = f[key][...]

		for key in rest:
			df.loc[file, key] = meta[key]

	return df


if __name__ == '__main__':
	data_path = BASE_DIR + '\\data\\data\\'
	df = add_files_from_dir(data_path)
	# data_path = BASE_DIR + '\\data\\nollmatning\\'
	# add_files_from_dir(data_path)

	df.to_csv(BASE_DIR + '\\data\\metadata2.csv')
