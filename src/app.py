import os
from bs4 import BeautifulSoup
import requests
import time
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Crear los datos de HTML de la pagina web proporcionada
url = "https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue"
#url = 'https://ycharts.com/companies/TSLA/revenues'
data = requests.get(url)

# Comprobar si se extra informacion, en caso contrario acceder de manera anonima
if data.status_code != 200:
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"}
    data = requests.get(url, headers = headers)
    
data_html = data.text

#Filtrar los datos del HTML para obterner unicamente los datos tipo tabla

soup = BeautifulSoup(data_html,"html.parser")
tablas = soup.find_all("table")

#Crear un data frame de la tabal "Tesla Quarterly Revenue"
for i, tabla in enumerate(tablas):
    if 'Tesla Quarterly Revenue' in str(tabla):
    #if 'Date' in str(tabla):
        id = i
        break
print(tablas[id])
#Con la tabla encontrada se realizara el data frame con las ganancias por fechas ademas se modificara su contenido
df= pd.DataFrame(columns = ['Fecha', 'Ganancia'])
for fila in tablas[id].tbody.find_all("tr"):
    colum=fila.find_all('td')
    if colum!=[]:
        Fecha=colum[0].text
        Ganancia=colum[1].text.replace("$", "").replace(",", "")
        df=pd.concat([df, pd.DataFrame({"Fecha": Fecha,"Ganancia": Ganancia}, index = [0])], ignore_index = True)

print(df)
