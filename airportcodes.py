import requests
from bs4 import BeautifulSoup
import lxml
import re
def getAIRPORTs( URL, headers ):
    r = requests.get(URL, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    airports = soup.find("tbody").find_all(lambda tag: tag.name == 'tr' and 
                                           (tag.get('class') == ['light-row'] or 
                                            tag.get('class') == ['dark-row']))
    lista = []
    for airport in airports:
        name = airport.find("th").text
        name = re.sub("\n","",name)
        
        columnas = airport.find_all("td")
        tipo = columnas[0].text
        tipo = re.sub("\\nType:|\\n","",tipo)
        tipo = tipo.lstrip()
        tipo = tipo.rstrip()
        
        ciudad = columnas[1].text
        ciudad = re.sub("City: ","",ciudad)
        
        pais = columnas[2].text
        pais = re.sub("Country: ","",pais)
        
        iata = columnas[3].text
        iata = re.sub("IATA: ","",iata)
        
        icao = columnas[4].text
        icao = re.sub("ICAO: ","",icao)
        
        faa = columnas[5].text
        faa = re.sub("FAA: ","",faa)
        info = [name,tipo,ciudad,pais,iata,icao,faa]
        lista.append(info)
        #print(info)
    return lista

def getHTREFs(URL,headers):
    r = requests.get(URL,headers=headers)
    soup = BeautifulSoup(r.content,"html.parser")
    hrefs = soup.find("tbody").find_all('a', href=True)
    for a in hrefs:
        print(a['href'])

def getLOCs(URL,headers):
    r = requests.get(url,headers=headers)
    #soup = BeautifulSoup(r.content,"html.parser")
    soup = BeautifulSoup(r.text,"lxml")
    algo = soup.find_all("div", {"class": "small-12 columns background-grey",
                                 "class": "small-12 columns",
                                 "class": "airport-basic-data large-6 medium-6 columns"})
    cadena = algo[0].text
    lat1 = cadena.index('Latitude') 
    lat2 = cadena.index('Longitude') 
    lon1 = cadena.index('Longitude') 
    lon2 = cadena.index('Time') 
    latitud = cadena[lat1+8:lat2]
    longitud = cadena[lon1+9:lon2]
    print(latitud,longitud)