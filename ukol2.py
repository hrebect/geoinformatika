import json

#nacteni souboru
with open('adresy.geojson',encoding='utf-8') as f:
    kontejnery = json.load(f)


print(type(kontejnery))