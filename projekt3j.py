## projekt_3.py: třetí projekt
## autor: Veronika Pazderová
## email: veronikapazderova06@gmail.com
##discord: Weruna
## Importujeme potřebné knihovny
import requests as req  ## requests pro HTTP požadavky
from bs4 import BeautifulSoup as bs  ## BeautifulSoup pro parsování HTML
from urllib.parse import urljoin, urlparse, parse_qs  ## Pomocné funkce pro práci s URL
from time import sleep  ## Funkce sleep pro čekání mezi pokusy
from random import choice  ## Funkce choice pro náhodný výběr
import sys  ## Knihovna sys pro přístup k argumentům příkazové řádky
import csv  ## Knihovna csv pro práci s CSV soubory

## Funkce pro získání stránky
def get_page(link: str):
    ## Několik pokusů získat stránku, pokud se nepodaří, čekáme mezi pokusy
    for pokus v rozmezí 1 až 7:
        try:
            print("Získávání stránky", link)
            ## Získáme stránku a parsujeme ji pomocí BeautifulSoup
            page = bs(req.get(link).text, features="html.parser")
            print("Úspěch")
            return page
        except req.exceptions.ConnectionError:
            print("Spojení odmítnuto, čekání", 10 * pokus, "sekund")
            sleep(10 * pokus)
    print("CHYBA - get_page neúspěšná")
    return

## Funkce pro zpracování výsledků ze stránky
def count_results(results_page: bs, link: str):
    print("Počítání výsledků ze stránky", link)
    row = []
    ## Získáme kód obce z URL
    row.append(parse_qs(urlparse(link).query)["xobec"][0])
    ## Název obce
    for h3 in results_page.find_all("h3"):
        if "Obec:" in h3.text:
            row.append(h3.text.strip()[6:])
            break
    ## Okres z URL (pokud existuje)
    try:
        row.append(parse_qs(urlparse(link).query)["xokrsek"][0])
    except KeyError:
        row.append("N/A")
    ## Voliči v seznamu
    row.append(results_page.find("td", {"headers": "sa2"}).text)
    ## Vydané obálky
    row.append(results_page.find("td", {"headers": "sa3"}).text)
    ## Platné hlasy
    row.append(results_page.find("td", {"headers": "sa6"}).text)
    ## Výsledky stran
    for result in results_page.find_all("td", {"headers": "t1sa2 t1sb3"}) + results_page.find_all("td", {"headers": "t2sa2 t2sb3"}):
        row.append(result.text)
    return row

## Hlavní část programu
if len(sys.argv) < 3:
    print("Je zapotřebí zadat odkaz na územní celek a název výstupního souboru")
    sys.exit(1)

## Získání hlavního odkazu a hlavní stránky
main_link = sys.argv[1]
main_page = get_page(main_link)

## Výpis důležitých informací z hlavní stránky
print(main_page.find("h1").text)
if "Praha" in main_page.find_all("h3")[0].text:
    print(main_page.find_all("h3")[0].text)
else:
    print(main_page.find_all("h3")[0].text, main_page.find_all("h3")[1].text)

## Seznam pro uložení odkazů
links = []
## Najdeme všechny odkazy na výsledky
for tag in main_page.find_all("td", {"class": "center"}):
    children = tag.findChildren()
    links.append(children[0]["href"])

## První řádek budou hlavičky, pak data
rows = []
## Hlavičky tabulky
headers = ["kód obce", "název obce", "okrsek", "voliči v seznamu", "vydané obálky", "platné hlasy"]
## Vybereme náhodnou stránku pro získání názvů stran
page = get_page(urljoin(main_link, choice(links)))
if page.find("h2").text.strip() == "Výsledky hlasování za územní celky – výběr okrsku":
    page = get_page(urljoin(main_link, choice(page.find_all("td", {"class": "cislo"})).findChildren()[0]["href"]))
elif page.find("h2").text.strip() == "Výsledky hlasování za územní celky":
    pass
else:
    print("CHYBA - stránka nerozpoznána")

## Přidáme názvy stran do hlaviček
for party_name in page.find_all("td", {"class": "overflow_name"}):
    headers.append(party_name.text)
rows.append(headers)

## Procházíme všechny odkazy a zpracováváme výsledky
for link in links:
    page = get_page(urljoin(main_link, link))
    if page.find("h2").text.strip() == "Výsledky hlasování za územní celky – výběr okrsku":
        for tag in page.find_all("td", {"class": "cislo"}):
            rows.append(count_results(get_page(urljoin(main_link, tag.findChildren()[0]["href"])), urljoin(main_link, tag.findChildren()[0]["href"])))
    elif page.find("h2").text.strip() == "Výsledky hlasování za územní celky":
        rows.append(count_results(page, urljoin(main_link, link)))
    else:
        print("CHYBA - stránka nerozpoznána")
        continue

## Uložíme data do CSV souboru
with open(sys.argv[2], 'w', newline="") as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerows(rows)