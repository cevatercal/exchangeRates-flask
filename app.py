from flask import Flask,jsonify
from ExchangeAPI import TCMBExchange,xRatesExchange

app = Flask(__name__)

apis = []
#new apis can be added here
apis.append(TCMBExchange())
apis.append(xRatesExchange())

@app.route("/today/EUR")
def currentEUR():
    name = ""
    lowest = 10**10
    for api in apis:
        rates = api.currentExchange()
        
        if float(rates["EUR"]) < lowest:
            lowest = float(rates["EUR"])
            name = api.name
    
    return jsonify(serviceName = name, rate = lowest)

@app.route("/today/USD")
def currentUSD():
    name = ""
    lowest = 10**10
    for api in apis:
        rates = api.currentExchange()
        if float(rates["USD"]) < lowest:
            lowest = float(rates["USD"])
            name = api.name
    
    return jsonify(serviceName = name, rate = lowest) 

@app.route("/historic/<day>-<month>-<year>")
def historicExchange(day,month,year):
    result = {}
    for api in apis:
        rates = api.getHistoricExchange(int(day), int(month), int(year))
        
        if len(rates) == 1:
            return jsonify(rates)
        rate = {}
        rate["USD"] = float(rates["USD"])
        rate["EUR"] = float(rates["EUR"])
        result[api.name] = rate

    return jsonify(result)

