# Scraper voleb
### O co jde v projektu?
Tento skript umožňuje získat výsledky voleb pro konkrétní okres z volby.cz
### Jak na to?

  Program spustíš s dvěma parametry, odkaz na stránku volebního okresu a název výstupního souboru.
> python _cesta k programu_ _"odkaz"_ _soubor_

např:
> python f:/scraper_voleb/main.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=14&xnumnuts=8103" volby.csv

### Příklady správných odkazů
- https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2104
- https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=4&xnumnuts=3203
- https://volby.cz/pls/ps2021/ps32?xjazyk=CZ&xkraj=13&xnumnuts=7204
