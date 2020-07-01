# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 12:46:40 2020

@author: User
"""
from botFalabella import runBot
import request

from flask import Flask
app = Flask(__name__)

@app.route('/scrapBot')
def hello_world():
    runBot()
    return 'Domo Arigato Mr Roboto'
"""
@app.route('/addProduct',methods=['POST'])
def testFun():
    content = request.get_json(silent=True)
    print(content)
    return 'Test'
"""
