import pandas as pd
import plotly.express as px

import numpy as np

import requests
import io

from datetime import date, datetime, timedelta

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

#Erstellen eines Dictionary mit allen Ländern drin
df_countries = df_general.groupby(['location']).count()
countries = []

for country in df_countries.iterrows():
    if (country[0] != "Africa" and country[0] != "Asia" and country[0] != "Europe" and
        country[0] != "European Union" and country[0] != "International" and country[0] != "North America" and
        country[0] != "Oceania" and country[0] != "South America" and country[0] != "World"):

        countries.append({"label": country[0], "value": country[0]})

yesterday = datetime.now() - timedelta(1)
yesterday_date = datetime.strftime(yesterday, '%Y-%m-%d')
yesterday_date2 = datetime.strftime(yesterday, '%d.%m.%Y')

app.layout = html.Div(children = [
    #header mit Titel
    html.Div(children = [
        html.H1("GENIUSS Covid-19 Dashboard")
    ], className="header"),

    #Container für die Diagramme / Haupteil der Seite
    html.Div(children = [
        #Auflistung new Cases linke Seite
        html.Div(children = [
            html.H2("New Cases from " + yesterday_date2, className="list-title"),
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
                html.H2("1. Parameter", className="dropdown-title"),
                html.H2("2. Parameter", className="dropdown-title"),
                html.H2("Time", className="dropdown-title")
            ], className="dropdown-titles"),

            #Dropdown-Menüs
            html.Div(children = [
                html.Div(
                    dcc.Dropdown(id='country',
                         options = countries,
                         multi = False,
                         value='Switzerland',
                         className="dropdown"),
                    className="dropdown-menu"
                ),

                html.Div(
                    dcc.Dropdown(id='show',
                         options = [
                             {"label": "New Cases", "value": 'new_cases'},
                             {"label": "Total Cases", "value": 'total_cases'},
                             {"label": "New Deaths", "value": 'new_deaths'},
                             {"label": "Total Deaths", "value": 'total_deaths'},
                             {"label": "New Vaccinations", "value": 'new_vaccinations'},
                             {"label": "People Vaccinated", "value": 'people_vaccinated'},
                             {"label": "People Fully Vaccinated", "value": 'people_fully_vaccinated'}],
                         multi = False,
                         value='new_cases',
                         className="dropdown"),
                    className="dropdown-menu"
                ),

                html.Div(
                    dcc.Dropdown(id='show2',
                         options = [
                             {"label": "New Cases", "value": 'new_cases'},
                             {"label": "Total Cases", "value": 'total_cases'},
                             {"label": "New Deaths", "value": 'new_deaths'},
                             {"label": "Total Deaths", "value": 'total_deaths'},
                             {"label": "New Vaccinations", "value": 'new_vaccinations'},
                             {"label": "People Vaccinated", "value": 'people_vaccinated'},
                             {"label": "People Fully Vaccinated", "value": 'people_fully_vaccinated'}],
                         multi = False,
                         value='new_vaccinations',
                         className="dropdown"),
                    className="dropdown-menu"
                ),

                html.Div(
                    dcc.DatePickerRange(
                        id='starttime',
                        min_date_allowed=date(2020, 1, 1),
                        max_date_allowed=yesterday_date,
                        initial_visible_month=yesterday_date,
                        start_date=date(2020, 1, 1),
                        end_date=yesterday_date
                    ),
                    className="dropdown-menu"
                )
            ], className="dropdown-menues"),

            #Diagramme
            html.Div(children = [
                html.Div(children = [
                    dcc.Graph(id='maingraph1', figure = {}),
                    html.Div("Hier Beschreibung vom Diagramm?")], className="graph"
                ),
                html.Div(children = [
                    dcc.Graph(id='maingraph2', figure = {}),
                    html.Div("Hier Beschreibung vom Diagramm?")], className="graph"
                ),
                html.Div(children = [
                    dcc.Graph(id='maingraph3', figure = {}),
                    html.Div("Hier Beschreibung vom Diagramm?")], className="graph"
                ),
                html.Div(children = [
                    dcc.Graph(id='maingraph4', figure = {}),
                    html.Div("Hier Beschreibung vom Diagramm?")], className="graph"
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
            html.Div("Dieses Dashboard wurde für das Modul DGUI an der FHGR entwickelt."),
            html.Div("Als Datengrundlage dienen die Covid-Daten von ourworldindata.org.")
        ])
    ], className="footer"),
], className="container")

@app.callback(
    [Output(component_id='newcases', component_property='figure'),
    Output(component_id='maingraph1', component_property='figure'),
    Output(component_id='maingraph2', component_property='figure'),
    Output(component_id='maingraph3', component_property='figure'),
    Output(component_id='maingraph4', component_property='figure')],
    [Input(component_id='continent', component_property='value'),
    Input(component_id='country', component_property='value'),
    Input(component_id='show', component_property='value'),
    Input(component_id='starttime', component_property='start_date'),
    Input(component_id='starttime', component_property='end_date'),
    Input(component_id='show2', component_property='value')]
)

def update_graph(option_slctd, option_slctd2, option_slctd3, option_slctd4, option_slctd5, option_slctd6):
    #Bearbeitung der Daten für alle Daten
    dff = df_general.copy()

    dff.replace('', np.NaN, inplace = True)
    numbers = dff._get_numeric_data()
    numbers[numbers < 0] = np.NaN
    dff[['continent']] = dff[['continent']].replace(np.NaN, 'undefined')

    dff1 = dff.copy()

    dff = dff[dff["location"] == option_slctd2]
    dff = dff[dff["date"] >= option_slctd4]
    dff = dff[dff["date"] <= option_slctd5]

    dff1_country = dff1[dff1["location"] == option_slctd2]
    dff1_continent = dff1_country.iloc[0]['continent']
    dff1 = dff1[dff1["continent"] == dff1_continent]
    dff1 = dff1[dff1["date"] == option_slctd5]

    #Bearbeitung der Daten für die neusten Einträge
    dff_latest = df_latest.copy()
    dff_latest.replace('', np.NaN, inplace=True)
    dff_latest.dropna(subset=['continent'], inplace=True)
    dff_latest.dropna(subset=['new_cases'], inplace=True)

    #dff_latest1 = dff_latest.copy() || wird momentan nicht benötigt

    dff_latest = dff_latest[dff_latest["continent"] == option_slctd]

    #wird momentan nicht benötigt
    #dff_latest1_country = dff_latest1[dff_latest1["location"] == option_slctd2]
    #dff_latest1_continent = dff_latest1_country.iloc[0]['continent']
    #dff_latest1 = dff_latest1[dff_latest1["continent"] == dff_latest1_continent]

    #Horizontales Bardiagramm
    fig = px.bar(dff_latest, x="new_cases", y="location", orientation='h')
    fig.update_layout(plot_bgcolor="#3F3F3f", paper_bgcolor="#3F3F3f", font_color="#DfDCDA", height=1000, margin=dict(pad=8))
    fig.update_yaxes(tickmode='linear',title=None)
    fig.update_xaxes(title=None)
    fig.update_traces(marker_color="#8F3B8E")

    #Liniendiagramm
    fig2 = px.line(dff, x='date', y=option_slctd3)
    fig2.update_layout(plot_bgcolor="#757575", paper_bgcolor="#757575", font_color="#DfDCDA")
    fig2.update_yaxes(title=None)
    fig2.update_xaxes(title=None)

    #Bardiagramm - wid momentan nicht benötigt
    #fig3 = px.bar(dff, x="date", y=option_slctd6)
    #fig3.update_layout(plot_bgcolor="#757575", paper_bgcolor="#757575", font_color="#DfDCDA")
    #fig3.update_yaxes(title=None)
    #fig3.update_xaxes(title=None)

    fig3 = px.line(dff, x='date', y=option_slctd6)
    fig3.update_layout(plot_bgcolor="#757575", paper_bgcolor="#757575", font_color="#DfDCDA")
    fig3.update_yaxes(title=None)
    fig3.update_xaxes(title=None)

    #Streudiagramm
    fig4 = px.scatter(dff1, x=option_slctd3, y=option_slctd6, size="population", color="location")
    fig4.update_layout(plot_bgcolor="#757575", paper_bgcolor="#757575", font_color="#DfDCDA")
    fig4.update_yaxes(title=None)
    fig4.update_xaxes(title=None)

    #Kartendiagramm
    fig5 = px.choropleth(dff1, locations="iso_code",color=option_slctd3)
    fig5.update_geos(visible=False, resolution=50, scope=dff1_continent.lower())
    fig5.update_layout(plot_bgcolor="#757575", paper_bgcolor="#757575", geo=dict(bgcolor="#757575"), font_color="#DfDCDA",margin={"r":0,"t":0,"l":0,"b":0})

    return fig, fig2, fig3, fig4, fig5

if __name__ == '__main__':
    app.run_server(debug=True)
