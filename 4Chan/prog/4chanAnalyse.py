import sys
import os
from datetime import datetime
import errno
import re
import json
from selenium import webdriver
import requests
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.options import Options



if len(sys.argv) > 1:
    board = sys.argv[1]
else:
    board = 'biz'


start = datetime.now()
now = datetime.now().strftime("%Y%m%d_%H%M%S")

url="https://boards.4channel.org/"+board+"/catalog"
delay = 20 # seconds
jsFile = "js/getTitreContentResponses.txt"
ForchanData = "4chanData.json"
resultFile = "..\\result\\board\\"+board+"\\result_"+now+".csv"


print("#################################################")
print("##########      4 CHAN DATA SCRAPER     #########")
print("#################################################")
print("                  board: "+board)
print("")
print("Openning Firefox Webdriver....")


options = Options()
options.headless = True



driver = webdriver.Firefox(options=options)
print("   > OK\n")

print("Openning url : " + url + " ...")                        
driver.get(url)

try:
    myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'bottom')))
    print("   > OK - Page is ready!\n")
except TimeoutException:
    print("Loading took too much time!")
    exit()

print("Getting JS function from file : " + jsFile +" ...")

with open(jsFile, 'r') as file:
    jsFunction = file.read()
print("   > OK\n")


print("Running JS to get Titles/Contents/Response ...")
jsReturn = driver.execute_script(jsFunction)
print("   > OK\n")

print("Saving data into file : "+ForchanData + " ...")
with open(ForchanData, 'w+', encoding="utf8") as fp:
    fp.write(jsReturn)
print("   > OK\n")

print("Closing Webdriver ...")
driver.close()
driver.quit()
print("   > OK\n")



print("Running dictionnary data extraction algorythm ...")
def isInDict(dict, key):
    if key in dict:
        return True
    return False

def trimWord(word):
    word = word.lower()
    word = word.strip()
    word = re.sub('[^A-Za-z0-9]+', '', word)
    #if word.endswith('s'):
        #word = word[:-1]
    return word

def motAIgnorer(word):
    if(word.endswith('/') and word.startswith('/')):
       return True
    if("http" in word):
       return True
    if(".com" in word):
       return True
    if(word.isnumeric()):
       return True
    if(len(word) < 2):
       return True

    return False



def aUnTotal(elem):
    if(int(elem["total"]) >= 0):
        return True
    return False

dicTitre = {}
listeFinale = []


f = open(ForchanData, encoding="utf8")

data = json.load(f)
 
for elem in data:
    if(aUnTotal(elem)):
        for mot in elem["titre"].split(" "):
            if(motAIgnorer(mot)):
                continue
            motValide = trimWord(mot)
            if(motAIgnorer(motValide)):
                continue
            if(not isInDict(dicTitre, motValide)):
                dicTitre[motValide] = [ 1 , int(elem["total"]), int(elem["total"]), 0 , 0, 0, 0]
                
            else:
                dicTitre[motValide][0] = dicTitre[motValide][0] + 1
                dicTitre[motValide][1] = dicTitre[motValide][1] + int(elem["total"])
                dicTitre[motValide][2] = round(dicTitre[motValide][1] / dicTitre[motValide][0], 2)

        for mot in elem["contenu"].split(" "):
            if(motAIgnorer(mot)):
                continue
            motValide = trimWord(mot)
            if(motAIgnorer(motValide)):
                continue
            if(not isInDict(dicTitre, motValide)):
                dicTitre[motValide] = [ 0 , 0, 0, 1 , int(elem["total"]), int(elem["total"]), 0]
                
            else:
                dicTitre[motValide][3] = dicTitre[motValide][0] + 1
                dicTitre[motValide][4] = dicTitre[motValide][1] + int(elem["total"])
                dicTitre[motValide][5] = round(dicTitre[motValide][4] / dicTitre[motValide][3], 2)

        for mot in elem["allrep"].split(" "):
            if(motAIgnorer(mot)):
                continue
            motValide = trimWord(mot)
            if(motAIgnorer(motValide)):
                continue
            if(not isInDict(dicTitre, motValide)):
                dicTitre[motValide] = [ 0 , 0, 0, 0 , 0, 0, 1]
                
            else:
                dicTitre[motValide][6] = dicTitre[motValide][6] + 1

for key in dicTitre:
    listeFinale.append([key,dicTitre[key][0] ,dicTitre[key][1] ,dicTitre[key][2],dicTitre[key][3],dicTitre[key][4],dicTitre[key][5],dicTitre[key][6]])

listeFinale = sorted(listeFinale, key=lambda x: x[3], reverse=True)
print("   > OK\n")


print("Saving processed data into file "+ resultFile+" ...")

if not os.path.exists(os.path.dirname(resultFile)):
    try:
        os.makedirs(os.path.dirname(resultFile))
    except OSError as exc: # Guard against race condition
        if exc.errno != errno.EEXIST:
            raise
        
with open(resultFile, 'w+') as fp:
    fp.write('Mot;;Nb Apparition Titre;Nb Rep total Titre ;Moy Rep/App Titre;;Nb Apparition Contenu;Nb Rep total Contenu;Moy Rep/App Contenu;RepAll\n')
    for i in range(len(listeFinale)):
        fp.write(listeFinale[i][0] + ";;"+ str(listeFinale[i][1]) + ";"+ str(listeFinale[i][2]) + ";"+str(listeFinale[i][3]).replace(".",",")+ ";;"+ str(listeFinale[i][4]) + ";"+ str(listeFinale[i][5]) + ";"+str(listeFinale[i][6]).replace(".",",")+ ";"+str(listeFinale[i][7]).replace(".",",")+"\n")
    
print("   > OK\n")
end = datetime.now()
time_taken = end - start
print('___ Total Execution Time : ',time_taken)
print("___ Output file in : " + resultFile)
print("#################################################")
