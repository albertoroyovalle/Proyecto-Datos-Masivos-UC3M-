import requests
import folium



def localizacion(key):
    """Te devuelve la latitud y la longitud de tu ubicación actual"""
    URL = 'https://www.googleapis.com/geolocation/v1/geolocate?key='+key

    # te devuelve un diccionario donde está almacenada la ubicación
    ubicacion = requests.post(URL).json()
    return [ubicacion['location']['lat'], ubicacion['location']['lng']]

def buscar_aeropuerto(key,lat,long):
    """
    Te permite buscar el aeropuerto más cercano. Hace una busqueda con la api de google
    llevada por la ubicación que tu le des. Luego te saca información de ese sitio con 
    otra api de google
    """
    URL = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?'
    params = {
        'key':key,
        'locationbias':'circle:2000@'+str(lat)+','+str(long),
        'input': "aeropuerto",
        'inputtype':"textquery"
    }
    id_aeropuerto = requests.get(URL, params=params).json()
    info_aeropuerto = {}
    # solo nos interesa el id del sitio
    info_aeropuerto['place_id'] = id_aeropuerto['candidates'][0]['place_id']
    # buscamos más información sobre el sitio
    URL_2 = "https://maps.googleapis.com/maps/api/place/details/json?"
    params_2 = {
        'place_id':info_aeropuerto['place_id'],
        'key':key,
        'fields':"name",
        'language':"es"
    }
    details = requests.get(URL_2,params=params_2).json()
    # guardamos el nombre
    info_aeropuerto['name'] = details['result']['name']
    return info_aeropuerto

def direciones(key, origen, destino):
    """Te saca la ruta entre un origen y un destino

    origen: será las coordenadas de nuestra ubicación
    obtenidas con la función localizacion().
    Hay que asegurarse de que el origen son coordenadas sin espacio
    entre ellas.

    destino: al aeropuerto que tenemos que ir obtenido con buscar_aeropuerto(),
    esta función te saca un place_id entonces para destination tenemos que poner
    primero place_id:
    """

    params = {
        'key':key,
        'mode': 'driving',
        'origin': origen,
        'destination': 'place_id:'+destino,
        'language': 'es',
        'units': 'metric'
    }

    URL = 'https://maps.googleapis.com/maps/api/directions/json?'

    return requests.get(URL, params=params)

def folium_map(ruta):
    """
    Te saca un mapa interactivo con la ruta que tienes que realizar.

    El parametro de entrada es el json que saca la función direciones().

    El json contiene entre otras cosas los pasos que tenemos que hacer en la ruta.
    Por cada "decisión que tenemos que tomar se seleciona un punto, es decir llegamos a una intersección y tenemos 
    que ir a la derecha, se genera un punto. Es por eso que en el mapa aparece el tramo de autovia aproximado, porque nos
    tenemos que quedar en esa autovia.

    """

    waypoints = [] #los puntos por los que tenemos que pasar en el camino
    marker_points = [] #los marcadores que queremos representar en el mapa

    if len(ruta['routes'])==0:
        print("No se ha podido encontrar una ruta.")
        return
    else:
        ruta = ruta['routes'][0] #acortamos el json

    # guardamos nuestro origen y destino para poner un marcador
    first_stop = ruta["legs"][0]["start_location"]
    marker_points.append(f'{first_stop["lat"]},{first_stop["lng"]}')
    last_stop = ruta["legs"][-1]["end_location"]
    marker_points.append(f'{last_stop["lat"]},{last_stop["lng"]}')

    # aqui juntamos todos los puntos por los que pasamos
    lista_pasos = ruta['legs'][0]['steps']
    for step in lista_pasos:
        waypoints.append(
            f'{step["end_location"]["lat"]},{step["end_location"]["lng"]}')


    # centramos el mapa en el punto medio entre el inicio y el final
    start = [float(i) for i in marker_points[0].split(",")]
    end = [float(i) for i in marker_points[1].split(",")]
    midpoint_gen = [str((x+y)/2) for x, y in zip(start, end)]

    m = folium.Map(location=midpoint_gen, zoom_start=11, width=800, height=500)

    folium.Marker(marker_points[0].split(","), popup="Tu ubicación").add_to(m)
    folium.Marker(marker_points[1].split(","), popup="Aeropuerto más cercano").add_to(m)

    # pasamos los puntos por los que tenemos que ir, a un formato que entienda la libreria.
    poly = []
    for i in waypoints:
        loc = i.split(",")
        poly.append((float(loc[0]), float(loc[1])))

    folium.PolyLine(poly).add_to(m)
    return m

def calle2ubicacion():
    """
    Te saca la latitud y longitud de la calle que tu le digas.
    """
    BASE_URL = "https://nominatim.openstreetmap.org/search?"
    while True:
        calle = input('Introduce el nombre de tu calle: ')
        params = {
            'street':calle,
            'format':"json"
            }
        response_calle = requests.get(BASE_URL, params=params)
        data = response_calle.json()
        if len(data)==0:
            # no se ha encontrado una dirección
            print("Introduce una calle correcta")
        elif len(data)>1:
            # se ha encontrado más de una dirección.
            print("Parece que hay más de un resultado posible.")
            while True:
                ciudad = input("Introduce la ciudad/municipio en la que estás por favor: ")
                params['city']=ciudad
                response_calle = requests.get(BASE_URL, params=params)
                data = response_calle.json()
                if len(data)==0:
                    # no se ha encontrado una dirección
                    print("Introduce una ciudad correcta")
                else:
                    break
            # se ha acotado la dirección a una ciudad
            break
        else:
            break

    return data[0]['lat'], data[0]['lon'];

def driver():
    API_KEY = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

    while True:
        permiso_loc = input("Me das acceso a tu ubicación: Si o No: ")
        if permiso_loc.lower()=="si":
            lat, long = localizacion(API_KEY)
            break
        elif permiso_loc.lower()=="no":
            lat, long = calle2ubicacion()
            break
        else:
            print("Introduce una sentencia correcta. Si o No.")
    
    aeropuerto = buscar_aeropuerto(API_KEY,lat,long)
    origen = str(lat)+','+str(long) #hay que poner la ubicación en este formato
    barajas_place_id = "ChIJAQAAANAxQg0R786FD-old24"
    
    URL = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?'
    params = {
        'key':API_KEY,
        'locationbias':'circle:2000@'+str(lat)+','+str(long),
        'input': "aeropuerto barajas",
        'inputtype':"textquery"
    }
    id_aeropuerto = requests.get(URL, params=params).json()
    barajas_place_id = id_aeropuerto['candidates'][0]['place_id']
    
    

    if aeropuerto['place_id'] != barajas_place_id:
        print(f"Tu aeropuerto más cercano es {aeropuerto['name']}. Lamentablemente todavía no trabajamos con este aeropuerto.")

        while True:
            llevar_a_barajas = input("¿Quiere que le llevemos al aeropuerto disponible más cercano?: ")

            if llevar_a_barajas.lower() == "si":
                ruta = direciones(API_KEY,origen,barajas_place_id).json()
                distancia = ruta['routes'][0]['legs'][0]['distance']['text']
                duracion = ruta['routes'][0]['legs'][0]['duration']['text']
                direcion_final = ruta['routes'][0]['legs'][0]['end_address'].split(",")
                print(f"El {direcion_final[0]} se encuentra a una distancia de {distancia}.\n")
                #print(f"Actualmente tardaría {duracion} en llegar.")
                mapa = folium_map(ruta)
                return mapa, duracion

            elif llevar_a_barajas.lower()=="no":
                print("Sentimos no tener su aeropuerto. Lo añadiremos en el futuro.\n Gracias por utilizar nustros servicios.")
                return 0, 0
            
            else:
                print("Introduce una sentencia correcta.")

    else:
        ruta = direciones(API_KEY, origen, aeropuerto['place_id']).json()
        distancia = ruta['routes'][0]['legs'][0]['distance']['text']
        duracion = ruta['routes'][0]['legs'][0]['duration']['text']
        direcion_final = ruta['routes'][0]['legs'][0]['end_address'].split(",")
        print(f"El {direcion_final[0]} se encuentra a una distancia de {distancia}.")
        #print(f"Actualmente tardaría {duracion} en llegar.")
        mapa = folium_map(ruta)
        return mapa, duracion

def dibujar_mapa(lista_sitios, ciudad):
    """
    Te pilla una lista de sitios y te los dibuja en el mapa.
    """
    API_KEY = 'AIzaSyBd6IZ1uDzuhk4ppC-793RX_EyHoAwpsM4'
    BASE_URL = "https://nominatim.openstreetmap.org/search?"
    URL = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?"
    cantidad_sitios = len(lista_sitios)

    # sacamos las coordenadas de la ciudad
    params = {'format': "json", 'city': ciudad}
    response_ciudad = requests.get(BASE_URL, params=params)
    data = response_ciudad.json()
    latitud_ciudad = data[0]['lat']
    long_ciudad = data[0]['lon']


    # ahora buscamos los sitios
    params = {
        'key': API_KEY,
        'inputtype': "textquery",
        'fields': "geometry",
        'language': "es",
        'locationbias': 'circle:7000@'+str(latitud_ciudad)+','+str(long_ciudad),
    }

    coordenadas_sitios = []
    sitios_correctos = [] #se almacenan solo los sitios que si que aportan una buena salida
    for id, elemento in enumerate(lista_sitios):
        params['input'] = elemento
        sitio = requests.get(URL, params=params).json()
        if sitio['status'] == 'OK':
            location = sitio['candidates'][0]['geometry']['location']
            coordenadas_sitios.append(
                (location['lat'], location['lng']))
            sitios_correctos.append(id)
        else:
            continue
        

    # definimos el punto medio del mapa
    latitudes = [float(coord[0]) for coord in coordenadas_sitios]
    longitudes = [float(coord[1]) for coord in coordenadas_sitios]


    punto_medio = (sum(latitudes)/len(latitudes),
                   sum(longitudes)/len(longitudes))

    mapa = folium.Map(location=punto_medio, zoom_start=13.5, width=800, height=500)

    for id, coord in enumerate(coordenadas_sitios):
        folium.Marker(coord,
                      popup=lista_sitios[sitios_correctos[id]].capitalize()).add_to(mapa)

    return mapa

def main():
    sitios = ["museo del prado", "puerta de alcalá", "estadio santiago bernabeu"]
    dibujar_mapa(sitios, "Madrid")

if __name__ == "__main__":
    main()
