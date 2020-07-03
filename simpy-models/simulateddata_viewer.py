import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import plotly
from dash.dependencies import Input, Output
import pandas as pd
import os
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt
import configparser
config = configparser.ConfigParser()
config.read("C:/Users/H395978/PycharmProjects/Neo4j-ProductionFlow-UI/setup.ini")

model_file_path = config['MODEL_SETTINGS']['model_file_path']
simpy_path = config['MODEL_SETTINGS']['simpy_path']


def invoke_as_api():
    print('Data viewer is loading the table')
    os.chdir(simpy_path)
    df = pd.read_csv('simulated_monty2_sfcflow_noventil.csv')

    df2 = df.tail(20)
    print(df2.head())
    app = dash.Dash(__name__)

    app.layout = dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df2.columns],
        data=df2.to_dict('records'),
    )

os.chdir(simpy_path)
df = pd.read_csv('simulated_monty2_sfcflow_noventil.csv')

df2 = df.tail(20)

app = dash.Dash(__name__)

def create_time_series(dff, axis_type, title):
    return {
        'data': [dict(
            x=dff['OPERATION'],
            y=dff['ELAPSED_QUEUE_TIME'],
            mode='lines+markers'
        )],
        'layout': {
            'height': 500,
            'margin': {'l': 20, 'b': 30, 'r': 10, 't': 10},
            'annotations': [{
                'x': 0, 'y': 0.85, 'xanchor': 'left', 'yanchor': 'bottom',
                'xref': 'paper', 'yref': 'paper', 'showarrow': False,
                'align': 'left', 'bgcolor': 'rgba(255, 255, 255, 0.5)',
                'text': title
            }],
            'yaxis': {'type': 'linear' if axis_type == 'Linear' else 'log'},
            'xaxis': {'showgrid': False}
        }
    }

# app.layout = dash_table.DataTable(
#     id='table',
#     columns=[{"name": i, "id": i} for i in df2.columns],
#     data=df2.to_dict('records'),
# )

app.layout = html.Div(
    html.Div([
        html.H1('Monty2 Simulated Results'),
        dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in df2.columns],
            data=df2.to_dict('records'),
        ),
        dcc.Graph(id='x-time-series',style={'height':'500px'}),
        html.Div([
            html.Iframe(id='iframe-livedata', src = 'https://cors-anywhere.herokuapp.com/https://snap-harisanthosh-venkatachalam-honeywell-com.eu-1.celonis.cloud/process-mining/analysis/d23044d6-5222-4672-b5bb-ea2863c706bf/link/frontend/documents/d23044d6-5222-4672-b5bb-ea2863c706bf/view/sheets/824c5d1b-bf00-43ee-a003-2ea428bc8e75/b/60a22b6d-2fe2-4012-a79b-ca0504c16be0', height = 600, width = 600)
        ],style={'width': '49%', 'display': 'inline-block', 'vertical-align': 'middle'}),
        dcc.Interval(
            id='interval-component',
            interval=3*1000, # in milliseconds
            n_intervals=0
        )
    ],style={'font-family': 'cursive','text-align': 'center'})
)

@app.callback([Output('table', 'data'),Output('x-time-series', 'figure')],
              [Input('interval-component', 'n_intervals')])
def update_metrics(n):
    os.chdir(simpy_path)
    df = pd.read_csv('simulated_monty2_sfcflow_noventil.csv')

    df2 = df.tail(20)
    return df2.to_dict('records'),create_time_series(df2, "Linear", "Simulation Results for Monty2")

if __name__ == '__main__':
    app.run_server(debug=False)
