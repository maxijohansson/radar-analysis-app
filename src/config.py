import os
import dash
import pandas as pd
import numpy as np

# from compile_metadata import add_files_from_dir

BASE_DIR = os.path.join(os.path.dirname( __file__ ), '..')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config['suppress_callback_exceptions'] = True
app.config.suppress_callback_exceptions = True

data_path = BASE_DIR + '\\data\\data\\'
files = os.listdir(data_path)
# files_to_graph = []
file_table_columns = ['filename', 'timestamp', 'angle', 'range_interval', 'data_length', 'step_length_m', 'update_rate', 'id']
colors = ['#0074D9', '#FF4136', '#3D9970', '#FF851B', '#B10DC9', '#AAAAAA', '#001f3f', '#7FDBFF']
max_selected_files = 5
nan_row = [np.nan for col in file_table_columns]
empty_selected_file_df = pd.DataFrame(columns=file_table_columns, data = [nan_row for i in range(max_selected_files)])

marks = {i: '{}'.format(i) for i in range(0, 2001, 100)}
marks.update({2100: 'auto'})

metadata = pd.read_csv(BASE_DIR + '\\data\\metadata.csv', delimiter = ';')
metadata = metadata[metadata['Column1'].isin(files)]
metadata.reset_index(inplace=True, drop=False)
metadata['filename'] = metadata['Column1']
metadata['id'] = metadata.index
metadata.set_index('Column1', inplace=True)
metadata.rename_axis(None, inplace=True)
metadata = metadata[['filename'] + [c for c in metadata if c not in ['filename']]]
metadata_dict = metadata.to_dict('records')
metadata_columns = [ {"name": i, "id": i, "deletable": False, "selectable": True} for i in metadata.columns ]

# print(metadata.to_dict('records'))

# selected_rows = [0]
# file_table = metadata.iloc[selected_rows, :]
# print(file_table.columns)
# file_table = file_table.loc[:, file_table_columns]
# print(file_table.to_dict('records'))

# metadata.rename(columns={'Column1': 'filename'}, inplace=True)


