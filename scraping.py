import requests 
from bs4 import BeautifulSoup 
import csv


baseUrl = 'https://www.cardmarket.com'
uri = "/fr/Magic/Products/Singles?site="

def getLinks(url, nbPg):
    urls = []
    for i in range(nbPg):
        urls.append(url + str(i))
    return urls

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

def swoup(url, process):
    response = requests.get(url)
    if response.ok:
        soup = BeautifulSoup(response.text, 'html.parser')
        try:
            return process(soup)
        except Exception:
            print("ERROR: Impossible to process ! " )
    else:
        print("ERROR: Failed Connect")
    return 

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
    print("You'got actually :"+ str(len(urls)) + " links !")
        
print(urls, "Pshatek got : " + str(len(urls)) + " links !")

rows = []
i = 0
for url in urls:
    print("Writing : " + str(i))
    row = {}
    row['id'] = i
    row['link'] = url['url']
    row['text'] = url['text']
    rows.append(row)
    i += 1

fieldnames = ['id', 'link', 'text']
with open('linkList.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)
    
print("Done")