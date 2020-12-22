import json, sys


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
    print(properties["addr:street"], properties["addr:housenumber"])