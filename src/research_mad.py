# Este modulo contiene las funciones que devuelven un valor entre cero y uno
# según criterios geograficos para 
import math
import json
from pymongo import MongoClient

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
        return 0.2 +0.8*(1000 - min(distancia))/900

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
        return 0.2 +0.8*(1000 - min(distancia))/900

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
    return (2000 - min(dist_2000))/2000



def val_kindergarden_madrid(point_madrid):
    fp=open('../output/')
    points=json.load()



def val_starbucks_madrid(point_madrid):
    fp=open('../output/')
    points=json.load()


def val_airport_madrid(point_madrid):
    fp=open('../output/')
    points=json.load()


def val_party_madrid(point_madrid):
    fp=open('../output/')
    points=json.load()


def val_basquet_madrid(point_madrid):
    fp=open('../output/')
    points=json.load()


def val_old_madrid(point_madrid):
    # Connect and get the data --> coodenates
    url_mongo = "mongodb://localhost:27017"
    client = MongoClient(url_mongo)
    db = client.get_database("design")
    result = list(db.companies.find({},{"category_code":1,"_id":0}))
    categories = [e['category_code'] for e in result]

def val_vegetariano_madrid(point_madrid):
    fp=open('../output/')
    points=json.load()


