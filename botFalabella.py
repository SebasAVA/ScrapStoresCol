# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 13:51:29 2020

@author: User
"""



def concatenate_list_data(list):
    result= ''
    for element in list:
        result += str(element)
    return result

def runBot():
    import requests
    import re
    from bs4 import BeautifulSoup
    from firebase import firebase
    import time

    fire = firebase.FirebaseApplication('https://pika-4af18.firebaseio.com/', None)
    IdsFala = fire.get('/store/falabella/', None)
    
    IdsInfo = fire.get('/prices/falabella/', None)
    
                
    for key in IdsFala: 
        if not key in IdsInfo: 
            URL = 'https://www.falabella.com.co/falabella-co/product/'+key
            page = requests.get(URL)
            soup = BeautifulSoup(page.content, 'html.parser')
            results = soup.find(id='testId-pod-prices-'+key)
        
            
            ProductName = soup.find('div', class_='jsx-3686231685 product-name fa--product-name')
            try:
                ProductName=ProductName.text.strip()
            except:
                print("No tiene nombre el producto")
            
            data =  { 'name': ProductName,
                      'url': URL,
                      'productId':key
                      }
            fire.put('/prices/falabella/',key,data)
            print(key) 
        
    
    for ProductId in IdsFala:
        URL = 'https://www.falabella.com.co/falabella-co/product/'+ProductId
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        try:
            results = soup.find(id='testId-pod-prices-'+ProductId)
            ProductName = soup.find('div', class_='jsx-3686231685 product-name fa--product-name')
            print(results.prettify())
        except:
            print("No hay precio del producto")


        try:
            ProductName=ProductName.text.strip()
        except:
            print("No tiene nombre el producto")
        
        try:
            price_normal= results.find('span',class_='copy13 primary high jsx-185326735 normal')
        except:
            print("No hay precio del producto")
        try:
            price_normal = price_normal.text.strip()
            priceN = (re.findall('\d+', price_normal ))
            price_Normal = int(concatenate_list_data(priceN))
        except:
            print("No hay precio del producto")
            
        try:    
            price_disc = results.find('span',class_='copy1 primary jsx-185326735 normal')
        except:
            print("No tiene precio de descuento")
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
        data =  { 'date': timeStamp,
                  'actualPrice': price_Normal,
                  'noDiscPrice':price_disc,
                  'discount': disct
                      }
        fire.put('/prices/falabella/'+ProductId+'/dates/',timeStamp,data)
