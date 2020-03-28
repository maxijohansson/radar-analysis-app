import os
import pandas as pd
import time
import numpy as np

import dash
import dash_table as dt
import dash_daq as daq
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

import data_utils as utils
import app_elements as elements

from config import *


app.layout = html.Div([
    html.Div([
        elements.selected_file_table
    ]),
    html.Div(
        dcc.Tabs(id='tabs', value='settings_tab', children=[
            dcc.Tab(label='Settings', value='settings_tab'),
            dcc.Tab(label='Amplitude/Phase', value='ap_tab'),
            dcc.Tab(label='Histograms', value='hist_tab'),
            dcc.Tab(label='Z-plane', value='z_tab')
        ]),
    ),
    dcc.Loading(
        id = "loading_main_tab", 
        children = [html.Div(id='main_tab')], 
        type = "default"
    ),
    html.Div(id='hidden_div', style={'display':'none'})
])


@app.callback(
    Output('main_tab', 'children'),
    [Input('tabs', 'value')],
    [State('selected_file_table', 'data')])
def render_tab(tab, selected_files):
    # time.sleep(1)

    files_to_graph = [row['filename'] for row in selected_files if row['filename'] != None]
    ids_to_graph =  [row['id'] for row in selected_files if row['id'] != None]

    if tab == 'settings_tab':
        return elements.settings_tab(files_to_graph)

    elif tab == 'ap_tab':
        return html.Div(elements.ap_tab(files_to_graph))

    elif tab == 'hist_tab':
        return html.Div(elements.hist_tab(files_to_graph))

    elif tab == 'z_tab':
        return html.Div(elements.z_tab(files_to_graph))


@app.callback(
    Output('selected_file_table', 'data'),
    [Input('metadata_table', 'selected_rows')],
    [State('selected_file_table', 'data')])
def update_settings(selected_ids, prev_selection):
    if selected_ids is None or len(selected_ids) == 0:
        return empty_selected_file_df.to_dict('records')
    elif len(selected_ids) > max_selected_files:
        return prev_selection
    else:
        file_table = empty_selected_file_df
        relevant_data = metadata.loc[:, file_table_columns]
        for i, selected_id in enumerate(selected_ids):
            file_table.iloc[i, :] = relevant_data.iloc[selected_id, :]

        return file_table.to_dict('records')


@app.callback(
    Output('metadata_table', 'selected_rows'),
    [Input('clear_selections', 'n_clicks')])
def clear_selections(click):
    return []


if __name__ == '__main__':
    app.run_server(debug=True)


