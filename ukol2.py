import json, sys, math
from pyproj import CRS, Transformer


#priprava prevodu mezi wgs a jtsk
crs_wgs = CRS.from_epsg(4326)
crs_jtsk = CRS.from_epsg(5514)
wgs2jtsk= Transformer.from_crs(crs_wgs,crs_jtsk)



def verejne_kont(kontejnery_data):#vyber souradnic  verejnych kontejneru
    kontejnery = []
    conteiner_features = kontejnery_data["features"]

    for conteiner in conteiner_features: #projde vsechny kontejnery
        properties = conteiner["properties"]
        pristup = properties["PRISTUP"]
     
        if pristup == 'volně': #souradnice volnych kontejneru ulozi do listu 'kontejnery'
            geometry = conteiner["geometry"]
            coordinates = (geometry['coordinates'])
            kontejnery.append(coordinates)
    return kontejnery

def vzdalenosti(adresy_data, kontejnery):
    adresy_features = adresy_data["features"] 
    max_minimum = 0
    for buliding in adresy_features:  #projede vsechny budovy 
        properties = buliding["properties"]
        geometry = buliding["geometry"]
        coordinates = (geometry['coordinates'])
        address = str(properties["addr:street"] + ' ' + properties["addr:housenumber"])
        y,x = wgs2jtsk.transform(coordinates[1],coordinates[0]) #prevod souradnic
        coord_jtsk = [y,x] #ulozeni souradnic jako list, aby byly stejný typ jako souradnice kontejneru
        minimum = 10000
        
        for souradnice in kontejnery: #vypocet vzdalenosti od kazdeho kontejneru
            x_vzdalenost = coord_jtsk[1]-souradnice[1]
            y_vzdalenost = coord_jtsk[0]-souradnice[0]
            vzdalenost = math.sqrt(x_vzdalenost * x_vzdalenost + y_vzdalenost *y_vzdalenost)
            if vzdalenost < minimum:
                minimum = vzdalenost
        if minimum > 10000: #ukoncveni programu, kdyz je u jednoho konejnery minimum vice nez 10 km
            sys.exit('CHYBA, u jedné adresy je nejbližší kontejner vzdálen více než 10 km')  
        if minimum > max_minimum:
            max_minimum = minimum
            max_address = address
    print(f'Nejdále ke kontejneru je z adresy {max_address} a to {int(round(max_minimum,0))} m.') 
    
    #print(coord_jtsk)

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

kontejnery = verejne_kont(kontejnery_data)

print(vzdalenosti(adresy_data,kontejnery))