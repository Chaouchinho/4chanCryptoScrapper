#pip install python-telegram-bot==13.13
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import sys
from datetime import datetime, timedelta
import csv
import glob, os
import subprocess

TOKEN = '6014410276:AAHOKy8na_McYbejQLwMv8iqUDb5ZukUh80'
board = "biz"
ForchanFolder = "..\\4chan\\result\\board\\"+board+"\\merged"

def start(update, context):
    update.message.reply_text("""
Bienvenue sur le bot de crypto Team

Les commandes disponibles sont :

- /getLast pour recuperer le dernier fichier de scrapping au format CSV (board /biz)

- /getTimeLastScrap pour connaitre la date du dernier scrapping (board /biz)

- /getTimeNextScrap pour connaitre la date du prochain scrapping (board /biz)

- /runAndGet pour lancer un scrap maintenant
    """)


def getMostResentFileInFolder(folderPath, extension):
    return glob.glob(folderPath+ "\\*." + extension)[len(glob.glob(folderPath+ "\\*."+extension))-1]

def getLast(update, context):
    try:
        chat_id = update.message.chat_id
        file_name = getMostResentFileInFolder(ForchanFolder, "csv")
        document = open(file_name, 'rb')
        context.bot.send_document(chat_id, document)
    except:
        update.message.reply_text('Impossible de recuperer le dernier fichier')

def getTimeLastScrap(update, context):
    try:
        chat_id = update.message.chat_id
        file_name = getMostResentFileInFolder(ForchanFolder, "csv")
        lastDate = datetime.fromtimestamp(os.path.getmtime(file_name)).strftime('%Y-%m-%d à %H:%M')
        update.message.reply_text('Le scrap le plus recent a été recuper le ' + lastDate)
    except:
        update.message.reply_text('Impossible de recuperer le dernier fichier')

def getTimeNextScrap(update, context):
    try:
        chat_id = update.message.chat_id
        file_name = getMostResentFileInFolder(ForchanFolder, "csv")
        nextDate = (datetime.fromtimestamp(os.path.getmtime(file_name)) + timedelta(hours=6)).strftime('%Y-%m-%d à %H:%M')
        update.message.reply_text('Le prochain scrap sera le ' + nextDate)
    except:
        update.message.reply_text('Impossible de recuperer le dernier fichier')

def runAndGet(update, context):
    try:
        chat_id = update.message.chat_id
        file_name = getMostResentFileInFolder(ForchanFolder, "csv")
        lastDate = datetime.fromtimestamp(os.path.getmtime(file_name)).strftime('%Y-%m-%d à %H:%M')
        update.message.reply_text('Le scrap le plus recent a été recuperer le ' + lastDate + '\n\nEtes-vous sur de vouloir lancer un scrapping maintenant ?\n\n/YesRun or /DontRun')
    except:
        update.message.reply_text('Impossible de recuperer le dernier fichier')

def yesRun(update, context):
    update.message.reply_text('La commande de Scrap vient d\'etre envoyé, le fichier sera disponible d\'ici 2 min\n\nJe te l\'envoi des que j\'ai fini de scrapper')
    subprocess.call(['C:\\4Chan\\run_biz_only.bat'])
    update.message.reply_text('Le scrapping est fini, voila le fichier')
    getLast(update, context)


def dontRun(update, context):
    update.message.reply_text('Sage decision, La patience est la vertu du juste et des hodlers')
    

def pas_compris(update, context):
    update.message.reply_text('Je n\'ai pas compris votre message')


def kdamien(update, context):
    update.message.reply_text('200k vont etre envoyé sur le wallet de Damien')

    

def main():
    # La classe Updater permet de lire en continu ce qu'il se passe sur le channel
    updater = Updater(TOKEN, use_context=True)

    # Pour avoir accès au dispatcher plus facilement
    dp = updater.dispatcher

    # On ajoute des gestionnaires de commandes
    # On donne a CommandHandler la commande textuelle et une fonction associée
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("getLast", getLast))
    dp.add_handler(CommandHandler("getTimeLastScrap", getTimeLastScrap))
    dp.add_handler(CommandHandler("getTimeNextScrap", getTimeNextScrap))
    dp.add_handler(CommandHandler("runAndGet", runAndGet))

    dp.add_handler(CommandHandler("DontRun", dontRun))
    dp.add_handler(CommandHandler("YesRun", yesRun))

    dp.add_handler(CommandHandler("send200kDamien", kdamien))


    # Pour gérer les autres messages qui ne sont pas des commandes
    dp.add_handler(MessageHandler(Filters.text, pas_compris))

    # Sert à lancer le bot
    updater.start_polling()

    # Pour arrêter le bot proprement avec CTRL+C
    updater.idle()


if __name__ == '__main__':
    main()
