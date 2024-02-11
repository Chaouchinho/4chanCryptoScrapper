##### GET COIN MARKET CAP ######

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from datetime import datetime

start = datetime.now()
now = datetime.now().strftime("%Y%m%d_%H%M%S")
resultFile = "..\\result\getCoin_"+now+".csv"
roundingAfterComma = 5
url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
  'start':'1',
  'limit':'5000',
  'convert':'USD'
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': '3d6aac58-e8e3-4a9c-8b65-78b34b489e93',
}


print("#################################################")
print("##########  GET DATA FROM COINMARKETCAP #########")
print("#################################################")
print("")
print("Running request to get data from CoinMarketCap....")

session = Session()
session.headers.update(headers)

try:
  response = session.get(url, params=parameters)
  data = json.loads(response.text)

  with open(resultFile, 'w+', encoding="utf8") as fp:
      fp.write("CoindID;CoinName;CoinLetters;CoinValue;" + "\n")

      for elem in data["data"]:   
        fp.write( str(elem["id"]) + ";"+ str(elem["name"])+ ";"+str(elem["symbol"])+ ";"+str(round(elem["quote"]["USD"]["price"], roundingAfterComma)).replace(".",",") +";\n" )

  print("   > OK") 
except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)
  print("   > KO")



