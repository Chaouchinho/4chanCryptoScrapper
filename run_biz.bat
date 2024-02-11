@echo off 
set board=biz


cd C:\4Chan\4Chan\prog
py -3.10 4chanAnalyse.py %board%

cd C:\4Chan\getCryptoFrom4chan\prog
py -3.10 merge4chanCrypto.py %board%

cd C:\4Chan\TelegramBot
py -3.10 sendOnly.py %board%

