import json, sys
from pyproj import CRS, Transformer

#funkce na prevod souradnic z wgs do jtsk
#vstup je list 
def prevod(souradnice):
    crs_wgs = CRS.from_epsg(4326)
    crs_jtsk = CRS.from_epsg(5514)
    wgs2jtsk= Transformer.from_crs(crs_wgs,crs_jtsk)
    y = souradnice[1]
    x = souradnice[0]
    return wgs2jtsk.transform(y,x)



#nacteni souboru
try:
    with open('adresy.geojson',encoding='utf-8') as f:
        adresy_data = json.load(f)
except FileNotFoundError:
    sys.exit('Soubor s adresami nenalezen')
try:
    with open('kontejnery.geojson',encoding='utf-8') as e:   
        kontejnery_data = json.load(e)
except FileNotFoundError:
    sys.exit('Soubor s kontejnery nenalezen')


adresy_features = adresy_data["features"] 

for buliding in adresy_features:  #projede vsechny budovy
    properties = buliding["properties"]
    geometry = buliding["geometry"]
    coordinates = (geometry['coordinates'])
    address = str(properties["addr:street"] + ' ' + properties["addr:housenumber"])
    y,x = prevod(coordinates)
    coord_jtsk = [y, x] #ulozeni souradnic jako list, aby byly stejný typ jako souradnice kontejneru


