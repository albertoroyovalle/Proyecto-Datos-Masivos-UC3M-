import pandas as pd
import numpy as np

def MejoresDESTINOS(Precio,Numero_Destinos=5):
    #Orden creciente
    orden=np.argsort(Precio['Precio más barato'])
    Precio['Destino'][1]
    ###Inicializo arrays
    Recommendation=[]
    Prices=[]
    Dates=[]
    Airport=[]
    #Escribo los 5 mas baratos
    for i,index in enumerate(orden):
        Recommendation.append(Precio['Destino'][index])
        Prices.append(Precio['Precio más barato'][index])
        Dates.append(Precio['Fechas'][index])
        Airport.append(Precio['Aeropuerto'][index])
        if i==Numero_Destinos:
            break
    #Cargo los datos en un dataframe pandas
    datos={'Recomendaciones':Recommendation,'Aeropuertos':Airport,'Precios':Prices,'Fechas':Dates}
    DATAFRAME_MEJORES_DESTINOS=pd.DataFrame(data=datos)
    return(DATAFRAME_MEJORES_DESTINOS)