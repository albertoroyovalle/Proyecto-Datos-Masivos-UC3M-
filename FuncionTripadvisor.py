import requests
import os 
from bs4 import BeautifulSoup
import lxml
import re
import pandas as pd
import numpy as np
import time

def ScrapperTripadvisor(ciudades,numero_de_planes):
    capitales={ "BERLIN-BRANDERBURG WILLY BRANDT ": "https://www.tripadvisor.es/Tourism-g187323-Berlin-Vacations.html",
    "ROMA/FIUMICINO" : "https://www.tripadvisor.es/Tourism-g187791-Rome_Lazio-Vacations.html" ,
    "PARIS/BEAUVAIS-TILLE": "https://www.tripadvisor.es/Tourism-g187147-Paris_Ile_de_France-Vacations.html" ,
    "PARIS/CHARLES DE GAULLE": "https://www.tripadvisor.es/Tourism-g187147-Paris_Ile_de_France-Vacations.html" ,
    "PARIS/ORLY": "https://www.tripadvisor.es/Tourism-g187147-Paris_Ile_de_France-Vacations.html" ,
    "BUCAREST": "https://www.tripadvisor.es/Tourism-g294458-Bucharest-Vacations.html" ,
    "VIENA": "https://www.tripadvisor.es/Tourism-g190454-Vienna-Vacations.html" ,
    "VARSOVIA": "https://www.tripadvisor.es/Tourism-g274856-Warsaw_Mazovia_Province_Central_Poland-Vacations.html"  ,
    "VARSOVIA/MODLIN": "https://www.tripadvisor.es/Tourism-g274856-Warsaw_Mazovia_Province_Central_Poland-Vacations.html" ,
    "BUDAPEST": "https://www.tripadvisor.es/Tourism-g274887-Budapest_Central_Hungary-Vacations.html" ,
    "PRAGA": "https://www.tripadvisor.es/Tourism-g274707-Prague_Bohemia-Vacations.html" ,
    "SOFIA": "https://www.tripadvisor.es/Tourism-g294452-Sofia_Sofia_Region-Vacations.html" ,
    "BRUSELAS": "https://www.tripadvisor.es/Tourism-g188644-Brussels-Vacations.html" ,
    "BRUSELAS/CHARLEROI": "https://www.tripadvisor.es/Tourism-g188644-Brussels-Vacations.html" ,
    "ESTOCOLMO/ARLANDA" : "https://www.tripadvisor.es/Tourism-g189852-Stockholm-Vacations.html" ,
    "ATENAS": "https://www.tripadvisor.es/Tourism-g189400-Athens_Attica-Vacations.html" , 
    "HELSINKI": "https://www.tripadvisor.es/Tourism-g189934-Helsinki_Uusimaa-Vacations.html" ,
    "RIGA": "https://www.tripadvisor.es/Tourism-g274967-Riga_Riga_Region-Vacations.html" ,
    "COPENHAGUE": "https://www.tripadvisor.es/Tourism-g189541-Copenhagen_Zealand-Vacations.html" ,
    "DUBLIN": "https://www.tripadvisor.es/Tourism-g186605-Dublin_County_Dublin-Vacations.html" ,
    "LISBOA": "https://www.tripadvisor.es/Tourism-g189158-Lisbon_Lisbon_District_Central_Portugal-Vacations.html"}
    URL=capitales[ciudades]
    headers = {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET',
                'Access-Control-Allow-Headers': 'Content-Type',
                'accept': '*/*',
                'accept-encoding': 'gzip, deflate',
                'accept-language': 'en,mr;q=0.9',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'}

    #Modulo de descripcion:

    try:
        r = requests.get(URL,headers=headers,timeout=5,verify=False)
        soup = BeautifulSoup(r.text, 'lxml')
        descripcion = soup.find("div",{"class":"WFLYV"})
        titulo=soup.find("div",{"class":"biGQs _P fiohW mowmC EVnyE"})
        texto=soup.find("div",{"class":"GYFPJ wESPJ _J B- G- Wh _S"})
        titulo=titulo.text
        texto=texto.text
    except:
        titulo="No hay titulo"
        texto="No hay descripcion"
            
    
    #Modulo de planes
    r = requests.get(URL,headers=headers,timeout=5,verify=False)
    soup = BeautifulSoup(r.text, 'lxml')
    planes = soup.find_all("div",{"class":"keSJi FGwzt ukgoS"})
    lista_planes=[]
    
    for i in range(numero_de_planes):
    	lista_planes.append(planes[i].text)
                 
    return lista_planes,titulo,texto
