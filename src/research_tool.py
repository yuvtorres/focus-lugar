# Este modulo contiene las funciones que devuelven un valor entre cero y uno
# según criterios geograficos para 
import math
import json
from pymongo import MongoClient
import apiquery

# distancia entre dos puntos Lat,Log
def f_haversine(point1,point2):
    dlon = point1[1]- point2[1]
    dlat = point1[0]- point2[0]
    a = math.sin (dlat/2)**2 + math.cos(point1[0]) * math.cos(point2[0]) * math.sin(dlon/2)**2
    r= 6.371 *1e6 # earth radio in meters
    return a * r

# Devuelve un valor entre cero y uno dependiendo del criterio de empresas de diseño
def val_design(point):
    
    # Connect and get the data --> coordenates
    url_mongo = "mongodb://localhost:27017"
    client = MongoClient(url_mongo)
    db = client.get_database("companies")
    design=db.design
    # *** El punto es pasado como Lat-Lon y Mongodb recibe a busqueda como Lon-Lat
    query={"design_coor":{"$nearSphere": [point[1], point[0]]}}
    result = list(design.find(query,{"latitude":1,"longitud":1,"_id":0}))

    # no hay empresas de diseño
    if len(result)==0:
        return 0
    
    puntos=[]
    [  puntos.append( ( e['latitude'] , e['longitud'] ) )    for e in result  ]
    
    distancias=[]
    [ distancias.append( f_haversine( point, e ) ) for e in puntos ]
    
    dist_1000 = list(filter( lambda number: number<1000,distancias))

    if min(distancias)>2000:
        return 0
 
    # las empresas que hay estan a mas de 1000 mt
    if len(dist_1000)==0:
        return 0.2

    if min (distancias) < 100:
        return 1

    else:
        return 0.2 +0.8*(1000 - min(distancias))/900

# devuelve un valor entre cero y uno dependiendo del criterio de startups 
# que han recaudado mas de 1 millon de USD

def val_succ(point):
    # Connect and get the data --> coodenates
    url_mongo = "mongodb://localhost:27017"
    client = MongoClient(url_mongo)
    db = client.get_database("companies")
    success=db.success
    query={"success_coor":{"$nearSphere": [point[1], point[0]],"$maxDistance":10000}}
    result = list(success.find(query,{"latitude":1,"longitud":1,"_id":0}))
    
    # no hay startups
    if len(result)==0:
        return 0
    
    puntos=[]
    [  puntos.append( ( e['latitude'] , e['longitud'] ) )    for e in result  ]
    
    distancias=[]
    [ distancias.append( f_haversine( point, e ) ) for e in puntos ]

    if min(distancias)>2000:
        return 0
    
    dist_1000 = list(filter( lambda number: number<1000,distancias))

    # las empresas que hay estan a mas de 1000 mt
    if len(dist_1000)==0:
        return 0.2

    if min (distancias) < 100:
        return 1

    else:
        return 0.2 +0.8*(1000 - min(distancias))/900

# devuelve un valor entre cero y uno dependiendo del criterio de no tener compañias  
# con mas de 10 años em un radio de 2 km

def val_old(point):
    # Connect and get the data --> coodenates
    url_mongo = "mongodb://localhost:27017"
    client = MongoClient(url_mongo)
    db = client.get_database("companies")
    old=db.old
    query={"success_coor":{"$nearSphere": [point[1], point[0]],"$maxDistance":10000}}
    result = list(old.find(query,{"latitude":1,"longitud":1,"_id":0}))
    
    # no hay startups
    if len(result)==0:
        return 1
    
    puntos=[]
    [  puntos.append( ( e['latitude'] , e['longitud'] ) )    for e in result  ]
    
    distancias=[]
    [ distancias.append( f_haversine( point, e ) ) for e in puntos ]

    if min(distancias)>2000:
        return 1
    
    dist_2000 = list(filter( lambda number: number<2000,distancias))
    
    if len(dist_2000)==0:
        return 1
    # las empresas que hay estan a menos de 2000 mt
    return (min(dist_2000))/2000



def val_kindergarden(point):
    lat=point[0]
    lon=point[1]
    radio=2000
    item=("kindergarden","text")
    result=apiquery.importar_api_map(lat,lon,radio,item)

    # no hay guarderias o error en la consulta
    if isinstance(result,int):
        print(f'error en kindergarde, resultado de la consulta :{result}')
        return 0

    if len(result)==0:
        return 0

    puntos=[]
    [  puntos.append( ( e['lat'] , e['lng'] ) )    for e in result  ]
    
    distancias=[]
    [ distancias.append( f_haversine( point, e ) ) for e in puntos ]

    if min(distancias)>3000:
        return 0
    
    dist_3000 = list(filter( lambda number: number<2000,distancias))
    
    if len(dist_3000)==0:
        return 0
    # las empresas que hay estan a menos de 2000 mt
    return (3000 - min(dist_3000))/3000



def val_starbucks(point):
    lat=point[0]
    lon=point[1]
    radio=2000
    item=("starbucks","text")
    result=apiquery.importar_api_map(lat,lon,radio,item)
    # no hay starbucks o error en la consulta
    if isinstance(result,int):
        print(f'error en starbucks, resultado de la consulta :{result}')
        return 0

   # no hay starbucks
    if len(result)==0:
        return 0
    
    puntos=[]
    [  puntos.append( ( e['lat'] , e['lng'] ) )    for e in result  ]
    
    distancias=[]
    [ distancias.append( f_haversine( point, e ) ) for e in puntos ]

    if min(distancias)>550:
        return 0
    
    dist_550 = list(filter( lambda number: number<550,distancias))
    
    if len(dist_550)==0:
        return 0
    # las empresas que hay estan a menos de 2000 mt
    return (550 - min(dist_550))/550


def val_airport(point):
    lat=point[0]
    lon=point[1]
    radio=10000
    item=("airport","type")
    result=apiquery.importar_api_map(lat,lon,radio,item)
    # no hay aeropuertos o error en la consulta
    if isinstance(result,int):
        print(f'error en aeropuerto, resultado de la consulta :{result}')
        return 0

   # no hay aeropuertos 
    if len(result)==0:
        return 0
    
    puntos=[]
    [  puntos.append( ( e['lat'] , e['lng'] ) )    for e in result  ]
    
    distancias=[]
    [ distancias.append( f_haversine( point, e ) ) for e in puntos ]

    # segun lo cerca que quede el aeropuerto
    return (10000 - min(distancias))/10000


def val_party(point):
    lat=point[0]
    lon=point[1]
    radio=2000
    item=("night_club","type")
    result=apiquery.importar_api_map(lat,lon,radio,item)
    # no hay clubs o error en la consulta
    if isinstance(result,int):
        print(f'error en party, resultado de la consulta :{result}')
        return 0

    # no hay bares de copas
    if len(result)==0:
        return 0
    
    puntos=[]
    [  puntos.append( ( e['lat'] , e['lng'] ) )    for e in result  ]
    
    distancias=[]
    [ distancias.append( f_haversine( point, e ) ) for e in puntos ]

    if min(distancias)>550:
        return 0
    
    dist_550 = list(filter( lambda number: number<550,distancias))
    
    if len(dist_550)==0:
        return 0
    # segun la distancia y el número de bares
    if len(dist_550)>5:
        return 1
    else:
        return(550 - min(dist_550))/550



def val_basquet(point):
    lat=point[0]
    lon=point[1]
    radio=1500
    item=("basketball court","text")
    result=apiquery.importar_api_map(lat,lon,radio,item)
    # no hay canchas o error en la consulta
    if isinstance(result,int):
        print(f'error en basquet, resultado de la consulta :{result}')
        return 0

    # no hay canchas de baloncesto
    if len(result)==0:
        return 0
    
    puntos=[]
    [  puntos.append( ( e['lat'] , e['lng'] ) )    for e in result  ]
    
    distancias=[]
    [ distancias.append( f_haversine( point, e ) ) for e in puntos ]

    # si hay mas de dos retorna 1
    if len(distancias)>2:
        return 1
    else:
        return(1500 - min(distancias))/1500

def val_vegetariano(point):
    lat=point[0]
    lon=point[1]
    radio=1500
    item=("vegan restaurant","text")
    result=apiquery.importar_api_map(lat,lon,radio,item)
    # no hay vaganos o error en la consulta
    if isinstance(result,int):
        print(f'error en veganos, resultado de la consulta :{result}')
        return 0

   # no hay restaurantes venganos
    if len(result)==0:
        return 0
    
    puntos=[]
    [  puntos.append( ( e['lat'] , e['lng'] ) )    for e in result  ]
    
    distancias=[]
    [ distancias.append( f_haversine( point, e ) ) for e in puntos ]

    # si hay mas de dos retorna 1
    if len(distancias)>2:
        return 1
    else:
        return(1500 - min(distancias))/1500
