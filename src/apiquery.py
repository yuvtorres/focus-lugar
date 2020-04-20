import requests
import json
import os
import pandas as pd
import time
 
import pandas as pd
from dotenv import load_dotenv

# A partir de una lista de ciudades/coordenadas, y la lista de lugares
# generá tantas bd/JSON como lugares con las coordenadas de los mismos.

def genera_bd():
    ciudades=[{'ciudad':'Madrid',
                  'latitud':40.416977,
                  'longitud':-3.703827},
               {'ciudad':'New York',
                  'latitud':40.7142715,
                  'longitud': -74.0059662},
               {'ciudad':'Berlin',
                 'latitud': 52.5243683,
                 'longitud': 13.4105301},
               {'ciudad':'Seatle',
                 'latitud':47.6062088,
                 'longitud': -122.3320694}]

    Lugares = [('kindergarden','text'),
               ('train_station','type'),
               ('starbucks','text'),
               ('night_club','type'),
               ('basketball court','text')]
    for city in ciudades:
        for lugar in Lugares:
            result=importar_api_map(city['latitud'],city['longitud'],2000,lugar)
            result=pd.DataFrame(result)
            result.to_json('output/'+city['ciudad']+'_'+lugar[0]+".json")

    return True

# Recibe las coordenadas, el radio de busqueda y criterio como tuple, y retorna 
# una lista con las coordenadas como tuplas

def importar_api_map(lat,lon,radio,item):
    load_dotenv()

    if item[1]=='text':
        content='keyword'
    elif item[1]=='type':
        content='type'
    else:
        print('Error pasing item argument')
        return 0

    key=os.getenv('key_api_map')
    url="https://maps.googleapis.com/maps/api/place/nearbysearch/json?location="\
            +str(lat)+","+str(lon)+"&radius="+str(radio)+"&"+content+"="+item[0]+"&key="+key
    res=requests.get(url)
    data=res.json()
    resultado=[]
    if data['status']=='OK':
        [resultado.append(e['geometry']['location']) for e in data['results']]
    else:
        print(f'error in lat:{lat}, lon:{lon} and item:{item} search')
        return 0

    while 'next_page_token' in data:
        time.sleep(2)
        url="https://maps.googleapis.com/maps/api/place/nearbysearch/json?pagetoken="\
                +data['next_page_token']+"&key="+key#+"&location="+str(lat)+","+str(lon)\
                                                    #      +"&radius="+str(radio)
        
        res=requests.get(url)
        data2=res.json()
        if data2['status']=='OK' and len(data2['results'])>0:
            [resultado.append(e['geometry']['location'] ) for e in data2['results']]
        else:
            print(f'error in lat:{lat}, lon:{lon} and item:{item} search')
            print(f'Status: {data2["status"]} - results:{data2["results"]} ')
            return 0
        data=data2

    return resultado


