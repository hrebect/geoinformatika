import json, sys
from pyproj import CRS, Transformer


#priprava prevodu mezi wgs a jtsk
crs_wgs = CRS.from_epsg(4326)
crs_jtsk = CRS.from_epsg(5514)
wgs2jtsk= Transformer.from_crs(crs_wgs,crs_jtsk)

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
conteiner_features = kontejnery_data["features"]

kontejnery = []
#vyber souradnic kontejneru

for conteiner in conteiner_features: #projde vsechny kontejnery
     c_properties = conteiner["properties"]
     c_pristup = c_properties["PRISTUP"]
     
     if c_pristup == 'volně': #souradnice volnych kontejneru ulozi do listu 'kontejnery'
        c_geometry = conteiner["geometry"]
        c_coordinates = (c_geometry['coordinates'])
        kontejnery.append(c_coordinates)


for buliding in adresy_features:  #projede vsechny budovy
    b_properties = buliding["properties"]
    b_geometry = buliding["geometry"]
    b_coordinates = (b_geometry['coordinates'])
    b_address = str(b_properties["addr:street"] + ' ' + b_properties["addr:housenumber"])
    y,x = wgs2jtsk.transform(b_coordinates[1],b_coordinates[0]) #prevod souradnic
    coord_jtsk = [y,x] #ulozeni souradnic jako list, aby byly stejný typ jako souradnice kontejneru
    
    
    #print(coord_jtsk)

