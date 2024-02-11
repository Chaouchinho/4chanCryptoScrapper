@echo off 
set board=biz


cd C:\4Chan\4Chan\prog
py 4chanAnalyse.py %board%

cd C:\4Chan\getCryptoFrom4chan\prog
py merge4chanCrypto.py %board%

