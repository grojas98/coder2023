# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 19:37:52 2023

@author: groja
"""

## IMPORTAR LIBRERÍAS

import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
%matplotlib qt
mpl.style.use('bmh')

#dataset escogido: VENTA VIDEOJUEGOS AÑO 2019 (vgsales-12-4-2019.csv)
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

# This is a pure scrape from the vgzcharts website. 
# My guess is that Global Sales is the sum of all Sales while 
# Total Shipped is when there are values missing in the sales columns. (Global Sales = Total Shipped) fuente: creador del dataset


#leer dataset
file = pd.read_csv('vgsales-12-4-2019.csv')
#unir columnas iguales, total_shipped son las ventas cuando faltan datos según el creador del dataset.
#rellenar valores nan para el uso de una nueva columna de Global_Sales_Real
file['Global_Sales'] = file['Global_Sales'].fillna(0)
file['Total_Shipped'] = file['Total_Shipped'].fillna(0)
file['Global_Sales_Real'] = file['Global_Sales']+file['Total_Shipped']

#%% GRÁFICOS MATPLOTLIB

# ver relación entre ventas globales y la calificación del usuario

fig, ax = plt.subplots(figsize = (25,15))
# (x,y)
ax.scatter(file['User_Score'],file['Global_Sales_Real'])
ax.set_title('Ventas Globales vs. Calificación de usuario (1-10)')
ax.set_ylabel('Ventas Globales (millones)')
ax.set_xlabel('Calificación de usuario')
fig.show()


# ver relación entre ventas globales según el género del juego

#agrupar género y sumar ventas globales
file_genre = file.groupby(['Genre'])['Global_Sales_Real'].sum()
file_genre = file_genre.reset_index()

fig, ax = plt.subplots(figsize = (25,15))
ax.bar(file_genre['Genre'], file_genre['Global_Sales_Real'])
ax.set_title('Ventas Globales según genero del juego (millones)')
ax.set_xlabel('Género')
ax.set_ylabel('Ventas Globales')
fig.show()


# ver relación la frecuencia de juegos según el género

fig, ax = plt.subplots(figsize = (25,15))
ax.hist(file['Genre'].values.flatten(),bins=len(file['Genre'].value_counts()))
ax.set_title('Histograma Género del juego')
ax.set_xlabel('Género')
ax.set_ylabel('Frecuencia absoluta')
fig.show()


## SCATTER PLOT (ventas globales vs clasificación usuario): se observa que no importa mucho la calificación del juego
# en relación a las ventas globales, debido a que se concentran los puntos
# dentro de la calificacón de usuario desde 7 a 10, lo cual es una clasificación
# alta, en donde se tienen de 0 a 4 millones de ventas, con algunas excepciones
# que concuerdan con clasificación alta y alto nivel de ventas y, análogamente,
# con clasificación baja y bajo nivel de ventas.

## BAR PLOT (ventas globales según género de juego): se observa que los juegos
# con mayor número de ventas son los juegos de , seguido por acción (Action)
# los juego de deportes (Sport), y los juegos con el menor número de ventas son
# los juegos de mesa (Board Game), de educación (Education) y de novelas visuales
# (Visual Novel).

## HISTOGRAMA (frecuencia de juegos en el dataset según genero): Para corroborar
# el barplot, se observa que la frecuencia de algunos juegos son bajas, por
# ejemplo los de juegos de mesa se observa que una muy pequeña cantidad están
# ingresados al dataset, por lo que se ve reflejado en la menor cantidad de ventas
# al igual con educación. Se puede interpretar que los juegos de deporte (Sport)
# si son bien vendidos debido a que no es el género de juego más ingresado al
# dataset.

#%% GRÁFICOS SEABORN

# settear estilo seaborn
sns.set_style(style="darkgrid", rc={"grid.color": ".6"})
sns.set_style(rc={"grid.linestyle": ":"})
sns.set_style(rc={"axes.titleweight": "normal"})
sns.set_style(rc={"axes.titlelocation": "left"})
sns.set_style(rc={"axes.titlecolor": "blue"})
sns.set_style(rc={"axes.labelcolor": "red"})
sns.set_style(rc={"axes.labelsize": "12"})
sns.set_style(rc={"axes.labelweight": "normal"})
sns.set_style(rc={"axes.linewidth": "0.5"})
sns.set_style(rc={"grid.color": "purple"})
sns.set_style(rc={"grid.linestyle": "--"})
sns.set_style(rc={"grid.linewidth": "0.5"})
sns.set_style(rc={"font.fantasy": "Comic Sans MS"})
sns.set_style(rc={"font.serif": "Utopia"})

file_line = file[['Rank','Global_Sales_Real']]
file_line = file_line.set_index('Rank')


#Ventas Globales vs Rank

plt.figure(figsize=(10,6))
sns.lineplot(data=file_line)
plt.ylabel('Ventas Globales')
plt.xlabel('Rank')
plt.title('Rank vs Ventas Globales')
plt.legend(bbox_to_anchor=(1, 1), loc='upper left')
plt.show()

# considerando que son los más vendidos e ingresados al dataset, separemos en género de Acción y Deportes.

file_games = file.loc[(file['Genre'] == 'Sports') | (file['Genre'] == 'Action')]

# boxplot para género = deportes y para género = acción

plt.figure(figsize=(10,6))
plt.title('Boxplot Género / Rank (Acción vs Deportes)')
ax = sns.boxplot(x="Genre", y="Rank", data=file_games)
plt.show()


# scatter plot con coLores Ventas globales vs clasificación de usuario

plt.figure(figsize=(10,6))
sns.scatterplot(data=file, x="User_Score", y="Global_Sales_Real", hue="Genre")
plt.legend(bbox_to_anchor=(1, 1), loc='best')
plt.ylabel('Ventas Globales (millones)')
plt.xlabel('Calificación de usuario')
plt.show()


# LINEPLOT (Ventas Globales vs Rank): Se observa que a medida que baja el rank del juego,
# va bajando su número de ventas y, curiosamente, se parece mucho a una gráfica de |1/x| para
# x>0

# BOXPLOT (Género/Rank): se ve que la mediana o segundo cuartil se encuentra para los juegos
# de deportes en Rank 20.000 aprox., con el 25% de los datos bajo 10.000 aprox. (primer cuartil) y el 
# 75% de los datos bajo 40.000 aprox. (tercer cuartil). Para los juegos de acción, la mediana se 
# encuentra aprox en un Rank 25.000, con el 25% de los datos bajo 12.000 aprox. y el 75% de los datos
# bajo 42.000 aprox.

# datos boxplot:
# deportes:
Q1_S = np.percentile(file_games.loc[file_games['Genre'] == 'Sports']['Rank'], 25)
Q2_S = np.percentile(file_games.loc[file_games['Genre'] == 'Sports']['Rank'], 50)
Q3_S = np.percentile(file_games.loc[file_games['Genre'] == 'Sports']['Rank'], 75)
Q1_S
Q2_S
Q3_S
# Acción:
Q1_A = np.percentile(file_games.loc[file_games['Genre'] == 'Action']['Rank'], 25)
Q2_A = np.percentile(file_games.loc[file_games['Genre'] == 'Action']['Rank'], 50)
Q3_A = np.percentile(file_games.loc[file_games['Genre'] == 'Action']['Rank'], 75)
Q1_A
Q2_A
Q3_A

## SCATTERPLOT (Ventas globales vs clasificación de usuario, con colores basado en el género del juego):
# misma conclusión que ocupando matplotlib sin colores, pero se observa que con colores basado en el
# género del juego, los juegos de deportes (Sports) y carreras (Racing), se encuentran con los números
# más altos en ventas.












