from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup

#download html
url = "https://finance.yahoo.com/quote/FB/options?date=1605830400&p=FB"
html = requests.get(url).text

#parse data
root = BeautifulSoup(html, "html.parser")

#read all volume
volume = root.find_all("td", class_ = "data-col8")
strike = root.find_all("a", class_ = "C($linkColor) Fz(s)")

totalC = 0
countC = 0
totalP = 0
countP = 0
last = 0

dictP = {}
dictC = {}
Multiply = 5

type = "call"
for eleV, eleS in zip(volume, strike):
    #chagne between put and call
    strS = str(eleS.string)
    numS = float(strS)
    if numS > last:
        last = numS
    else:
        type = "put"

    #calculate volume
    strV = str(eleV.text)
    if strV != '-':
        numV = int(strV)
        if type == "call":
            totalC += numV
        else:
            totalP += numV
    else:
        numV = 0

    #put data into dict
    if type == "call":
        countC += 1
        dictC[numS] = numV
    else:
        countP += 1
        dictP[numS] = numV

#print("Call AVG: " + str(totalC / countC))
#print("Put AVG: " + str(totalP / countP))
avgC = totalC / countC
avgP = totalP / countP
rangeC = avgC * Multiply
rangeP = avgP * Multiply

print("AVG for call is " + str(rangeC))
for key in dictC:
    if dictC[key] > rangeC:
        print("Call " + str(key) + " " + str(dictC[key]))

print("================================================")
print("AVG for put is " + str(rangeP))
for key in dictP:
    if dictP[key] > rangeP:
        print("Call " + str(key) + " " + str(dictP[key]))

#stop program
input("\nPress anything to exit")
