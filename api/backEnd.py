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

#Scraping and requesting

providers = {
    "shell": {
        "link": "https://www.shell.dk/customer-service/priser-pa-benzin-og-diesel.html",
        "95": "/html/body/div[1]/main/div/div/div[2]/div/div/div/div/div/table/tbody/tr[2]/td[7]/text()",
        "D": "/html/body/div[1]/main/div/div/div[2]/div/div/div/div/div/table/tbody/tr[4]/td[7]/text()",
    },
    "ck": {
        "link": "https://www.circlek.dk/priser",
        "95": "/html/body/div[2]/main/div/div/article/div/div[2]/div/div[2]/div/div[3]/div/div/table/tbody/tr[1]/td[3]/div/span/following-sibling::text()",
        "D": "/html/body/div[2]/main/div/div/article/div/div[2]/div/div[2]/div/div[3]/div/div/table/tbody/tr[3]/td[3]/div/span/following-sibling::text()",
    },
    "q8": {
        "link": "https://www.q8.dk/-/api/PriceViewProduct/GetPriceViewProducts",
        "95": {
            'payload': '{"FuelsIdList":[{"ProductCode":"22251"}],"FromDate":${d1},"ToDate":${d2}}',
            'path': [
                'Products',
                0,
                'PriceInclVATInclTax'
            ],
        },
        "D": {
            'payload': '{"FuelsIdList":[{"ProductCode":"24451"}],"FromDate":${d1},"ToDate":${d2}}',
            'path': [
                'Products',
                0,
                'PriceInclVATInclTax'
            ],
        },
    },
     "f24": {
        "link": "https://www.q8.dk/-/api/PriceViewProduct/GetPriceViewProducts",
        "95": {
            'payload': '{"FuelsIdList":[{"ProductCode":"22251"}],"FromDate":${d1},"ToDate":${d2}}',
            'path': [
                'Products',
                0,
                'PriceInclVATInclTax'
            ],
        },
        "D": {
            'payload': '{"FuelsIdList":[{"ProductCode":"24451"}],"FromDate":${d1},"ToDate":${d2}}',
            'path': [
                'Products',
                0,
                'PriceInclVATInclTax'
            ],
        },
    },
    "ok": {
        "link": "https://www.ok.dk/privat/produkter/benzinkort/benzinpriser",
        "95": "/html/body//div[@id='d6e03ece6a51429dbf4fbb13b4fc69ce']//div[@class='flex-table__cell cell--val hidden-xs']/text()",
        "D": "/html/body//div[@id='891cf20738b3425aaad10914184ed690']//div[@class='flex-table__cell cell--val hidden-xs']/text()",
    },
    "ingo": {
        "link": "https://www.ingo.dk/",
        "95": "/html/body/div[1]/main/div/div/article/div/div/div[4]/div/div[1]/article/div/div[1]/div/table/tbody/tr[2]/td[3]/div/text()",
        "D": '/html/body/div[1]/main/div/div/article/div/div/div[4]/div/div[1]/article/div/div[1]/div/table/tbody/tr[5]/td[3]/div/text()',
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

    def oneMonthTime(self):
        one_month = datetime.today() + relativedelta(months=-1)
        one_monthWOS = dt.datetime.replace(one_month,second=0, microsecond=0)
        one_monthTs = datetime.timestamp(one_monthWOS)
        one_monthTs = int(one_monthTs)
        return one_monthTs

    def payload(self, providerId, gType):
        oneMonthTime = self.oneMonthTime()
        currentTime = self.currentTime()
        payload = Template(providers[providerId][gType]['payload']).substitute(d1=oneMonthTime, d2=currentTime)
        return payload

    def getm1(self, providerId, gType):
        payload = self.payload(providerId, gType)
        link = (providers[providerId]["link"])
        r = providers[providerId][gType]['path']
        request = requests.post(link, json=json.loads(payload))
        responseReturn = request.json()
        valueOfGtype = self.pathGet(responseReturn, r)
        return valueOfGtype

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

print("Shell: " + str(getData.conn('shell')))
print("Circle K: " + str(getData.conn('ck')))
print("Q8: " + str(getData.conn('q8')))
print("F24: " + str(getData.conn('f24')))
print("OK: " + str(getData.conn('ok')))
print("Ingo: " + str(getData.conn('ingo')))

shell = Provider("Shell", getData.getm2("shell", "95"), getData.getm2("shell", "D"))
shell_95 = getData.getm2("shell", "95")
shell_D = getData.getm2("shell", "D")

ck = Provider("Circle K", getData.getm2("ck", "95"), getData.getm2("ck", "D"))
ck_95 = getData.getm2("ck", "95")
ck_D = getData.getm2("ck", "D")

q8 = Provider("Q8", getData.getm1("q8", "95"), getData.getm1("q8", "D"))
q8_95 = getData.getm1("q8", "95")
q8_D = getData.getm1("q8", "D")

f24 = Provider("F24", getData.getm1("f24", "95"), getData.getm1("f24", "D"))
f24_95 = getData.getm1("f24", "95")
f24_D = getData.getm1("f24", "D")

ok = Provider("OK", getData.getm2("ok", "95")[:5], getData.getm2("ok", "D")[:5])
ok_95 = getData.getm2("ok", "95")[:5]
ok_D = getData.getm2("ok", "D")[:5]

ingo = Provider("Ingo", getData.getm2("ingo", "95")[:5], getData.getm2("ingo", "D")[:5])
ingo_95 = getData.getm2("ingo", "95")[:5]
ingo_D = getData.getm2("ingo", "D")[:5]

providersListed = [shell, ck, q8, f24, ok, ingo]

providersDTO = json.dumps([ob.__dict__ for ob in providersListed])
print(providersDTO)


#Write to db
ts = time.time()
ts = int(ts)

conn = database.connect()
#(connection, date, provider_name, price_95, price_d)
def shellAdd():
    database.addData(conn, ts, 'Shell', shell_95, shell_D)

def ckAdd():
    database.addData(conn, ts, 'Circle K', ck_95, ck_D)

def q8Add():
    database.addData(conn, ts, 'Q8', q8_95, q8_D)

def f24Add():
    database.addData(conn, ts, 'F24', f24_95, f24_D)

def okAdd():
    database.addData(conn, ts, 'OK', ok_95, ok_D)

def ingoAdd():
    database.addData(conn, ts, 'Ingo', ingo_95, ingo_D)

def addAll():
    database.addData(conn, ts, 'Shell', shell_95, shell_D)
    database.addData(conn, ts, 'Circle K', ck_95, ck_D)
    database.addData(conn, ts, 'Q8', q8_95, q8_D)
    database.addData(conn, ts, 'F24', f24_95, f24_D)
    database.addData(conn, ts, 'OK', ok_95, ok_D)
    database.addData(conn, ts, 'Ingo', ingo_95, ingo_D)

def getAll():
    database.getAll(conn)

def create():
    database.createTables(conn)

getAll()