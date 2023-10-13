# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 19:37:38 2023

@author: groja
"""

#importar librerías
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from scipy import stats
%matplotlib qt
#columnas:
# Rank - Ranking of overall sales
# Name - Name of the game
# Platform - Platform of the game (i.e. PC, PS4, XOne, etc.)
# Genre - Genre of the game
# ESRB Rating - ESRB Rating of the game
# Publisher - Publisher of the game
# Developer - Developer of the game
# Critic Score - Critic score of the game from 10
# User Score - Users score the game from 10
# Total Shipped - Total shipped copies of the game
# Global_Sales - Total worldwide sales (in millions)
# NA_Sales - Sales in North America (in millions)
# PAL_Sales - Sales in Europe (in millions)
# JP_Sales - Sales in Japan (in millions)
# Other_Sales - Sales in the rest of the world (in millions)
# Year - Year of release of the game

#leer dataset
file = pd.read_csv('vgsales-12-4-2019.csv')
#unir columnas iguales, total_shipped son las ventas cuando faltan datos según el creador del dataset.
#rellenar valores nan para el uso de una nueva columna de Global_Sales_Real
file['Global_Sales'] = file['Global_Sales'].fillna(0)
file['Total_Shipped'] = file['Total_Shipped'].fillna(0)
file['Global_Sales_Real'] = file['Global_Sales']+file['Total_Shipped']

#abstract: Este dataset contiene datos sobre ventas de juegos según varios parámetros, algunos siendo
# la calificación del usuario, calificación de críticas, información de los publicadores del juego y del juego en sí, etc.
# Se pueden observar algunas relaciones con las ventas realizando algunos análisis con ciencia de datos, observando
# posteriormente algunos gráficos que corroboren los datos obtenidos de los cálculos realizados. Algunos datos del dataset
# aparecen como nulos, lo cual en algunos cálculos fueron considerados en que no darán un resultado real de lo que se quiere
# observar, si no un dato medianamente inclinado dependiendo de la cantidad de nulos que contenga la sección del dataset.
# Por otro lado, algunos datos si contienen información completa, por lo cual no impedirá el cálculo en ese sentido.
# A continuación se verán descritos tanto por texto como por código la obtención de las preguntas de interés correspondientes
# a este dataset.

file_describre = file.describe() #descripción del dataframe

## PREGUNTAS

# A partir de estos datos, puedo saber
# 1. ¿Que género de juego se vende más entre Japón, America del Norte y Europa?
# 2. ¿Como se distribuyen los datos de ventas globales según el género?
# 3. ¿Las críticas de los usuarios afectan las ventas globales, viendolos por género?


#%% 1.

file_ventas = file[['Genre','NA_Sales','PAL_Sales','JP_Sales','Other_Sales']]
nulos = file_ventas[['NA_Sales','PAL_Sales','JP_Sales','Other_Sales']].isnull().sum()
nulos

#Se observa gran cantidad de nulos, por lo que la información puede estar inclinada a la información existente

file_ventas_v2 = file_ventas.groupby('Genre').sum().reset_index()
file_ventas_v2['Total'] = file_ventas_v2[['NA_Sales', 'PAL_Sales', 'JP_Sales','Other_Sales']].sum(axis=1)
file_ventas_v2['Promedio'] = file_ventas_v2[['NA_Sales', 'PAL_Sales', 'JP_Sales','Other_Sales']].mean(axis=1)

print('El género más vendido entre Japón, America del Norte y Europa (añadiendo otras partes del mundo también) es '
      + str(file_ventas_v2['Genre'].loc[file_ventas_v2['Total'] == file_ventas_v2['Total'].max()].values[0]) + 'con '
      + str(int(file_ventas_v2['Total'].max().round())) + ' millones de ventas ' + 'y un promedio de '
      + str(int(file_ventas_v2['Promedio'].max().round())) + ' millones de ventas.')


file_ventas_v3 = file_ventas_v2.melt(id_vars=['Genre'], var_name='Type', value_name='Sales')

# Gráfico con la información de ventas por cada lugar, separado por el género del juego
plt.figure()
sns.barplot(data=file_ventas_v3,x='Genre',y='Sales',hue='Type')

#%% 2.

file_ventas_globales = file[['Genre','Global_Sales_Real']]
nulos_ventas_globales = file_ventas_globales[['Global_Sales_Real']].isnull().sum()
nulos_ventas_globales

# Se observan que no hay nulos, por lo que los datos son más verídicos

file_ventas_globales_v2 = file_ventas_globales.groupby('Genre').sum().reset_index()

plt.figure()
sns.barplot(data=file_ventas_globales_v2,x='Genre',y='Global_Sales_Real')


# Se observa un cambio con lo observado anteriormente, ahora el género "Action" es el más vendido, esto es debido a la
# menor cantidad de nulos, lo cual es significativamente menor.


#%%

file_criticas_ventas = file[['Genre','User_Score','Global_Sales_Real']]

plt.figure()
sns.scatterplot(data=file_criticas_ventas, x="User_Score", y="Global_Sales_Real",hue='Genre')


# Se observa que la calificación del usuario no afecta mucho a las ventas en este dataset, debido a que un alto
# número de calificación, no obtiene necesariamente gran número de ventas























