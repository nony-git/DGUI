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
            style = {'text-align': 'left'}),
    html.H4("Aufgabenblatt 7, Aufgabe 13", style = {'text-align': 'left'}),
    
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
        
    dcc.Graph(id='covidplot', figure = {})], 
                               style={'display': 'inline-block', 
                                      'vertical-align': 'top', 
                                      'margin-left': '3vw', 'margin-top': '3vw',
                                      'width': '40vw', 'height': '40vh'})
])

@app.callback(
    Output(component_id='covidplot', component_property='figure'),
    [Input(component_id='continent', component_property='value')]
)

def update_graph(option_slctd):
    dff = df.copy()
        
    dff.replace('', np.NaN, inplace = True)
    numbers = dff._get_numeric_data()
    numbers[numbers < 0] = np.NaN
    dff[['continent']] = dff[['continent']].replace(np.NaN, 'undefined')
    dff[['gdp_per_capita']] = dff[['gdp_per_capita']].replace(np.NaN, 0)
    
    
    dff = dff[dff["continent"] == option_slctd]
   
    #Aufgabe 13b) Streudiagramm 
    fig = px.scatter(dff, x="new_cases", y="new_deaths", color="location",  
                     marginal_x="box", marginal_y="box", size='gdp_per_capita', trendline="ols",
                     title="Aufgabe 13b) Streudiagramm | Kontinent: "+option_slctd)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
