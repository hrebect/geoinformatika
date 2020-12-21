import json

#nacteni souboru
with open('kontejnery.geojson', 'r') as f:
    data=json.loads(f)


print(type(data))