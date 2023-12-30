#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 29 08:49:12 2023

@author: shaymo
"""

from dash import Dash, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.graph_objects as go
import dash_mantine_components as dmc


#incorporate data
df = pd.read_csv('sentiment_analysis_news.csv')

count = df['sentiment'].value_counts()
positive_count = int(count.iloc[0])
negative_count = int(count.iloc[1])
neutral_count = int(count.iloc[2])

#initialize the app
external_stylesheets = [dmc.theme.DEFAULT_COLORS]
app = Dash(__name__, external_stylesheets=external_stylesheets)

def generate_graph():
    colors = ['#47B39C', '#FFC154', '#EC6B56']
    labels = ['Positive', 'Neutral', 'Negative']
    values = [positive_count, neutral_count, negative_count]
    
    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    fig.update_traces(hoverinfo='value', textinfo='percent', marker=dict(colors=colors))

    return fig


#app layout
app.layout = dmc.Container([
    dmc.Title('Analyzing Sentiments on \'Voice to Parliament\'', color = 'blue', size='h2'),
    dmc.Space(h=20),
    dmc.Text(align='left'),
    dmc.MultiSelect(
        id='column_selector',
        placeholder='Select the column you want to display!',
        value=[],
        clearable=True,
        data=df.columns, 
        style={'width':400},
        ),
    dmc.Grid([
        dmc.Col([
            dash_table.DataTable(
                id='selected_column_table',
                columns = [
                    {'name':i, 'id':i,'hideable':True} for i in df.columns
                    ],
                css=[{'selector': '.show-hide', 'rule': 'display: none'}],
                column_selectable='multi',
                page_size=10, 
                tooltip_data=[
                    {
                        column:{'value':str(value), 'type':'markdown'}
                        for column, value in row.items()
                        } for row in df.to_dict('records')
                    ],
                tooltip_duration=None,
                style_data={'height':'auto'},
                style_table={'overflowX':'auto'}, 
                style_cell={'textAlign':'left',
                            'overflow':'hidden',
                            'textOverflow':'ellipsis',
                            'maxWidth':0,
                            },
                style_cell_conditional=[],
                ),
            ], span=6),
        dmc.Col([dcc.Graph(figure=generate_graph(), id='pie chart')], span=6),
        ]),
    ], fluid=True)

@callback(
    Output('selected_column_table', 'data'), 
    Output('selected_column_table', 'style_cell_conditional'),
    Input('column_selector', 'value')
    )

def update_table(selected_columns):
    if not selected_columns:
        return df.to_dict('records'),[]
    else:
        return df[selected_columns].to_dict('records'), [
            {'if':{'column_id':col}, 'display':'none'}
            for col in df.columns if col not in selected_columns
            ]
    

#run the app
if __name__ == '__main__':
    app.run(debug=True)