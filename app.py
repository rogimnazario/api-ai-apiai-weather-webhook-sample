#!/usr/bin/env python

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os

import operator

from flask import Flask, request, make_response, jsonify

# Flask app should start in global layout
app = Flask(__name__)
ops = { "+": operator.add, "-": operator.sub,"/": operator.div,"*":operator.mul }

@app.route('/webhook', methods=['GET','POST'])
def webhook():   
    req = request.get_json(force=True)
    
    num1 = req.get("result").get("parameters").get("number-integer") #retorna um array
    num2 = req.get("result").get("parameters").get("number-integer1")    
    operador = req.get("signal")
    
    result = ops[operador](num1[0],num2[0])
    
    return json.dumps({
        "speech": result,
        "displayText": result,
        # "data": data,
        # "contextOut": [],
        "source": "boi-magia"
    })


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
