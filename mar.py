import requests
from time import sleep
import bs4
from bs4 import BeautifulSoup
import re
import json
import csv
from datetime import datetime
import pandas as pd
import random

import arrow


# with open("temp.csv",'a',encoding='utf-8',newline = "") as newcsv:
#     writer = csv.writer(newcsv)


proxy = pd.read_csv("prox.csv")
proxiesToList = proxy.values.tolist()
def getReq():
    firstTime = True
    try:
        df = pd.read_csv("temp.csv")
               
        firstTime = False
    except:
        df = pd.DataFrame({"Time":[],"Ticker":[],"Headline":[]}).astype(str)
    
    
    headers = {
    'authority': 'marketchameleon.com',
    'x-mobdisp': 'false',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'x-requested-with': 'XMLHttpRequest',
    'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
    'origin': 'https://marketchameleon.com',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://marketchameleon.com/PressReleases',
    'accept-language': 'en-US,en;q=0.9',
    }

    params = (
        ('keywordHighlightClass', 'pr_keyword_highlight'),
    )

    data = {
    'draw': '1',
    'columns[0][data]': 'Symbol',
    'columns[0][name]': 'Symbol',
    'columns[0][searchable]': 'true',
    'columns[0][orderable]': 'true',
    'columns[0][search][value]': '',
    'columns[0][search][regex]': 'false',
    'columns[1][data]': 'Price',
    'columns[1][name]': 'Price',
    'columns[1][searchable]': 'true',
    'columns[1][orderable]': 'true',
    'columns[1][search][value]': '',
    'columns[1][search][regex]': 'false',
    'columns[2][data]': 'PricePctChg',
    'columns[2][name]': 'PricePctChg',
    'columns[2][searchable]': 'true',
    'columns[2][orderable]': 'true',
    'columns[2][search][value]': '',
    'columns[2][search][regex]': 'false',
    'columns[3][data]': 'Headline',
    'columns[3][name]': 'Headline',
    'columns[3][searchable]': 'true',
    'columns[3][orderable]': 'true',
    'columns[3][search][value]': '',
    'columns[3][search][regex]': 'false',
    'columns[4][data]': 'PressReleaseDate',
    'columns[4][name]': 'PressReleaseDate',
    'columns[4][searchable]': 'true',
    'columns[4][orderable]': 'true',
    'columns[4][search][value]': '',
    'columns[4][search][regex]': 'false',
    'columns[5][data]': 'PressReleaseFeedView',
    'columns[5][name]': 'PressReleaseFeedView',
    'columns[5][searchable]': 'true',
    'columns[5][orderable]': 'true',
    'columns[5][search][value]': '',
    'columns[5][search][regex]': 'false',
    'columns[6][data]': 'HasOptions',
    'columns[6][name]': 'HasOptions',
    'columns[6][searchable]': 'true',
    'columns[6][orderable]': 'true',
    'columns[6][search][value]': '',
    'columns[6][search][regex]': 'false',
    'columns[7][data]': 'InETF',
    'columns[7][name]': 'InETF',
    'columns[7][searchable]': 'true',
    'columns[7][orderable]': 'true',
    'columns[7][search][value]': '',
    'columns[7][search][regex]': 'false',
    'columns[8][data]': 'MarketCap',
    'columns[8][name]': 'MarketCap',
    'columns[8][searchable]': 'true',
    'columns[8][orderable]': 'true',
    'columns[8][search][value]': '',
    'columns[8][search][regex]': 'false',
    'columns[9][data]': 'InWatchlist',
    'columns[9][name]': 'InWatchlist',
    'columns[9][searchable]': 'true',
    'columns[9][orderable]': 'true',
    'columns[9][search][value]': '',
    'columns[9][search][regex]': 'false',
    'columns[10][data]': 'HasFwdDate',
    'columns[10][name]': 'HasFwdDate',
    'columns[10][searchable]': 'true',
    'columns[10][orderable]': 'true',
    'columns[10][search][value]': '',
    'columns[10][search][regex]': 'false',
    'order[0][column]': '4',
    'order[0][dir]': 'desc',
    'start': '0',
    'length': '25',
    'search[value]': '',
    'search[regex]': 'false'
    }

    for x in range(50):
        try:
            splitprox = random.choice(proxiesToList)[0].split(":")
            proxyy = f'http://{splitprox[2]}:{splitprox[3]}@{splitprox[0]}:{splitprox[1]}'
            response = requests.post("https://marketchameleon.com/PressReleases/getAllPressReleases",proxies = {'http':proxyy, 'https':proxyy}, headers=headers, params=params, data=data,timeout=3)
            if response.status_code == 200:
                break
        except:
            continue
    jsonData = response.text
    jsonData = re.sub(r'\\u0022','"', jsonData)
    jsonLoad = json.loads(jsonData)
    finalList = {"Time":[], "Ticker":[],"Price":[],"Headline":[],"Source":[]}
    
    for i in jsonLoad['data']:
        date = i['PressReleaseDate']
        date = re.sub(r'/Date\(','', date)
        date = int(re.sub(r'\)/','', date))/1000
        ticker = i['Symbol']
        headline = i['Headline']
        dateToDateTime = str(datetime.fromtimestamp(date).strftime("%Y-%m-%d %H:%M:%S"))
        dateToDateTime1 = arrow.get(date)
        dateToDateTime2 = dateToDateTime1.to('US/Eastern').format('YYYY-MM-DD HH:mm:ss ')
        price = i['Price']
        publication = i['Source']
        
        
        count = df["Headline"].str.contains(headline,regex=False).any()
        if not count:
            
            finalList["Time"].append(dateToDateTime2)
            finalList["Ticker"].append(ticker)
            finalList["Headline"].append(headline)
            finalList["Price"].append(price)
            finalList["Source"].append(publication)
            print(f'{dateToDateTime} | Tick: {ticker} | Price: {price} | News: {headline} | \n By: {publication}')
            print("-"*200)
    tempFrame = pd.DataFrame.from_dict(finalList) 
    
    df = df.append(tempFrame,ignore_index = True)
    
    return df
    
    
    
while True:
    allNews = getReq()
    
    allNews.to_csv("temp.csv",index=False)

            
    sleep(2)