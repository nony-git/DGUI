import pandas as pd
import plotly.express as px

import numpy as np

import requests
import io

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


app = dash.Dash(__name__)


CSV_URL = 'https://covid.ourworldindata.org/data/owid-covid-data.csv'
csv_data = requests.get(CSV_URL).content 
df = pd.read_csv(io.StringIO(csv_data.decode('latin1')), sep=',')


app.layout = html.Div(children = [    
        
    html.H1("GENIUSS Covid-19 Dashboard", 
            style = {'text-align': 'center'}),
    html.H4("Aufgabenblatt 7, Aufgabe 13 und 14", style = {'text-align': 'center'}),
    
    #Aufgabe 13a) Dropbdownmenu für das Attribut "Continent" mit dem Default-Value "Europe"
    dcc.Dropdown(id='continent',
                 options = [
                     {"label": "Europe", "value": 'Europe'},
                     {"label": "North America", "value": 'North America'},
                     {"label": "South America", "value": 'South America'},
                     {"label": "Asia", "value": 'Asia'},
                     {"label": "Oceania", "value": 'Oceania'},
                     {"label": "Africa", "value": 'Africa'},
                     {"label": "undefined", "value": 'undefined'}],
                 multi = False,
                 value='Europe',
                 style = {"width": "40%"}),
    
    html.Div(children = [   
    html.H3("Aufgabe 13", style = {'text-align': 'left'}),   
    dcc.Graph(id='covidplot', figure = {}),
    #Aufgabe 14b) Versuch den Zeitverlauf mittels Slider im Streudiagramm darzustellen
    dcc.Slider(
        id='the_slider',
        min=2020,
        max=2021,
        value=2021,
        step=0.0833,
        marks={i: '{}'.format(i) for i in range(2020, 2022)},
    ),
    ],
                               style={'display': 'block', 
                                      'vertical-align': 'top', 
                                      'margin-left': '3vw', 'margin-top': '3vw',
                                      'width': '40vw', 'height': '40vh'}),
    
    html.Div(children = [
    html.H3("Aufgabe 14", style = {'text-align': 'left'}),
    html.Div(children = [
        dcc.Graph(id='covidplot2', figure = {}),
        dcc.Graph(id='covidplot3', figure = {})
        ],
        style={'display': 'flex',
               'justify-content': 'space-between',
               'widht': '100%'
               })], 
        style={'display': 'flex',
               'flex-direction': 'column',
               'vertical-align': 'top', 
               'margin-left': '3vw', 'margin-top': '10vw',
               'width': '80vw', 'height': '40vh'})
])

@app.callback(
    [Output(component_id='covidplot', component_property='figure'),
     Output(component_id='covidplot2', component_property='figure'),
     Output(component_id='covidplot3', component_property='figure')],
    [Input(component_id='continent', component_property='value'),]
     
)

def update_graph(option_slctd):
    dff = df.copy()
        
    dff.replace('', np.NaN, inplace = True)
    numbers = dff._get_numeric_data()
    numbers[numbers < 0] = np.NaN
    dff[['continent']] = dff[['continent']].replace(np.NaN, 'undefined')
    dff[['gdp_per_capita']] = dff[['gdp_per_capita']].replace(np.NaN, 0)
    dff[['edit_total_cases']] = np.max(dff['total_cases'])
    grouped = dff.groupby(['location', 'continent'])['total_deaths'].max().reset_index()

    grouped = grouped[grouped["continent"] == option_slctd]
    dff = dff[dff["continent"] == option_slctd]
   
    #Aufgabe 13b) Streudiagramm 
    fig = px.scatter(dff, x="new_cases", y="new_deaths", color="location",  
                     marginal_x="box", marginal_y="box", size='gdp_per_capita', trendline="ols",
                     title="Streudiagramm für Kontinent: "+option_slctd)
    
    #Aufgabe 14a) weitere Diagramme
    fig2 = px.line(dff, x='date', y='new_cases', line_group='location', color='location', 
                  title='Entwicklung der neuen Fälle für Kontinent: '+option_slctd)
    
    fig3 = px.bar(grouped, x="location", y="total_deaths", color="location",  
                  title="Total Tote pro Land für Kontinent: "+option_slctd)

    return fig, fig2, fig3


if __name__ == '__main__':
    app.run_server(debug=True)
