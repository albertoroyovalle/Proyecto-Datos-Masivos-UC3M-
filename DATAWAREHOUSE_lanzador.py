"""
Datawarehouse.

Este pequeño codigo se encargaría cada x tiempo de actualizar nuestras tablas csv de Aena.

Para ello se hará una llamada al ETL/función getDESTINOS ...

getDESTINOS es la ETL relacionada con la fuente aena:
    entradas: 
    "w" o "r"  ("w" sería para escribir y exportar en nuestro path_output los datos de aena en un archivoCSV)  
                   ("r" para escribir los datos de aena en una variable. Esta funcionalidad no la utilizaremos ya que no trabajaremos en un esquema virtual. 
                    Las llamadas a esta funcion se hacen de vez en cuando)
    path_output (path donde se escribe el archivo csv)

ESTE CODIGO DEBERIA DE FUNCIONAR PERFECT

"""



from ETL_AenaToCSV import getDESTINOS
#from WRAPPER_GetPrecio import getPRECIOS

import requests
from bs4 import BeautifulSoup
import lxml
import re
import pandas as pd
import numpy as np
import os


def main():
    URL="https://www.aena.es/es/adolfo-suarez-madrid-barajas/aerolineas-y-destinos/destinos-aeropuerto.html"
    path_output="/home/proyectodatos/Desktop/Codigos_Datos_Masivos/Codigos"
    data=getDESTINOS( "w", path_output)
    #da_prices=getPRECIOS(Datos,"w",path_output)
  

if __name__ == "__main__":
    main()
