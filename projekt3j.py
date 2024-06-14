## projekt_3.py: třetí projekt
autor: Veronika Pazderová
email: veronikapazderova06@gmail.com
discord: Weruna
##
import requests as req  
from bs4 import BeautifulSoup as bs 
from urllib.parse import urljoin  
from time import sleep  
from random import choice  
import sys  

def get_page(link):  
    for pokus in range(1, 7):  ## Pro cyklus s proměnnou pokus od 1 do 6
        try:  ## Začátek bloku try
            print("stahování", link)  
            page = bs(req.get(link).text, features="html.parser")  
            print("úspěch")  
            return page  
        except req.exceptions.ConnectionError:  
            print("Odmítnuto připojení, čekání", 10 * pokus, "sekund")  
            sleep(10 * pokus)  
    print("CHYBA - stránka se nepodařilo stáhnout")  ## Vypíše chybovou zprávu
    return  ## Vrátí None

def count_results(results_page):  
    print("počítání výsledků")  
    return  ## Vrátí None

if len(sys.argv) < 3:  
    print("Je zapotřebí zadat odkaz na územní celek a název výstupního souboru")  ## Vypíše zprávu o nutnosti zadat správné argumenty
    sys.exit(1)  ## Ukončí program s chybovým kódem 1

main_link = sys.argv[1]  ## První argument se použije jako hlavní odkaz
main_page = get_page(sys.argv[1])  ## Zavolá funkci get_page s hlavním odkazem a uloží vrácenou stránku do main_page

print(main_page.find("h1").text)  ## Vypíše text obsažený v prvním nadpisu h1 na hlavní stránce
if "Praha" in main_page.find_all("h3")[0].text:  ## Pokud je na hlavní stránce nadpis h3 obsahující "Praha"
    print(main_page.find_all("h3")[0].text)  ## Vypíše tento nadpis
else:  ## Jinak
    print(main_page.find_all("h3")[0].text, main_page.find_all("h3")[1].text)  

links = []  ## Inicializuje prázdný seznam odkazů
for tag in main_page.find_all('td', {'class' : 'center'}):  
    children = tag.findChildren()  
    links.append(children[0]['href'])  

rows = []  ## Inicializuje prázdný seznam řádků
headers = ["kód obce", "název obce", "okrsek", "voliči v seznamu", "vydané obálky", "platné hlasy"]  ## Vytvoří seznam hlaviček
page = get_page(urljoin(main_link, choice(links)))  ## Zavolá funkci get_page s náhodně vybraným odkazem a uloží vrácenou stránku do page

if page.find("h2").text.strip() == "Výsledky hlasování za územní celky – výběr okrsku":  ## Pokud je na stránce nadpis h2 obsahující "Výsledky hlasování za územní celky – výběr okrsku"
    page = get_page(urljoin(main_link, choice(page.find_all('td', {'class' : 'cislo'})).findChildren()[0]["href"]))  ## Zavolá funkci get_page s náhodně vybraným odkazem a uloží vrácenou stránku do page
elif page.find("h2").text.strip() == "Výsledky hlasování za územní celky":  ## Pokud je na stránce nadpis h2 obsahující "Výsledky hlasování za územní celky"
    pass  ## Nic se neděje
else:  
    print("CHYBA - stránka není rozpoznána")  

for party_name in page.find_all("td", {"class" : "overflow_name"}):  ## Prochází všechny tagy td s třídou overflow_name na stránce
    headers.append(party_name.text)  

rows.append(headers)  
print(headers)  
print(rows[0])  

for link in links:  
    page = get_page(urljoin(main_link,