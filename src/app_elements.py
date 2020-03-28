import numpy as np

import dash
import dash_table as dt
import dash_daq as daq
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

import plotly.graph_objects as go

import data_utils as utils

from config import *


# The table at the top of the page, always visible
selected_file_table = (
    dt.DataTable(
        id = 'selected_file_table',
        columns = [
            {"name": col, "id": col} for col in file_table_columns
        ],
        data = empty_selected_file_df.to_dict('records'),
        style_as_list_view = True,
        style_header = {
            'backgroundColor': 'white',
            'fontWeight': 'bold'
        },
        style_data_conditional = [{
                "if": {"row_index": i},
                "backgroundColor": colors[i],
                'color': 'white'
            } for i in range(len(colors))
        ],
        style_cell_conditional = [{
                'if': {'column_id': c},
                'textAlign': 'left'
            } for c in ['filename']
        ]
    )
)


# Returns the Settings tab
def settings_tab(selected_files):
    selected_ids = metadata.loc[selected_files, 'id']

    return(

        html.Div(
            dbc.Button('Clear selections', color='Primary', id='clear_selections')
        ),
        html.Div(
            [
            html.Div(
                dt.DataTable(
                    id='metadata_table',
                    columns = metadata_columns,
                    data=metadata_dict,
                    filter_action="native",
                    sort_action="native",
                    sort_mode="multi",
                    row_selectable="multi",
                    selected_rows=selected_ids,
                    page_current= 0,
                    style_as_list_view=True,
                    style_cell_conditional=[{
                            'if': {'column_id': c},
                            'textAlign': 'left'
                        } for c in ['filename']
                    ],
                    style_data_conditional=[{
                            'if': {'row_index': 'odd'},
                            'backgroundColor': 'rgb(248, 248, 248)'
                        }
                    ]
                )
            ),
            html.Div(
                [
                html.Label('Amplitude range'),
                dcc.Slider(
                    id = 'max_amplitude',
                    min = 0,
                    max = 2100,
                    step = 100,
                    marks = marks,
                    value = 2100,
                ),
                ],
                style = {'width': '48%', 'display': 'inline-block'}
            )
            ],
            style={'width': '100%'}
        )

    )


# Returns the Amplitude/Phase tab
def ap_tab(files_to_graph):
    if len(files_to_graph) > 0:
        amplitude, phase = update_ap_graphs(files_to_graph)
    else:
        amplitude, phase = {'data': [], 'layout': {}}, {'data': [], 'layout': {}}

    return(
        html.Div([
            dcc.Graph(id='amplitude', figure=amplitude),
            dcc.Graph(id='phase', figure=phase),
        ], style={'display': 'inline-block', 'height': 400, 'width': '100%'})
    )


def z_tab(files_to_graph):
    z_plane = update_z_graphs(files_to_graph)

    return(
        html.Div([
            dcc.Graph(
                id = 'z_plane',
                figure = z_plane,
                style={ 'width': '50%', 'height': '500px'}
            )
        ])
    )


def hist_tab(files_to_graph):
    if len(files_to_graph) > 0:
        amplitude, phase = update_hist(files_to_graph)
    else:
        amplitude, phase = {'data': [], 'layout': {}}, {'data': [], 'layout': {}}

    return(
        html.Div([
            html.Div(
                dcc.Graph(id='amplitude_hist', figure=amplitude),
                style = {'display': 'inline-block', 'width': '48%'}
            ),
            html.Div(
                dcc.Graph(id='phase_hist', figure=phase),
                style = {'display': 'inline-block', 'width': '48%'}
            )
            
        ], style={'display': 'inline-block', 'height': 400, 'width': '100%'})
    )


# Returns a figure 
def ap_graph(x, ys, xaxis, yaxis):
    data = []
    j = 0
    for x,y in zip(x,ys):
        # colors = [mean_color, 'darkgray', 'darkgray']
        opacities = [1.0, 0.25, 0.25]
        for i,y in enumerate(y):
            data.append(
                dict(
                x = x,
                y = y,
                opacity = opacities[i],
                mode = 'markers',
                marker = {
                    'size': 2,
                    'color': colors[j],
                })
            )
        j = j+1
    
    return {
        'data': data,
        'layout': dict(
            xaxis = {
                'title': xaxis,
                'tickmode': 'linear',
                'dtick': 0.05,
            },
            yaxis = {
                'title': yaxis,
            },
            margin = {'l': 50, 'b': 30, 't': 10, 'r': 0},
            hovermode = 'closest',
            showlegend=False
        )
    }


# Returns two figures
def update_ap_graphs(files_to_graph):
    xs = []
    y_amplitudes = []
    y_phases = []

    for i,file in enumerate(files_to_graph):
        iq = utils.read_data(data_path + file)
        amplitude, phase = utils.polar(iq)
        meta = utils.read_meta(data_path + file)

        d = meta['step_length_m']
        x = [meta['range_start_m'] + d*i for i in range(meta['data_length'])]
        xs.append(x)
    
        y_amplitudes.append([])
        y_amplitudes[i].append(amplitude.mean(axis='rows'))
        y_amplitudes[i].append(y_amplitudes[i][0] + amplitude.std())
        y_amplitudes[i].append(y_amplitudes[i][0] - amplitude.std())

        y_phases.append([])
        y_phases[i].append(phase.mean(axis='rows'))
        y_phases[i].append(y_phases[i][0] + phase.std())
        y_phases[i].append(y_phases[i][0] - phase.std())

    amplitude = ap_graph(xs, y_amplitudes, 'distance (m)', 'amplitude')
    phase = ap_graph(xs, y_phases, 'distance (m)', 'phase')
    
    return amplitude, phase


# Returns a figure
def z_graph(xs, ys, xaxis, yaxis):
    data = []
    j = 0
    for x_trio,y_trio in zip(xs, ys):
        i = 0
        opacities = [1.0, 0.25, 0.25]
        for x, y in zip(x_trio, y_trio):
            data.append(dict(
                x = x,
                y = y,
                opacity = opacities[i],
                mode = 'markers',
                marker = {
                    'size': 2,
                    'color': colors[j],
                }
            ))
            i = i+1
        j = j+1
    
    return {
        'data': data,
        'layout': dict(
            xaxis = {
                'title': xaxis,
            },
            yaxis = {
                'title': yaxis,
            },
            margin = {'l': 50, 'b': 30, 't': 10, 'r': 0},
            hovermode = 'closest',
            showlegend=False,
            scaleratio=1
        )
    }



def update_z_graphs(files_to_graph):
    xs = []
    ys = []

    for i,file in enumerate(files_to_graph):
        iq = utils.read_data(data_path + file)
        a, b = utils.rect(iq)
        meta = utils.read_meta(data_path + file)

        xs.append([])
        xs[i].append(a.mean(axis='rows'))
        # xs[i].append(xs[i][0] + a.std())
        # xs[i].append(xs[i][0] - a.std())
    
        ys.append([])
        ys[i].append(b.mean(axis='rows'))
        # ys[i].append(ys[i][0] + b.std())
        # ys[i].append(ys[i][0] - b.std())

    z = z_graph(xs, ys, 'real', 'imaginary')
    
    return z


# returns figures
def update_hist(files_to_graph):
    amplitudes_at_peak = []
    phases_at_peak = []

    for i,file in enumerate(files_to_graph):
        iq = utils.read_data(data_path + file)
        amplitude, phase = utils.polar(iq)
        meta = utils.read_meta(data_path + file)

        d = meta['step_length_m']
        x = [meta['range_start_m'] + d*i for i in range(meta['data_length'])]

        x_peak_n = amplitude.mean(axis='rows').idxmax()
        x_peak_d = x[x_peak_n]

        amplitudes_at_peak.append(amplitude[x_peak_n])
        phases_at_peak.append(phase[x_peak_n])

    amplitude = histogram(amplitudes_at_peak, 'amplitude at first peak', 'distribution')
    phase = histogram(phases_at_peak, 'phase at first peak', 'distribution')
    
    return amplitude, phase


def histogram(sets, xaxis, yaxis):
    data = []
    j = 0
    for l in sets:
        data.append(go.Histogram(
            x = l, 
            opacity = 0.5,
            marker_color = colors[j]
        ))
        j = j+1
    
    return {
        'data': data,
        'layout': dict(
            xaxis = {
                'title': xaxis,
            },
            yaxis = {
                'title': yaxis,
            },
            margin = {'l': 50, 'b': 30, 't': 10, 'r': 0},
            hovermode = 'closest',
            showlegend = False,
            barmode = 'overlay'
        )
    }

