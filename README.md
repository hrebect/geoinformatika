## Dokumentace k programu
Program má za úkol ze souborů adres a kontejnerů ve formátu GeoJSON vypočítat maximální a průměrnou vzdálenost k nejbližšímu veřejnému kontejneru z adres.
### Funkce programu
První funkce programu je zde příprava převodu souřadnic z wgs do Jtsk pomocí knihovny `PyProj` a funkcí `Transformer`.
Vstupními soubory programu jsou `kontejnery.geojson` a `adresy.geojson`. 
Když soubory nejsou k dispozici, tak se program ukončí.
Z nich je v následujících funkcích `verejne_kont` a `vzdalenosti` dostána potřebná data a následně zpracována.
#### verejne_kont
Tato funkce ze slovníku, obsahující jednotlivé informace o kontejnerech, vezme všechny kontejnery, která mají hodnotu klíče `PRISTUP` „volně“ a nahrají jejich souřadnice do listu `kontejnery`.
#### vzdalenosti
Tato funkce získá k jednotlivým domům adresy z hodnot klíče `addr:street` a `addr:housenumber` a jejich souřadnice z klíče `coordinates`. Tyto souřadnice jsou ve formátu wgs. Proto je na ně použita již připravená funkce pro převod souřadnic do jtsk.
Pomocí Pythagorovy věty je následné vypočítána vzdálenost k jednotlivým kontejnerům a zaznamenána ta nejmenší.
Nejmenší vzdálenosti jsou uloženy do listu `list_minim`. Když nějaká z nich přesáhne 10 km, tak se program ukončí.
Nakonec je pomocí knihovny `statistics` získán průměr a medián a jednotlivé výsledky jsou vypsány na obrazovku.

