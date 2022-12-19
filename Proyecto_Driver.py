import location
from bs4 import BeautifulSoup
import requests
import lxml
import re
import pandas as pd
import numpy as np


from WRAPPER_GetPrecio import getPRECIOS
from mejoresdestinos import MejoresDESTINOS
from FuncionTripadvisor import ScrapperTripadvisor
import warnings
import ipywidgets as widgets
from IPython.display import display
warnings.filterwarnings('ignore')


def step_1():
    """
    1) Lo primero que hace esta función será llamar a la fución 
    de la ubicación e imprimir por pantalla el output de esa función
    sin mostrar la imagen aún
    """
    mapa_Aeropuerto, duracion = location.driver()

    return mapa_Aeropuerto, duracion

def step_2():
    """
    2) A continuación se mostrarán por pantalla todos los destinos
    Barajas.
    """
    path_output="." 
    ReadCapitales=pd.read_csv('/home/proyectodatos/Desktop/Codigos_Datos_Masivos/Codigos/CSVs/CAPITALESdeAENA.csv')
    ReadCapitales = ReadCapitales.drop(columns='Unnamed: 0')

    print("\nEl aeropuerto seleccionado es Adolfo Suárez Madrid-Barajas (MAD).")

    print(ReadCapitales.head(20))

    """
    3)  Por último se muestran los 5 destinos más baratos con los 
    planes de TripAdvisor 
    """
    destinos_opt = input("\n\n¿Desea ver qué destinos son los más recomendables?: ")
    if destinos_opt.lower() == "si" or destinos_opt.lower() == "sí":
       
        Precios=getPRECIOS(ReadCapitales,"w",path_output)
        LISTA_5Destinos=MejoresDESTINOS(Precios)
        print("\nLos destinos más recomendables son los más baratos.\n\n")
        print(LISTA_5Destinos)

    
    else:
        final_opt = input("¿Desea salir de la aplicación?")
        if  final_opt.lower() == "si" or final_opt.lower() == "sí":
            return

        else:
            pass

    cinco_destinos = LISTA_5Destinos['Recomendaciones'].str.split("/")
    lista_dropdown = [(cinco_destinos[i][0], i) for i in range(len(cinco_destinos))]
    # lista_dropdown = [cinco_destinos[i][0] for i in range(len(cinco_destinos))]
    return lista_dropdown, LISTA_5Destinos['Recomendaciones'].str.replace(" ", "");


def step_3(ciudad, destinos):
    """
    el input es lo que introducimos con el desplegable
    destinos es el data frame de antes
    """

    lista_planes, b, c = ScrapperTripadvisor(destinos[ciudad],5)
    print("Ciudad: ", destinos[ciudad])
    print(b,"\n")
    print(c,"\n")
    print("Lista de planes: \n")
    print(*lista_planes, sep="\n")

    mapa_sitios = location.dibujar_mapa(lista_planes, destinos.str.split("/")[ciudad][0])
    display(mapa_sitios)


    return

def step_4(mapa, duracion):
    print("La ruta hacia el aeropuerto es la siguiente:")
    print(f"Ahora mismo tardaría {duracion}.")
    display(mapa)
    return
