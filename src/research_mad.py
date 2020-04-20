import math
import json
from pymongo import MongoClient

def val_design_madrid(point_madrid):
    
    # Connect and get the data --> coordenates
    url_mongo = "mongodb://localhost:27017"
    client = MongoClient(url_mongo)
    db = client.get_database("design")
    # *** El punto es pasado como Lat-Lon y Mongodb recibe a busqueda como Lon-Lat
    query={design_coor:{$nearSphere: [point_madrid[1], point_madrid[0]]}}
    result = list(db.companies.find(query,{"latitude":1,"longitud":1,"_id":0}))

    # no hay empresas de diseño
    if len(result)==0:
        return 0
    
    puntos=[]
    [  puntos.append( ( e['latitud'] , e['longitud'] ) )    for e in result  ]
    
    distancias=[]
    [ distancias.append( f_haversine( point_madrid, e ) ) for e in puntos ]
    
    dist_1000 = list(filter( lambda number: number<1000,distance))

    # las empresas que hay estan a mas de 1000 mt
    if len dist_1000==0:
        return 0.2

    if min (distancias) < 100:
        return 1

    else:
        return 0.2 +0.8*(1000 - min(distancia))/900


# distancia entre dos puntos Lat,Log
def f_haversine(point1,point2):
    dlon = point1[1]- point2[1]
    dlat = point1[0]- point2[0]
    a = math.sin (dlat/2)**2 + math.cos(point1[0]) * math.cos(point2[0]) * math.sin(dlon/2)**2
    r= 6.371 *1e6
    return a * r



def val_kindergarden_madrid(point_madrid):
    fp=open('../output/')
    points=json.load()

def val_succ_madrid(point_madrid)
    # Connect and get the data --> coodenates
    url_mongo = "mongodb://localhost:27017"
    client = MongoClient(url_mongo)
    db = client.get_database("design")
    result = list(db.companies.find({},{"category_code":1,"_id":0}))
    categories = [e['category_code'] for e in result]


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


