import sys
sys.path.insert(0, 'src/')
from funobjetivo import fun_objetivo
import research_tool
import geopandas as gpd
import json
from geojson import Polygon, Feature, FeatureCollection
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib import pyplot as plt

# La solución alternativa es valorar la función en una malla de puntos sobre cada ciudad.
# 1) Generación de la malla de puntos y sus valores


def main():
    #
    # Calcula la malla para new york
    #
    valor_ny=[]
    lat_max=40.859602
    lat_min=40.641156
    lng_max=-73.887981
    lng_min=-74.025693
    num_pasos=20
    paso_lat=(lat_max-lat_min)/num_pasos
    paso_lng=(lng_max-lng_min)/num_pasos

    for i in range(num_pasos):
        linea_valor=[]
        for k in range(num_pasos):
            linea_valor.append(fun_objetivo([lat_min+k*paso_lat,lng_min+i*paso_lng]))
        
        valor_ny.append(linea_valor)


    malla_ny=[]
    for i in range(num_pasos):
        for k in range(num_pasos):
            el_cubo=Polygon([[(lng_min + ( float(i) - 0.5)*paso_lng, lat_min + (float(k)-0.5)*paso_lat),
                          (lng_min + ( float(i) + 0.5)*paso_lng, lat_min + (float(k)-0.5)*paso_lat),
                          (lng_min + ( float(i) + 0.5)*paso_lng, lat_min + (float(k)+0.5)*paso_lat),
                          (lng_min + ( float(i) - 0.5)*paso_lng, lat_min + (float(k)+0.5)*paso_lat),
                          (lng_min + ( float(i) - 0.5)*paso_lng, lat_min + (float(k)-0.5)*paso_lat)]])

        malla_ny.append( Feature(properties={"valor":valor[k][i]},geometry=el_cubo) )

    malla_ny_json= FeatureCollection(malla_ny)
    
    with open('../output/ny_json.json', 'w') as outfile:
        json.dump(malla_ny_json, outfile)

    df1=gpd.read_file('../output/ny_json.json')
    df1 = df1.to_crs(epsg=3857)

    fig,ax1=plt.subplots(1, 1)
    divider = make_axes_locatable(ax1)
    cax = divider.append_axes("right", size="5%", pad=0.1)
    ax1=df1.plot(column='valor', alpha=0.5, ax=ax1,legend=True, cax=cax)
    fig.set_size_inches(10.5, 15.5)
    ctx.add_basemap(ax1)
    plt.savefig('../output/map_ny.png')


    #
    # Calcula la malla para madrid
    #
    valor_md=[]
    nlat_max=40.521943
    lat_min=40.402217
    lng_max=-3.736493
    lng_min=-3.658524
    num_pasos=20
    paso_lat=(lat_max-lat_min)/num_pasos
    paso_lng=(lng_max-lng_min)/num_pasos

    for i in range(num_pasos):
        linea_valor=[]
        for k in range(num_pasos):
            linea_valor.append(fun_objetivo([lat_min+k*paso_lat,lng_min+i*paso_lng]))
        
        valor_md.append(linea_valor)


    malla_md=[]
    for i in range(num_pasos):
        for k in range(num_pasos):
            el_cubo=Polygon([[(lng_min + ( float(i) - 0.5)*paso_lng, lat_min + (float(k)-0.5)*paso_lat),
                          (lng_min + ( float(i) + 0.5)*paso_lng, lat_min + (float(k)-0.5)*paso_lat),
                          (lng_min + ( float(i) + 0.5)*paso_lng, lat_min + (float(k)+0.5)*paso_lat),
                          (lng_min + ( float(i) - 0.5)*paso_lng, lat_min + (float(k)+0.5)*paso_lat),
                          (lng_min + ( float(i) - 0.5)*paso_lng, lat_min + (float(k)-0.5)*paso_lat)]])

        malla_md.append( Feature(properties={"valor":valor[k][i]},geometry=el_cubo) )

    malla_md_json= FeatureCollection(malla_md)
    
    with open('../output/md_json.json', 'w') as outfile:
        json.dump(malla_md_json, outfile)

    df1=gpd.read_file('../output/md_json.json')
    df1 = df1.to_crs(epsg=3857)

    fig,ax1=plt.subplots(1, 1)
    divider = make_axes_locatable(ax1)
    cax = divider.append_axes("right", size="5%", pad=0.1)
    ax1=df1.plot(column='valor', alpha=0.5, ax=ax1,legend=True, cax=cax)
    fig.set_size_inches(10.5, 15.5)
    ctx.add_basemap(ax1)
    plt.savefig('../output/map_md.png')


if __name__=="__main__":
    main()

