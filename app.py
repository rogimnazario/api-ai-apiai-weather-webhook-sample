#!/usr/bin/env python

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os

from flask import Flask, request, make_response, jsonify

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['GET','POST'])
def webhook():   
    print("Antes de ler o request.")
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(req)
    print(req.get("result").get("action"))
    
    return json.dumps({
        "speech": "10",
        "displayText": "Assim 10",
        # "data": data,
        # "contextOut": [],
        "source": "boi-magia"
    })


def processRequest(req):
    if req.get("result").get("action") != "quantosUsuarios":
        return {}
    baseurl = "https://reqres.in/api"
    yql_query = makeYqlQuery(req)
    if yql_query is None:
        return {}
    yql_url = baseurl + urlencode({'per_page': yql_query})
    result = urlopen(yql_url).read()
    data = json.loads(result)
    res = makeWebhookResult(data)
    return res


def makeYqlQuery(req):
    result = req.get("result")
    parameters = result.get("parameters")
    qtd = parameters.get("qtd-user")
    if qtd is None:
        return None

    return 10 #"select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='" + city + "') and u='c'"


def makeWebhookResult(data):
    query = data.get('data')
    if query is None:
        return {}

    speech = "Retorno: " + query

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "webhook-rrn4"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
