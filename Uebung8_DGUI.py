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

#laden des gesamten Datensatzes
CSV_URL_GENERAL = 'https://covid.ourworldindata.org/data/owid-covid-data.csv'
csv_data_general = requests.get(CSV_URL_GENERAL).content
df_general = pd.read_csv(io.StringIO(csv_data_general.decode('latin1')), sep=',')

#Laden der letzetn Änderungen / neusten Einträge
CSV_URL_LATEST = 'https://covid.ourworldindata.org/data/latest/owid-covid-latest.csv'
csv_data_latest = requests.get(CSV_URL_LATEST).content
df_latest = pd.read_csv(io.StringIO(csv_data_latest.decode('latin1')), sep=',')

app.layout = html.Div(children = [
    #header mit Titel
    html.Div(children = [
        html.H1("GENIUSS Covid-19 Dashboard")
    ], className="header"),

    #Container für die Diagramme / Haupteil der Seite
    html.Div(children = [
        #Auflistung new Cases linke Seite
        html.Div(children = [
            html.H2("New Cases", className="list-title"),
            dcc.Dropdown(id='continent',
                 options = [
                     {"label": "Europe", "value": 'Europe'},
                     {"label": "North America", "value": 'North America'},
                     {"label": "South America", "value": 'South America'},
                     {"label": "Asia", "value": 'Asia'},
                     {"label": "Oceania", "value": 'Oceania'},
                     {"label": "Africa", "value": 'Africa'}],
                 multi = False,
                 value='Europe',
                 className="dropdown dropdown-list"),
            dcc.Graph(id='newcases', figure = {})
        ], className="wrapper-list"),

        #Diagramme in der Mitte
        html.Div(children = [
            #Titel der Dropdown-Menüs
            html.Div(children = [
                html.H2("Country", className="dropdown-title"),
                html.H2("Show", className="dropdown-title"),
                html.H2("Time", className="dropdown-title")
            ], className="dropdown-titles"),

            #Dropdown-Menüs
            html.Div(children = [
                html.Div(
                    dcc.Dropdown(id='country',
                         options = [
                             {"label": "Switzerland", "value": 'Switzerland'},
                             {"label": "Austria", "value": 'Austria'},
                             {"label": "Germany", "value": 'Germany'}],
                         multi = False,
                         value='Switzerland',
                         className="dropdown"),
                    className="dropdown-menu"
                ),

                html.Div(
                    dcc.Dropdown(id='show',
                         options = [
                             {"label": "Cases", "value": 'Cases'},
                             {"label": "Deaths", "value": 'Deaths'},
                             {"label": "Hospitalizations", "value": 'Hospitalizations'}],
                         multi = False,
                         value='Cases',
                         className="dropdown"),
                    className="dropdown-menu"
                ),

                html.Div(
                    dcc.Dropdown(id='time',
                         options = [
                             {"label": "Test", "value": 'Test'},
                             {"label": "Test1", "value": 'Test1'},
                             {"label": "Test2", "value": 'Test2'}],
                         multi = False,
                         value='Test',
                         className="dropdown"),
                    className="dropdown-menu"
                )
            ], className="dropdown-menues"),

            #Diagramme
            html.Div(children = [
                html.Div(
                    dcc.Graph(id='newcases_country', figure = {}), className="graph"
                )
            ], className="graphs"),
        ], className="wrapper-graphs"),
    ], className="graph-container"),

    #footer mit Infos zum Projekt
    html.Div(children = [
        html.Div(children = [
            html.Div("Gruppe 7"),
            html.Div("Alan Müller, Gene Bichler, Nino Parolari, Silvan Reis")
        ]),
        html.Div(children = [
            html.Div("Dieses Dashboard wurde für das Modul DGUI an der FHGR entwickelt.")
        ])
    ], className="footer"),
], className="container")

@app.callback(
    [Output(component_id='newcases', component_property='figure'),
    Output(component_id='newcases_country', component_property='figure')],
    [Input(component_id='continent', component_property='value'),
    Input(component_id='country', component_property='value')]
)

def update_graph(option_slctd, option_slctd2):
    #Bearbeitung der Daten für alle Daten
    dff = df_general.copy()

    dff.replace('', np.NaN, inplace = True)
    numbers = dff._get_numeric_data()
    numbers[numbers < 0] = np.NaN
    dff[['continent']] = dff[['continent']].replace(np.NaN, 'undefined')

    dff = dff[dff["location"] == option_slctd2]

    #Bearbeitung der Daten für die neusten Einträge
    dff_latest = df_latest.copy()
    dff_latest.replace('', np.NaN, inplace=True)
    dff_latest.dropna(subset=['continent'], inplace=True)
    dff_latest.dropna(subset=['new_cases'], inplace=True)

    dff_latest = dff_latest[dff_latest["continent"] == option_slctd]

    #Horizontales Bar-Diagramm
    fig = px.bar(dff_latest, x="new_cases", y="location", orientation='h')
    fig.update_layout(plot_bgcolor="#3F3F3f", paper_bgcolor="#3F3F3f", font_color="#DfDCDA", height=1000, margin=dict(pad=8))
    fig.update_yaxes(tickmode='linear',title=None)
    fig.update_xaxes(title=None)
    fig.update_traces(marker_color="#8F3B8E")

    #Linien Diagramm
    fig2 = px.line(dff, x='date', y='new_cases')
    fig2.update_layout(plot_bgcolor="#3F3F3f", paper_bgcolor="#3F3F3f", font_color="#DfDCDA")
    fig2.update_yaxes(title=None)
    fig2.update_xaxes(title=None)

    return fig, fig2

if __name__ == '__main__':
    app.run_server(debug=True)
