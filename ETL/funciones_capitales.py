from bs4 import BeautifulSoup
import requests
import lxml
import re
import pandas as pd
import numpy as np


def getCapitales(path_output):
    #path_output="/home/vant/Documentos/Master/DatosMasivos/Scripts"
    URL='https://es.wikipedia.org/wiki/Anexo:Ciudades_de_la_Uni%C3%B3n_Europea_por_poblaci%C3%B3n'
    r = requests.get(URL)    #Make a request to a web page
    soup = BeautifulSoup(r.text, 'lxml')


    tr=soup.find_all("b")

    capitales=[]
    for i in range(len(tr)):
        capitales.append(tr[i].text)

    capitales.pop(0)
    a=np.arange(24,len(capitales),1)
    for i in a: 
        capitales.pop(24)
    for i in range(len(capitales)):
        capitales[i]=capitales[i].replace('á','a').replace('é','e').replace('í','i').replace('ó','o').replace('ú','u').upper()

    Destinos={'Destinos':capitales}
    CapitalesDataframe=pd.DataFrame(data=Destinos)
    CapitalesDataframe.to_csv(path_output+"/Capitales.csv")


def setCapitales(Aena,Capitales,path_output):
    ReadDestinos=pd.read_csv(path_output+Aena, header=None, names=['Destinos','Iniciales'])
    ReadCapitales=pd.read_csv(path_output+Capitales, header=None, names=['Destinos'])
    index=[]
    for i,D in enumerate(ReadCapitales['Destinos']):
        for j,Aena in enumerate(ReadDestinos['Destinos']):
            if Aena.startswith(D):
                index.append(j-1)    

    index.pop(0)
    CapitalFinal=[]
    AeropuertoFinal=[]

    for i in index:
        CapitalFinal.append(ReadDestinos['Destinos'][i])
        AeropuertoFinal.append(ReadDestinos['Iniciales'][i])



    datos={'Destino':CapitalFinal,'Aeropuerto':AeropuertoFinal}
    DATAFRAME=pd.DataFrame(data=datos)
    DATAFRAME.to_csv(path_output+"/CAPITALESdeAENA.csv")
