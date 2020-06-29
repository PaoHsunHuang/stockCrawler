from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
import time

def myCast(str):
    #remove ',' in string make it nunber
    a = str.split(',')
    ret = ""
    for ele in a:
        ret += ele
    return ret

def checkVolume(url):
    #get html
    html = requests.get(url).text
    root = BeautifulSoup(html, "html.parser")

    #read volume, and strike
    volume = root.find_all("td", class_ = "data-col8")
    strike = root.find_all("a", class_ = "C($linkColor) Fz(s)")

    #if data exist
    if volume and strike:
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
            numS = float(myCast(strS))
            if numS > last:
                last = numS
            else:
                type = "put"

            #calculate total volume, for calculate avg
            strV = str(eleV.text)
            if strV != '-':
                numV = int(myCast(strV))
                if type == "call":
                    totalC += numV
                else:
                    totalP += numV
            else:
                numV = 0

            #put data into dictionary
            if type == "call":
                countC += 1
                dictC[numS] = numV
            else:
                countP += 1
                dictP[numS] = numV

        #calculate avg
        avgC = totalC / countC
        avgP = totalP / countP
        rangeC = avgC * Multiply
        rangeP = avgP * Multiply

        #output result
        print("AVG for call is " + str(round(rangeC, 2)))
        for key in dictC:
            if dictC[key] > rangeC:
                print("Call " + str(key) + " " + str(dictC[key]))

        print("AVG for put is " + str(round(rangeP, 2)))
        for key in dictP:
            if dictP[key] > rangeP:
                print("Put " + str(key) + " " + str(dictP[key]))
        print("================================================")

    #if this date is not exist, print error message
    else:
        print("Date not exist")
        print("================================================")
        return




#THIS IS THE START OF THE PROGRAM

#get current time, calcualte next friday
#use next 4 week of friday to run
cur = time.time()
oneWeekUnix = 604800
nextFriday = 1592524800

company = input("Enter Stock Code:")
while nextFriday < cur:
    nextFriday += oneWeekUnix

timeList = []
for i in range(4):
    timeList.append(str(nextFriday))
    nextFriday += oneWeekUnix
i = 1;
print("Check company " + company)
for ele in timeList:
    url = "https://finance.yahoo.com/quote/"
    url += company
    url += "/options?date="
    url += ele
    print("WEEK" + str(i))
    i += 1
    checkVolume(url)



input("\nPress anything to exit")
