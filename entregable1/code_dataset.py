# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 15:16:46 2023

@author: groja
"""

# importar librerias

import pandas as pd
import numpy as np

# leer datasets

dataset_covid = pd.read_csv("all-states-history.csv")
dataset_game_sales = pd.read_csv("vgsales-12-4-2019.csv")
dataset_accidents = pd.read_csv("US_Accidents_Dec21_updated.csv")

#%% COVID

tamaño_dataset_covid = dataset_covid.shape

print('Tamaño dataset COVID: ' + str(tamaño_dataset_covid[0]) + ' filas y ' +str(tamaño_dataset_covid[1]) + ' columnas\n')

# variables potencialmente interesantes dataset covid

# filtrar únicamente datos más recientes (última data a hasta 7 de marzo 2021), obtener únicamente datos del 2021

dataset_covid_v2 = dataset_covid.loc[dataset_covid['date'] >= '2021-01-01']

# obtener muertes confirmadas en ese año
# deathConfirmed: COVID-19 como causa confirmada de muerte
# deathProbable: COVID-19 como causa probable de muerte
# death: deathConfirmed + deathProbable

muertes = dataset_covid_v2['deathConfirmed'].sum()
print("El año 2021 hasta el 7 de marzo hubieron " + str(int(muertes)) + " muertes confirmadas debido a la enfermedad COVID-19 en USA")

# obtener columnas relevantes para visualizar muertes

dataset_covid_v3 = dataset_covid_v2[['date','state','death','deathConfirmed','deathIncrease','deathProbable','recovered']]

# localizar dia y estado en el que hubo más muertes hasta dicha fecha

dataset_covid_v4 = dataset_covid_v3[['date','state','deathConfirmed']].loc[
    dataset_covid_v3['deathConfirmed'] == dataset_covid_v3['deathConfirmed'].max()]
dataset_covid_v4 = dataset_covid_v4.reset_index()

print('\nEl día ' + str(dataset_covid_v4['date'][0]) + ' en el estado de ' + str(dataset_covid_v4['state'][0]) + ' hubieron ' + str(int(dataset_covid_v4['deathConfirmed'][0])) + ' muertes confirmadas, siendo el mayor número hasta la fecha (7 de marzo 2021)')

# localizar dias y estados en donde hubo muertes confirmadas que superaron los 10000

dataset_covid_v5 = dataset_covid_v3[['date','state','deathConfirmed']].loc[
    dataset_covid_v3['deathConfirmed'] > 10000]

# rellenar valores nan por 0 en columnas que no tienen info

dataset_covid_v6 = dataset_covid_v3.fillna(0)

#%% VENTA VIDEOJUEGOS

tamaño_dataset_games = dataset_game_sales.shape

print('Tamaño dataset GAME SALES: ' + str(tamaño_dataset_games[0]) + ' filas y ' +str(tamaño_dataset_games[1]) + ' columnas\n')

# agrupar por cada publisher, cuantos juegos contiene el dataset

published = dataset_game_sales.groupby(['Publisher']).size().reset_index(name='cantidad de juegos en el dataset')

#otra forma:

published2 = dataset_game_sales.groupby(['Publisher'])['Name'].count().reset_index(name='cantidad de juegos en el dataset')

#otra forma2:

published3 = dataset_game_sales['Publisher'].value_counts().reset_index(name='cantidad de juegos en el dataset')

# ver que publisher tiene más de 100 juegos

published_v2 = published.loc[published['cantidad de juegos en el dataset'] > 100]
published_v2 = published_v2.sort_values(by='cantidad de juegos en el dataset',ascending=False).reset_index(drop=True)

# top 5

published_top = published_v2.head().set_index('Publisher')

# se observa que frecuentemente no se conoce el nombre del publisher, siendo este el top 1, filtrandolo quedaria:
    
published_v3 = published_v2.loc[published_v2['Publisher'] != 'Unknown']

# top 5

published_top2 = published_v3.head().set_index('Publisher')
print('El publisher con más juegos es ' + str(published_top2.reset_index()['Publisher'][0]))

# buscar valores de los juegos que más hayan distribuido: Total shipped copies of the game

distribuidos = dataset_game_sales[['Name','Publisher','Total_Shipped']]

# como nos interesan los que contengan valores en esa columna, se eliminaran las columnas con valores 'nan'

distribuidos_v2 = distribuidos.dropna(subset='Total_Shipped')

# top 5

distribuidos_v3 = distribuidos_v2.head().set_index('Name')

print('\nEl juego más distribuido es ' + str(distribuidos_v3.reset_index()['Name'][0]))

# plataformas con más juegos

platforms = dataset_game_sales['Platform'].value_counts().reset_index(name='cantidad de juegos en la plataforma')

print('\nLa plataforma más usada es ' + str(platforms.reset_index()['index'][0]))

#%% ACCIDENTES US

tamaño_dataset_accidentes = dataset_accidents.shape

print('Tamaño dataset ACCIDENTES: ' + str(tamaño_dataset_accidentes[0]) + ' filas y ' +str(tamaño_dataset_accidentes[1]) + ' columnas\n')

severidad = dataset_accidents.groupby(['Severity']).size().reset_index(name='cantidad de accidentes')
nmax_severidad = severidad['Severity'].loc[severidad['cantidad de accidentes'] == severidad['cantidad de accidentes'].max()].reset_index(drop=True)[0]
nmax_accidentes = severidad['cantidad de accidentes'].max()
print('La mayor cantidad de accidentes son de un nivel de severidad ' + str(nmax_severidad) + ' (de un rango de 1 - 4, 4 más severo) con un total de ' + str(nmax_accidentes) + ' accidentes.\n')

state = dataset_accidents.groupby(['State']).size().reset_index(name='cantidad de accidentes')
nmax_state = state['State'].loc[state['cantidad de accidentes'] == state['cantidad de accidentes'].max()].reset_index(drop=True)[0]
nmax_accidentes2 = state['cantidad de accidentes'].max()
print('La mayor cantidad de accidentes son en el estado de ' + str(nmax_state) + ' con un total de ' + str(nmax_accidentes2) + ' accidentes.\n')

city = dataset_accidents.groupby(['City']).size().reset_index(name='cantidad de accidentes')
nmax_city = city['City'].loc[city['cantidad de accidentes'] == city['cantidad de accidentes'].max()].reset_index(drop=True)[0]
nmax_accidentes3 = city['cantidad de accidentes'].max()
print('La mayor cantidad de accidentes son en la ciudad de ' + str(nmax_city) + ' con un total de ' + str(nmax_accidentes3) + ' accidentes.\n')

weather = dataset_accidents.groupby(['Weather_Condition']).size().reset_index(name='cantidad de accidentes')
nmax_weather = weather['Weather_Condition'].loc[weather['cantidad de accidentes'] == weather['cantidad de accidentes'].max()].reset_index(drop=True)[0]
nmax_accidentes4 = weather['cantidad de accidentes'].max()
print('La mayor cantidad de accidentes son con condición climática ' + str(nmax_weather) + ' con un total de ' + str(nmax_accidentes4) + ' accidentes.\n')

#%%

#analisis velocidad del viento vs severidad de accidentes

wind_speed_analysis = dataset_accidents[['Severity','Wind_Speed(mph)']]

wind_speed_analysis = wind_speed_analysis.dropna(subset='Wind_Speed(mph)')
promedio_ws = np.mean(wind_speed_analysis['Wind_Speed(mph)'])

#severidad accidentes con viento por arriba del promedio

wind_speed_analysis_v2 = wind_speed_analysis.loc[wind_speed_analysis['Wind_Speed(mph)'] > promedio_ws]
#severidad más repetida
sv = wind_speed_analysis_v2['Severity'].value_counts().idxmax()
print('Severidad más repetida',sv)
#promedio severidad
promedio_sv = np.mean(wind_speed_analysis_v2['Severity'])
print(promedio_sv)

#severidad accidentes con viento por abajo del promedio

wind_speed_analysis_v3 = wind_speed_analysis.loc[wind_speed_analysis['Wind_Speed(mph)'] <= promedio_ws]
#severidad más repetida
sv = wind_speed_analysis_v3['Severity'].value_counts().idxmax()
print(sv)
#promedio severidad
promedio_sv = np.mean(wind_speed_analysis_v3['Severity'])
print(promedio_sv)

# la severidad más repetida y el promedio no cambian mucho, pero si se ven las demás severidades

# viento por arriba del promedio
sv = wind_speed_analysis_v2['Severity'].value_counts()
# viento por abajo del promedio
sv2 = wind_speed_analysis_v3['Severity'].value_counts()

sv
sv2

#se observa un aumento en la severidad 3 y 1, y una excepción en la severidad 4











