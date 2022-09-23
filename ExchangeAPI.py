from abc import ABC, abstractmethod
import xml.etree.ElementTree as ET
import requests
from requests_html import HTMLSession

class exchangeAPI(ABC):
    
    @abstractmethod
    def getHistoricExchange(self,day,month,year):
        pass
    
    @abstractmethod
    def currentExchange(self):
        pass


class TCMBExchange(exchangeAPI):
    
    def __init__(self):
        self.name = "TCMB"
        self.daily = "https://www.tcmb.gov.tr/kurlar/today.xml"
        self.historic_base = "http://www.tcmb.gov.tr/kurlar/"

    def currentExchange(self):
        try:
            r = requests.get(self.daily)
            root = ET.fromstring(r.text)
            rates = {}
            for cur in root.findall("Currency"):
                code = cur.get("Kod")
                rate = cur.find("ForexBuying").text
                rates[code] = rate
            
            return rates
        except:
            return {"Error":"Holiday"}

    def getHistoricExchange(self,day, month, year):
        if day // 10 == 0:
            day = "0" + str(day)

        if month // 10 == 0:
            month = "0" + str(month)

        
        url = self.historic_base + str(year) + str(month) + "/" + str(day) + str(month) + str(year) + ".xml"
        try:
            r = requests.get(url)
            
            root = ET.fromstring(r.text)
            rates = {}
            for cur in root.findall("Currency"):
                code = cur.get("Kod")
                rate = cur.find("ForexBuying").text
                rates[code] = float(rate)
            
            return rates
        
        except:
            return {"Error":"Holiday"}

class xRatesExchange(exchangeAPI):

    def __init__(self):
        self.name = "xRates"

        self.histoic_url = "https://www.x-rates.com/historical/?from=TRY&amount=1&date="
        self.USD_path = '//*[@id="content"]/div[1]/div/div[1]/div[1]/table[1]/tbody/tr[1]/td[3]/a'
        self.EUR_path = '//*[@id="content"]/div[1]/div/div[1]/div[1]/table[1]/tbody/tr[2]/td[3]/a' 
        
        self.cur_USD_url = "https://www.x-rates.com/calculator/?from=USD&to=TRY&amount=1"
        self.cur_EUR_url = "https://www.x-rates.com/calculator/?from=EUR&to=TRY&amount=1"
        self.cur_path = '//*[@id="content"]/div[1]/div/div[1]/div/div/span[2]'

        

    def currentExchange(self):
        try:
            session = HTMLSession()
            usd_response = session.get(self.cur_USD_url)
            eur_response = session.get(self.cur_EUR_url)

        except requests.exceptions.RequestException as e:
            print(e)
            return {"error":e}

        usd = usd_response.html.xpath(self.cur_path)
        eur = eur_response.html.xpath(self.cur_path)

        return({"USD":float(usd[0].text.split()[0]),"EUR":float(eur[0].text.split()[0])})

    def getHistoricExchange(self, day, month, year):
        if day // 10 == 0:
            day = "0" + str(day)

        if month // 10 == 0:
            month = "0" + str(month)
        
        url = self.histoic_url + str(year) + "-" + str(month) + "-" + str(day)
        try:
            session = HTMLSession()
            response = session.get(url)
     
        except requests.exceptions.RequestException as e:
            print(e)
            return {"error":e}

        usd = response.html.xpath(self.USD_path)
        eur = response.html.xpath(self.EUR_path) 

        return {"USD":float((usd[0].text.split()[0])),"EUR": float(eur[0].text.split()[0])}

