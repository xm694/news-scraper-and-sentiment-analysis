#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 23 17:58:14 2023

@author: shaymo
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup



root='https://www.google.com'
url = 'https://www.google.com/search?q=voice+to+parliament&tbs=cdr%3A1%2Ccd_min%3A9%2F1%2F2023%2Ccd_max%3A10%2F14%2F2023&tbm=nws'
headers = {'User-Agent':'Mozilla/5.0'}

def news(url):
    driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    wait = WebDriverWait(driver, 10)
    driver.get(url)
    get_url = driver.current_url
    wait.until(EC.url_contains(root))
    if get_url == url:
        page_source = driver.page_source
    
    soup = BeautifulSoup(page_source, 'html.parser')
    
    news = soup.find_all('div', class_='SoaBEf')
    news_data = []
    
    for item in news:
        title = item.find('div', class_='n0jPhd ynAwRc MBeuO nDgy9d').text
        snippet = item.find('div', class_='GI74Re nDgy9d').text
        link = item.find('a', href=True)['href']
        date_div = item.find('div', class_='OSrXXb rbYSKb LfVVr')
        date = date_div.find('span').text
        
        #pre-word processing ready for csv
        title = title.replace(',', '')
        snippet = snippet.replace(',', '')
        
        news_data.append({'Title':title,'Date': date,'Snippet': snippet,'Link': link})
        
    df = pd.DataFrame(news_data, columns=['Title', 'Date', 'Snippet', 'Link'] )
    df.to_csv('news.csv', mode='a', index=False)
    next_url = soup.find('a', attrs={'id':'pnnext'})['href']
    url = root + next_url
    return url


while True:
        url = news(url)



