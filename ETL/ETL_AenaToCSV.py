"""" 
Funcion la cual tiene como objetivo:

     la extracción de informacion via scrapper de la pagina web de AENA. 
     Transformación de datos a un formato comodo y a CSV

Entradas: 
        URL "https://www.aena.es/es/adolfo-suarez-madrid-barajas/aerolineas-y-destinos/destinos-aeropuerto.html"
        path_output: string con la dirección de tu directorio de trabajo
        w="w" si quieres exportar 

Salidas: pandas dataframe y/o csv en tu directorio de trabajo

"""




import requests
import os 
from bs4 import BeautifulSoup
import lxml
import re
import pandas as pd
import numpy as np
#FUNCIONES:
def getDESTINOS(w,path_output):
    URL= "https://www.aena.es/es/adolfo-suarez-madrid-barajas/aerolineas-y-destinos/destinos-aeropuerto.html"
    r = requests.get(URL)    #Make a request to a web page
    soup = BeautifulSoup(r.text, 'lxml')
    destinos = soup.find_all("span", {"class": "title bold"})  #This thing is just bs4.element.ResultSet with n element like: <span class="title bold">A CORUÑA (LCG)</span>
    
    
    #I want to transform the n element stuff of bs4  <span class="title bold">A CORUÑA (LCG)</span> into n element list of "A CORUÑA (LGC)"
    destino=[]
    for i in destinos:
        destino.append(str(i.text))   #For obtaining a list of strings 
        
    bsoup_destinos=destino #Renombro 
    #bsoup_destinos tiene el formato de "Ciudad+Iniciales". Es decir, tenemos un array del estilo ("Madrid (MAD)","London Gatwick (LGW)" ...)
    #Por temas de la vida nos interesa tener en un array los nombres de los sitios y en otra las iniciales (iniciales sirven como entrada a otro programa )
    
    
    
    NombreDestino=np.empty(len(bsoup_destinos),dtype=object)
    InicialDestino=np.empty(len(bsoup_destinos),dtype=object)
    #Bucle que transforma nuesta salida del scrapper a dos arrays. Uno con el nombre de la ciudad y otro con sus iniciales
    for i,Destinos in enumerate(bsoup_destinos):
        tempvar=Destinos.split("(")
        NombreDestino[i]=(tempvar[0])
        InicialDestino[i]=(tempvar[1].replace(")",""))

    datos={"Destinos":NombreDestino,"Iniciales":InicialDestino}
    FinalDataframe=pd.DataFrame(data=datos)
    if w=="w":
        FinalDataframe.to_csv(path_output+"/DestinosAena.csv")
        print("CSV exportado a tu carpeta de trabajo actual")
    return(FinalDataframe)
