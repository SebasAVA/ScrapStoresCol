# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 12:46:40 2020

@author: User
"""


from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Domo Arigato Mr Roboto'
import requests
import re
from bs4 import BeautifulSoup
from firebase import firebase
import time


def concatenate_list_data(list):
    result= ''
    for element in list:
        result += str(element)
    return result


firebase = firebase.FirebaseApplication('https://pika-4af18.firebaseio.com/', None)
IdsFala = firebase.get('/store/falabella/', None)

IdsInfo = firebase.get('/prices/falabella/', None)

            
for key in IdsFala: 
    if not key in IdsInfo: 
        URL = 'https://www.falabella.com.co/falabella-co/product/'+key
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
    
        results = soup.find(id='testId-pod-prices-'+key)
        print(results.prettify())
    
        
        ProductName = soup.find('div', class_='jsx-3686231685 product-name fa--product-name')
        try:
            ProductName=ProductName.text.strip()
        except:
            print("No tiene nombre el producto")
        
        data =  { 'Name': ProductName,
                  'Url': URL,
                  'ProductId':key
                  }
        firebase.put('/prices/falabella/',key,data)
        print(key) 
    

for ProductId in IdsFala:
    URL = 'https://www.falabella.com.co/falabella-co/product/'+ProductId
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')

    results = soup.find(id='testId-pod-prices-'+ProductId)
    print(results.prettify())

    
    ProductName = soup.find('div', class_='jsx-3686231685 product-name fa--product-name')
    try:
        ProductName=ProductName.text.strip()
    except:
        print("No tiene nombre el producto")
    
    
    price_normal= results.find('span',class_='copy13 primary high jsx-185326735 normal')
    try:
        price_normal = price_normal.text.strip()
        priceN = (re.findall('\d+', price_normal ))
        price_Normal = int(concatenate_list_data(priceN))
    except:
        print("No hay precio del producto")
    
    price_disc = results.find('span',class_='copy1 primary jsx-185326735 normal')
    try:
        price_disc = price_disc.text.strip()
        priceD = (re.findall('\d+', price_disc ))
        price_disc = int(concatenate_list_data(priceD))
    except:
        print("No tiene precio de descuento")
        
    disc = soup.find('div', class_='jsx-1231170568 pod-badges pod-badges-PDP')
    try:
        disct = disc.text.strip()
        dis = (re.findall('\d+', disct ))
        disct = int(concatenate_list_data(dis))
    except:
        print("No tiene valor de de descuento")
    timeStamp = int(time.time())
    data =  { 'Date': timeStamp,
              'ActualPrice': price_Normal,
              'NoDiscPrice':price_disc,
              'Discount': disct
                  }
    firebase.put('/prices/falabella/'+ProductId+'/Dates/',timeStamp,data)
