import sys
from datetime import datetime
import csv
import glob, os
import enchant
import requests

if len(sys.argv) > 1:
    board = sys.argv[1]
else:
    board = 'biz'
    
now = datetime.now().strftime("%Y%m%d_%H%M%S")

coinMarketCapFolder="..\\..\\coinmarketcap\\result"
ForchanFolder = "..\\..\\4chan\\result\\board\\"+board
resultFile = "..\\..\\4chan\\result\\board\\"+board+"\\merged\\merged_result_"+now+".csv"


def getMarket():
    response = []
    for i in(range(0,20)):
        try:
            response1 = requests.get(timeout=3, url="https://api.coinlore.net/api/tickers/?start="+  str(i*200) + "&limit="+  str(i*200 +200) )
            response = response + response1.json()["data"]
        except:
            try:
                response1 = requests.get(timeout=3, url="https://api.coinlore.net/api/tickers/?start="+  str(i*200) + "&limit="+  str(i*200 +200) )
                response = response + response1.json()["data"]
            except:
                print("fail getting loop nb#"+str(i))

    return response
    
global dataMarketCap
dataMarketCap = getMarket()

def getDataByTicker(ticker):
    for elem in dataMarketCap:
        if(elem['symbol'].lower() == ticker):
           return [elem['market_cap_usd'],elem['percent_change_7d'],str(elem['rank'])]
    return -1

def getDataByName(name):
    for elem in dataMarketCap:
        if(elem['name'].lower() == name):
           return [elem['market_cap_usd'],elem['percent_change_7d'],str(elem['rank'])]
    return -1

def csvIntoArray(filePath):
    with open(filePath, encoding="utf8", newline='') as f:
        reader = csv.reader(f, delimiter  = ';')
        data = list(reader)
    return data

def getMostResentFileInFolder(folderPath, extension):
    return glob.glob(folderPath+ "\\*." + extension)[len(glob.glob(folderPath+ "\\*."+extension))-1]

def isKeyInList(liste, indice, toFind):
    for elem in liste:
        if(elem[indice].lower() == toFind.lower()):
            return True
    return False

    
def getCryptosFromDictionnary(dico, coinMarketCap):
    data = []
    d = enchant.Dict("en_US")
    for mot in dico:
        for coin in coinMarketCap:
            if( (mot[0].lower() == coin[1].lower()) or (mot[0].lower() == coin[2].lower()) ):
                if( not isKeyInList(data, 0, mot[0].lower() )  ):
                    if(not d.check(mot[0].lower())):

                        temp = -1
                        temp = getDataByTicker(mot[0].lower())
                        if(temp == -1):
                            temp = getDataByName(mot[0].lower())
                        if(temp == -1):
                            temp = ["","",""]
                        mot.append("")
                        mot.append(temp[0])
                        mot.append(temp[1])
                        mot.append(temp[2])
                        data.append(mot)

    return data

coinMarketCapFile = getMostResentFileInFolder(coinMarketCapFolder, "csv")
listCoins = csvIntoArray(coinMarketCapFile)

ForchanFile = getMostResentFileInFolder(ForchanFolder, "csv")
ForchanData = csvIntoArray(ForchanFile)


merged = getCryptosFromDictionnary(ForchanData, listCoins)
merged = sorted(merged, key=lambda x: int(x[2]), reverse=True)

if not os.path.exists(os.path.dirname(resultFile)):
    try:
        os.makedirs(os.path.dirname(resultFile))
    except OSError as exc: # Guard against race condition
        if exc.errno != errno.EEXIST:
            raise
        
with open(resultFile, 'w+') as fp:
    fp.write("Mot;;Nb Apparition Titre;Nb Rep total Titre ;Moy Rep/App Titre;;Nb Apparition Contenu;Nb Rep total Contenu;Moy Rep/App Contenu;Presence dans les reponses;;MarketCap;Percent7Days;Rank\n")
    for i in range(len(merged)):
        fp.write(';'.join(merged[i])+"\n")

