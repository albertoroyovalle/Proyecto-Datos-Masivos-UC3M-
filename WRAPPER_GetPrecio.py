import requests
from pprint import pprint
import pandas as pd
import numpy as np

url = "https://travelpayouts-travelpayouts-flight-data-v1.p.rapidapi.com/v2/prices/month-matrix"



def getPRECIOS(Datos,w,path_output):

    PrecioBarato=[]
    FechaVuelos=[]

    #Bucle de la muerte. Saca los precios mas baratos de los vuelos de aqui a un mes. REPASAR LO DE LA FECHA... Necesita la fecha de hoy, deberia de ser una fecha introducida por el usuario...
    for i in range(len(Datos['Aeropuerto'])):
        destino=Datos['Aeropuerto'][i]
        origen="MAD"
        fecha="2023-01-25" #formato yyyy-mm para ver el mas baratos del mes o yyyy-mm-dd para ver el mas barato de un dia
        divisa="EUR"

        querystring = {"origin":origen,"destination":destino,"month":fecha,"currency":divisa}

        headers = {
            "X-Access-Token": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "X-RapidAPI-Key": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "X-RapidAPI-Host": "travelpayouts-travelpayouts-flight-data-v1.p.rapidapi.com"
        }

        try:
            response = requests.request("GET", url, headers=headers, params=querystring)

            datos=response.json()['data']
            PrecioBarato.append(datos[0].get('value'))
            FechaVuelos.append(datos[0].get('depart_date'))
            #print("Vuelo a:",destino," a un precio de ",PrecioBarato[i]," con fecha de: ", FechaVuelos[i])  

        except Exception:
            print("No flights")
            PrecioBarato.append("No Flights")
            FechaVuelos.append("No Flights")
            continue
    #Creamos la tabla con los datos antiguos de destinos y datos nuevos de precios y fechas
    FinalDataframe=Datos
    FinalDataframe['Precio más barato']=PrecioBarato
    FinalDataframe['Fechas']= FechaVuelos
    if w=="w":
        FinalDataframe.to_csv(path_output+"/AENAmasPRECIOS.csv")

    return(FinalDataframe)


