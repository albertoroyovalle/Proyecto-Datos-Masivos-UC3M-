from bs4 import BeautifulSoup
import requests
import lxml
import re
import pandas as pd
import numpy as np
from funciones_capitales import getCapitales, setCapitales 


path_output="/home/proyectodatos/Desktop/Codigos_Datos_Masivos/Codigos/CSVs"
Aena='/DestinosAena.csv'
Capitales='/Capitales.csv'


getCapitales(path_output)
setCapitales(Aena,Capitales,path_output) 
