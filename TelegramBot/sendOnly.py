#pip install python-telegram-bot==13.13
import telegram
import sys
from datetime import datetime, timedelta
import csv
import glob, os
import subprocess


if len(sys.argv) > 1:
    board = sys.argv[1]
else:
    board = 'biz'

TOKEN = '6014410276:AAHOKy8na_McYbejQLwMv8iqUDb5ZukUh80'
ForchanFolder = "..\\4chan\\result\\board\\"+board+"\\merged"


def getMostResentFileInFolder(folderPath, extension):
    return glob.glob(folderPath+ "\\*." + extension)[len(glob.glob(folderPath+ "\\*."+extension))-1]

def sendLast(bot, chat_id):
    try:
        file_name = getMostResentFileInFolder(ForchanFolder, "csv")
        document = open(file_name, 'rb')
        bot.sendMessage(chat_id=chat_id, text="Un scrapping auto viens de se finir")
        bot.send_document(chat_id, document)
    except:
        bot.sendMessage(chat_id=chat_id, text="Le scraping viens de se finir, mais impossible d'envoyer le fichier, merci de faire un /getLast")
        

chat_id = "-727368095"
#chat_id="5086044569"  #Sohib
bot = telegram.Bot(token=TOKEN)

sendLast(bot, chat_id)
