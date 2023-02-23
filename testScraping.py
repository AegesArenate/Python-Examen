import requests 
from bs4 import BeautifulSoup 
import csv
import re

# L'url du site que je souhaite Scraper
baseUrl = 'https://www.cardmarket.com'
uri = "/fr/Magic/Products/Singles?site="

# Genere des liens avec l'argument "page" qui s'incrémente
def getLinks(url, nbPg):
    # initialisation du resultat (vide pour l'instant)
    urls = []
    # Pour chaque page
    for i in range(nbPg):
        # Ajoute la concatenation de l'url avec l'index au tableau d'urls
        urls.append(url + str(i))
    return urls

# Fonction qui permet de "crawler" sur le site et recuperer tous les liens sur la page visée
def getEndpoints(soup):
    links = []
    divA = soup.find('div', { "class": "table-body"})
    arrDivB = divA.findAll('div', {"class":"row no-gutters"})
    for divB in arrDivB :
        arrDivC = divB.findAll('div', {"class":"col"})
        for divC in arrDivC :
            arrDivD = divC.findAll('div', {"class":"row no-gutters"})
            for divD in arrDivD :
                divE = divD.find('div', {"class":"col-10"})
                a = divE.find('a')
                try: 
                    links.append({
                        'url': a['href'],
                        'text': a.text.strip()
                    })
                except:
                    pass
    return links

def getInfoByPage(soup):
    fiches = []
    fiche = {}
    infoListContainer = soup.find("div",{"class": "info-list-container"})
    labeled = infoListContainer.find('dl', {"class": "labeled"})
    number = labeled.find("dd", {"class": "d-none d-md-block col-6 col-xl-7"})
    try: 
        fiches.append({
            'number': number.text.strip()
        })
    except:
        pass
    edition = number.findAll("dd", {"class": "col-6 col-xl-7"})
    for dda in edition :
        divFlex = dda.find("div", {"class": "d-flex"})
        a = divFlex.find("a", {"class","mb-2"})
        try: 
            fiches.append({
                'edition': a.text.strip()
            })
        except:
            pass
    trendPrice = labeled.findAll("dd", {"class": "col-6 col-xl-7"})
    for ddb in trendPrice:
        spana = ddb.findAll("span")[2]
        try: 
            fiches.append({
                'trendPrice': spana.text.strip()
            })
        except:
            pass
    sevTrendPrice = labeled.findAll("dd", {"class": "col-6 col-xl-7"})
    for ddc in sevTrendPrice:
        spanb = ddc.findAll("span")[4]
        try: 
            fiches.append({
                'sevTrendPrice': spanb.text.strip()
            })
        except:
            pass
    fiche = {
        "number": number,
        "edition": edition,
        "trendPrice": trendPrice,
        "sevTrendPrice": sevTrendPrice
    }
    dMdBlock = infoListContainer.find('div', {"class": "d-md-block "})
    if dMdBlock is not None:
        description = dMdBlock.find("p")
        try: 
            fiches.append({
                fiche['description']: description.text.strip()
            })
        except:
            pass
    fiches.append(fiche)
    return fiches 

# Fonction qui récupère les informations de la page et les ajoute à une liste

   
def swoup(url, process):
    # Instanciation de mon proxy
    response = requests.get(url)
    # si mon site renvoie un code HTTP 200 (OK)
    if response.ok:
        # je passe le contenue html de ma page dans un "parser"
        soup = BeautifulSoup(response.text, 'html.parser')
        try:
            # Je retourne l'execution de ma fonction process prenan ma SWOUP SWOUP en parametre
            return process(soup)
        except Exception:
            print("ERROR: Impossible to process ! ")
    else:
        print("ERROR: Failed Connect")
    return 


# concatene mes liens a l'url
def addBaseUrl(baseUrl, urls):
    res = []
    for url in urls or []:
        res.append({
            'url': baseUrl + url['url'],
            'text': url['text']
        })
    return res


urls = []
for link in getLinks(baseUrl + uri, 3):
    print("Checking " + link)
    urls.extend(addBaseUrl(baseUrl, swoup(link, getEndpoints)))
    print("You'got actually :" + str(len(urls)) + " links !")
        
print(urls, "Pshatek got : " + str(len(urls)) + " links !")

# Pour chaque URL, on récupère les informations sur la carte
cards = []
for url in urls:
    print("Scraping " + url['url'])
    card = {}
    card['link'] = url['url']
    card['text'] = url['text']
    swoup(url['url'], lambda soup: getInfoByPage(soup, card))
    cards.append(card)

# Enregistrement des informations dans un fichier CSV
fieldnames = ['id', 'link', 'text', 'number', 'edition', 'trendPrice', 'sevTrendPrice', 'description']
with open('linkList.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for card in cards:
        writer.writerow(card)