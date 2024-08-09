import os
from bs4 import BeautifulSoup
import requests
import time
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Crear los datos de HTML de la pagina web proporcionada
url = 'https://ycharts.com/companies/TSLA/revenues'
data = requests.get(url)

# Comprobar si se extra informacion, en caso contrario acceder de manera anonima
if data.status_code != 200:
    headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
    data = requests.get(url, headers = headers)
    
data_html = data.text

#Filtrar los datos del HTML para obterner unicamente los datos tipo tabla

soup = BeautifulSoup(data_html,"html.parser")
tablas = soup.find_all("table")

#Crear un data frame de la tabal "Tesla Quarterly Revenue"
df= pd.DataFrame(columns = ['Fecha', 'Ganancia'])
for i, tabla in enumerate(tablas):
    if 'thead' in str(tabla):
        for fila in tablas[i].find_all("tr")[1:]:
            colum=fila.find_all('td')
            Fecha = colum[0].get_text(strip=True)
            Ganancia = int(colum[1].get_text(strip=True).replace('.','').replace('B','000000000').replace('M','000000'))
            df=pd.concat([df, pd.DataFrame({"Fecha": Fecha,"Ganancia": Ganancia}, index = [0])], ignore_index = True)


#Modificacion de la columa de Fecha
df['Fecha'] = pd.to_datetime(df['Fecha']) # Para convertir la columna Date a un objeto datetime.
df['Fecha'] = df['Fecha'].dt.strftime('%d-%m-%Y')

#Realizamos la conexion
'''
connection = sqlite3.connect("Tabla.db")
cursor = connection.cursor()
cursor.execute("""CREATE TABLE Ganancias (Fecha, Ganancias)""")
tuples = list(df.to_records(index = False))
tuples[:5]
cursor.executemany("INSERT INTO Ganancias VALUES (?,?)", tuples)
connection.commit()
'''

#Visualizacion 
grafica_plot = sns.lineplot(data = df, x = "Fecha", y = "Ganancia")
fig = grafica_plot.get_figure()
fig.savefig("grafica_plot.png")

