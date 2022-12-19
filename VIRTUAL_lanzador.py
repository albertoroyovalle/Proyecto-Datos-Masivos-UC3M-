"""
VIRTUAL.

Este codigo se encargará de sacar los precios de los vuelos y seleccionar las 5 mejores opciones.
Para ello tomará los datos de la tabla de capitales europeas a las que podemos viajar y hará una busqueda de precios utilizando la función getPRECIOS (wrapper)


Falta: Entrada con las capitales 
Falta: el modulo que elija los 5 mejores vuelos.

getPRECIOS es el WRAPPER relacionado con la fuentes como skyscanner.

    entradas: 
    "w" o "r"  ("w" sería para escribir y exportar en nuestro path_output los datos un archivoCSV)  
                   ("r" para escribir los datos en una variable)
    path_output (path donde se escribe el archivo csv)



"""



from AenaToCSV import getDESTINOS
from GetPrecio import getPRECIOS

import requests
from bs4 import BeautifulSoup
import lxml
import re
import pandas as pd
import numpy as np
import os


def main():
    URL="https://www.aena.es/es/adolfo-suarez-madrid-barajas/aerolineas-y-destinos/destinos-aeropuerto.html"
    path_output="/home/vant/Documentos/Master/DatosMasivos/Scripts/Final"
    
    Destinos=pd.read_csv(path_output+'/DestinosCapitales.csv', header=None, names=['Destinos']) 
    da_prices=getPRECIOS(Destinos,"w",path_output)
  

if __name__ == "__main__":
    main()
