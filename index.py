import pandas as pd
import plotly.express as px

import numpy as np
import statistics

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


#Aufgabe 11a) Einlesen des Covid-19 Datensatzes mit einem Pandas DataFrame
df = pd.read_csv("https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv")

df.replace('', np.NaN , inplace = True)

df[['continent']] = df[['continent']].replace(np.NaN, "undefined")

numbers = df._get_numeric_data()
numbers[numbers < 0] = np.NaN


#Aufgabe 11b) Berechnen von Mittelwert, Standardabweichung, Varianz, Median und Maximum für das Attribut «new_cases»
mittelwert = np.mean(df['new_cases'])
print(mittelwert)

standardabweichung = np.std(df['new_cases'])
print(standardabweichung)

varianz = np.var(df['new_cases'])
print(varianz)

median = np.nanmedian(df['new_cases'])
print(median)

maximum = np.max(df['new_cases'])
print(maximum)


#Aufgabe 11c) Land mit dem höchsten Mittelwert beim Attribut «new_cases»
grouped = df.groupby(['location']).mean()


country = ''
highest_mean = 0

for index, row in grouped.iterrows():
    if row['new_cases'] > highest_mean:
        if (index != 'World' and index != 'Europe' and index != 'North America' and index != 'Asia' and index != 'Africa' and index != 'European Union' and index != 'Oceania' and index != 'South America'):
            highest_mean = row['new_cases']
            country = index

print(country)
print(highest_mean)


#Aufgabe 12a) Streudiagramm erzeugen
#ohne Farbe funktioniert
fig = px.scatter_matrix(df, dimensions=["total_cases", "new_cases", "hosp_patients", "new_vaccinations"])
fig.show()

#mit Farbe Fehlermeldung
fig = px.scatter_matrix(df, dimensions=["total_cases", "new_cases", "hosp_patients", "new_vaccinations"], color="continent")
fig.show()


#Aufgabe 12b) Mittelwert von "total cases", "new cases", "hosp_patients" und "new_vaccinations" für alle Länder
groupedscat = df.groupby(['location','continent']).mean().reset_index()

fig = px.scatter_matrix(groupedscat, dimensions=["total_cases", "new_cases", "hosp_patients", "new_vaccinations"], color="continent")
fig.show()
