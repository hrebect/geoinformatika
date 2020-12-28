import json, sys, math, statistics
from pyproj import CRS, Transformer


#priprava prevodu mezi wgs a jtsk
crs_wgs = CRS.from_epsg(4326)
crs_jtsk = CRS.from_epsg(5514)
wgs2jtsk= Transformer.from_crs(crs_wgs,crs_jtsk)



def verejne_kont(kontejnery_data):#vyber souradnic  verejnych kontejneru
    kontejnery = []
    container_features = kontejnery_data["features"]

    for container in container_features: #projde vsechny kontejnery
        properties = container["properties"]
        pristup = properties["PRISTUP"]
     
        if pristup == 'volně': #souradnice volnych kontejneru ulozi do listu 'kontejnery'
            geometry = container["geometry"]
            coordinates = (geometry['coordinates'])
            kontejnery.append(coordinates)
    return kontejnery

def vzdalenosti(adresy_data, kontejnery):
    adresy_features = adresy_data["features"] 
    
    list_minim = [] #list pro median
    max_minimum = 0 #vzdalenost nemuze byt zaporna, spodni hranice maximalního minima
    
    for buliding in adresy_features:  #projede vsechny budovy 
        properties = buliding["properties"]
        geometry = buliding["geometry"]
        coordinates = (geometry['coordinates'])
        address = str(properties["addr:street"] + ' ' + properties["addr:housenumber"])
        y,x = wgs2jtsk.transform(coordinates[1],coordinates[0]) #prevod souradnic
        coord_build = [y,x] #ulozeni souradnic jako list, aby byly stejný typ jako souradnice kontejneru
        minimum = 10000 #horní hranice minima, podle zadani nepracujeme se vzdalenostmi nad 10 km
        
        for coord_cont in kontejnery: #vypocet vzdalenosti od kazdeho kontejneru
            x_vzdalenost = coord_build[1]-coord_cont[1]
            y_vzdalenost = coord_build[0]-coord_cont[0]
            vzdalenost = math.sqrt(x_vzdalenost * x_vzdalenost + y_vzdalenost *y_vzdalenost) #phytagoras
            if vzdalenost < minimum: #hledani minima pro adresu v ramci kontejneru
                minimum = vzdalenost
        list_minim.append(minimum) #list vsech minim
        if minimum > 10000: #ukoncveni programu, kdyz je u jednoho konejnery minimum vice nez 10 km
            sys.exit('CHYBA, u jedné adresy je nejbližší kontejner vzdálen více než 10 km')  
        
        if minimum > max_minimum: #hledání maximalního minima v ramci vsech adres
            max_minimum = minimum
            max_address = address
        
    #vypocte prumeru
    prumer = statistics.mean(list_minim)
    #vystupy
    print(f'Načteno {len(adresy_features)} adresních bodů')
    print(f'Načteno {len(kontejnery)} kontejnerů\n')
    print(f'Pruměrná vzdálenost ke kontejneru je {int(round(prumer,0))} m.')
    print(f'Nejdále ke kontejneru je z adresy {max_address} a to {int(round(max_minimum,0))} m.')
    print(f'Medián vzdáleností je {int(round(statistics.median(list_minim)))} m.') #vypocet medianu a jeho zobrazeni

#nacteni souboru
try:
    with open('adresy.geojson',encoding='utf-8') as f:
        adresy_data = json.load(f)
except FileNotFoundError: #ukonceni programu, kdyz soubor nebude nalezen
    sys.exit('Soubor s adresami nenalezen')
try:
    with open('kontejnery.geojson',encoding='utf-8') as e:   
        kontejnery_data = json.load(e)
except FileNotFoundError: #ukonceni programu, kdyz soubor nebude nalezen
    sys.exit('Soubor s kontejnery nenalezen')

kontejnery = verejne_kont(kontejnery_data)
vzdalenosti(adresy_data,kontejnery)