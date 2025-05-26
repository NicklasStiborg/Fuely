#imports
import scrapy as scy
from scrapy import Selector
import requests
import json
import datetime as dt
from datetime import datetime
from dateutil.relativedelta import relativedelta
from string import Template
import database
import time

headers = {
    "Content-Type": "application/json"
}

#Scraping and requesting
providers = {
    "shell": {
        "api": "yes",
        "payload": "no",
        "link": "https://shellservice.dk/wp-json/shell-wp/v2/daily-prices",
        "95": {
            'payload': '',
            'path': [
                'results',
                'products',
                0,
                'price_incl_vat'
            ],
        },
        "D": {
            'payload': '',
            'path': [
                'results',
                'products',
                2,
                'price_incl_vat'
            ],
        },
    },
    "ck": {
        "api": "no",
        "payload": "no",
        "link": "https://www.circlek.dk/priser",
        "95": "/html/body/div[1]/main/div/div/article/div/div[2]/div/div/div[2]/div/div[3]/div/div/table/tbody/tr[1]/td[3]/div/text()",
        "D": "/html/body/div[1]/main/div/div/article/div/div[2]/div/div/div[2]/div/div[3]/div/div/table/tbody/tr[3]/td[3]/div/text()",
    },
    "q8": {
        "api": "no",
        "payload": "no",
        "link": "https://www.q8.dk/priser/",
        "95": "/html/body/main/article[3]/div/div/div/div/ul/li[1]/div/text()",
        "D": "/html/body/main/article[3]/div/div/div/div/ul/li[2]/div/text()",
    },
    "ok": {
        "api": "no",
        "payload": "no",
        "link": "https://www.ok.dk/privat/produkter/benzinkort/benzinpriser",
        "95": "/html/body//div[@id='d6e03ece6a51429dbf4fbb13b4fc69ce']//div[@class='flex-table__cell cell--val hidden-xs']/text()",
        "D": "/html/body//div[@id='891cf20738b3425aaad10914184ed690']//div[@class='flex-table__cell cell--val hidden-xs']/text()",
    },
    "ingo": {
        "api": "no",
        "payload": "no",
        "link": "https://www.ingo.dk/",
        "95": "/html/body/div[1]/main/div/div/article/div/div/div[4]/div/div[1]/article/div/div[1]/div/table/tbody/tr[1]/td[3]/div/text()",
        "D": '/html/body/div[1]/main/div/div/article/div/div/div[4]/div/div[1]/article/div/div[1]/div/table/tbody/tr[2]/td[3]/div/text()',
    }
}

class getDataClass:
    def __init__(self):
        self.data = []
     
    def pathGet(self, dictionary, path):
        for item in path:
            dictionary = dictionary[item]
        return dictionary

    def conn(self, providerId):
        link = (providers[providerId]["link"])
        responsetxt = requests.get(link)
        return responsetxt
 
    def currentTime(self):
        currentTimeDt = datetime.today()
        currentTimeWOS = dt.datetime.replace(currentTimeDt,second=0, microsecond=0)
        currentTimeTs = datetime.timestamp(currentTimeWOS)
        currentTimeTs = int(currentTimeTs)
        return currentTimeTs

    def payload(self, providerId, gType):
        oneMonthTime = self.oneMonthTime()
        currentTime = self.currentTime()
        payload = Template(providers[providerId][gType]['payload']).substitute(d1=oneMonthTime, d2=currentTime)
        return payload

    #API method
    def getm1(self, providerId, gType, payload="no"):
        link = (providers[providerId]["link"])
        r = providers[providerId][gType]['path']
        if payload == "yes":
            payload = self.payload(providerId, gType)
            request = requests.post(link, json=json.loads(payload), headers=headers)
        else:
            request = requests.get(link, headers=headers)
        responseReturn = request.json()
        valueOfGtype = self.pathGet(responseReturn, r)
        return valueOfGtype

    #Webscraping method
    def getm2(self, providerId, gType):
        link = (providers[providerId]["link"])
        response = requests.get(link).content
        sel = Selector(text=response)
        priceList = sel.xpath(providers[providerId][gType]).extract()
        price = priceList[0]
        return price.strip()

class Provider:
    def __init__(self, name, unleaded, diesel):
        self.name = name
        self.unleaded = unleaded
        self.diesel = diesel

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)

getData = getDataClass()
#Write to db
ts = time.time()
ts = int(ts)

conn = database.connect()
print(conn)

for i in providers:
    print(i)
    #if yes use api
    if providers[i]["api"] == "yes":
        #if yes use payload
        if providers[i]["payload"] == "yes":
            j = Provider(i, getData.getm1(i, "95", "yes"), getData.getm1(i, "D", "yes"))
        else:
        #default will be no    
            j = Provider(i, getData.getm1(i, "95"), getData.getm1(i, "D"))
        j_95 = getData.getm1(i, "95")
        j_D = getData.getm1(i, "D")
    else:
        if i == "ingo" or "ok":
            j = Provider(i, getData.getm2(i, "95")[:5], getData.getm2(i, "D")[:5])
        else: 
            j = Provider(i, getData.getm2(i, "95"), getData.getm2(i, "D"))
        j_95 = getData.getm2(i, "95")
        j_D = getData.getm2(i, "D")
    database.addData(conn, ts, i, j_95, j_D)
