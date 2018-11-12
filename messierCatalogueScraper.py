# -*- coding: utf-8 -*-
"""
UOC. Máster en Ciencia de Datos

Tipología y Ciclo de vida de Datos

Curso 2018-2019. Práctica 1

@author: Leticia García Ramos & Javier Batuecas Rodríguez
"""

import os
import requests
from bs4 import BeautifulSoup
import csv

#En primer lugar, accedemos a la página índice, de la que obtendremos todos los enlaces a los que debemos entrar
page = requests.get('http://www.messier.seds.org/m/mindex.html')
soup = BeautifulSoup(page.content, "html.parser")

#Creamos una lista vacía en la que cargaremos estos enlaces, que luego usaremos para construir las URLs
#definitivas, concatenándolos con la url raíz
urlFinal = []

#Hacemos uso de un bucle for para acceder a todos los enlaces (href de todos los a)
for link in soup.pre.find_all('a'):
    urlFinal.append(link.get('href'))

#Establecemos la url raíz
URL_RAIZ = "http://www.messier.seds.org/m/"

#Establecemos el directorio de trabajo actual como el que contendrá al archivo generado.
#También ponemos nombre al archivo
currentDir = os.path.dirname(__file__)
filename = "messier_catalogue.csv"
filePath = os.path.join(currentDir, filename)

#Creamos una lista vacía, que será una lista de listas que al final usaremos para escribir en el CSV
messierFinal = []

#La primera lista dentro de esta lista será la de títulos o encabezados de la información
titulos = ["name", "mainInfo", "rightAscension", "declination", "distance", "visualBrightness", "apparentDimension", "link"]

#La añadimos a la lista final como primer elemento
messierFinal.append(titulos)

#De nuevo, bucle for. En cada iteración se construye la url a la que se accede
for i in range(0, len(urlFinal)):
    
    #Se construye la url
    url = "%s%s" % (URL_RAIZ, urlFinal[i])
    
    page = requests.get(url)
    
    statusCode = page.status_code
    #Se comprubea que el status es correcto
    if statusCode == 200:        
        soup = BeautifulSoup(page.content, "html.parser")
        
        #En la etiqueta "center", con formato "h1", tenemos el nombre del objeto Messier
        name = soup.body.center.h1.get_text()
        #Hacemos un tratamiento de los datos para prevenir errores, eliminando comas y saltos de líneas
        name = name.replace(',', ' ').replace('\n', ' ')
        
        #Para la información principal bucamos la etiqueta <i>
        mainInfo = soup.body.center.i.get_text()
        #También hacemos un sencillo tratamiento del texto con el fin de prevenir errores
        mainInfo = mainInfo.replace(';', '.').replace('\n', ' ').replace('"', ' ')
        
        #Por último, extraemos información de la tabla del elemento en cuestión
        tabla = soup.find_all('table')
        
        for i in tabla:
            #La información aparece entre las etiquetas <td>
            valores = i.find_all('td')
            rightAscension = valores[0].find(text=True)
            declination = valores[1].find(text=True)
            distance = valores[2].find(text=True)
            visualBrightness = valores[3].find(text=True)
            apparentDimension = valores[4].find(text=True)
        
        #Construimos una lista con todos los elementos relativos al objeto en el que estamos iterando
        #Eliminamos, con strip, los saltos de línea iniciales y finales de cada cadena, que hemos detectado que
        #se extraen con ese formato
        aux = [name.strip('\n'), mainInfo.replace('\n', ' '), rightAscension.strip('\n'), declination.strip('\n'), distance.strip('\n'), visualBrightness.strip('\n'), apparentDimension.strip('\n'), url]
        
        #Añadimos a la lista final esta lista como siguiente elemento
        messierFinal.append(aux)
        
    #Si el status no fuera correcto, se itera al siguiente valor
    else:
        continue
    
#Para finalizar, usamos la lista creada en messierFinal para crear el fichero CSV
with open(filePath, 'w', newline='') as csvFile:
  writer = csv.writer(csvFile)
  for messierObject in messierFinal:
    writer.writerow(messierObject)
