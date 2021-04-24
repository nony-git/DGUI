# Run with python index.py and
# visit http://127.0.0.1:8050/ browser

import pandas as pd
import plotly.express as px

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


#Aufgabe 11a) Einlesen des Covid-19 Datensatzes mit einem Pandas DataFrame
df = pd.read_csv("https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv")


#Aufgabe 11b) Berechnen von Mittelwert, Standardabweichung, Varianz, Median und Maximum für das Attribut «new_cases»
print(df[['new_cases']])


#Aufgabe 12c) Land mit dem höchsten Mittelwert beim Attribut «new_cases» 
