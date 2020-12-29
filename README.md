## Vzdálenost ke kontejnerům na tříděný odpad
Program má za úkol ze souborů adres a kontejnerů ve formátu GeoJSON vypočítat maximální a průměrnou vzdálenost k nejbližšímu veřejnému kontejneru z adres.
### Vlastnosti programu
Program načte 2 soubory, jeden nese informace o kontejnerech a druhý o adresách. Když je jeden nebo oba soubory nedostupný, program se ukončí. S chybami uvnitř souborů program nepočítá, a když nějaké naskytnou, spadne.
Program se souborů získá potřebné atributy pro další zpracování.
Ke každé adrese vypočítá nebližší kontejner. Když u nějaké adresy nastane, že je nejbližší kontejner vzdálen 10 km, tak se program ukončí.
Výsledkem programu je adresa, která má nejdál k nejbližšímu kontejneru, průměrná vzdálenost k nejbližšímu kontejneru a medián.
### Vstupní soubor
Vstup tvoří 2 soubory ve formátu GeoJSON
Vstupní soubor adres je v souřadnicovém systému WGS84 a soubor kontejnerů v JTSK.
U adres je potřeba, aby soubor obsahoval `addr:street` a `addr:housenumber` a `coordinates`.
U dat s kontejnery nás zajímají `coordinates` a `PRISTUP`.
#### verejne_kont
Tato funkce ze slovníku, obsahující jednotlivé informace o kontejnerech, vezme všechny kontejnery, které mají hodnotu klíče `PRISTUP` „volně“ a nahrají jejich souřadnice do listu `kontejnery` a vrátí seznam souřadnic všech přístupných kontejnerů.
#### adresy
Funkce `adresy` ze slovníku s adresami získá souřadnice sledovaných budov, které rovnou převede do JTSK, a jejich adresu jako textový řetězec. Tyto informace vrátí jako 2 seznamy.
#### vzdalenosti
Tato funkce vezme seznam souřadnic adres a seznam souřadnic kontejnerů a vypočítá mezi nimi vzdálenost.
Ke každé adrese se zjistí nejbližší kontejner. Tyto výsledky jsou vráceny jako seznam minimálních vzdáleností. Dále funkce vrací největší vzdálenost ze seznamu minimálních vzdáleností a řetězec s adresou k této hodnotě.
