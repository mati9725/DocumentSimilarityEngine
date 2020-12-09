# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 21:43:20 2020

@author: mati9
"""


import requests
import bs4 as bs
import urllib.robotparser
import time
import json
from datetime import datetime
        
result_dict = dict()    
rp = urllib.robotparser.RobotFileParser('https://pl.wikipedia.org/robots.txt')
rp.read()
# print (rrate)

urls = ['https://pl.wikipedia.org/wiki/Adolf_Hitler']

while len(urls) > 0 and len(result_dict) <= 100:
    url = urls.pop()

    if not rp.can_fetch("*", url):
        print(f"Url disallowed: {url}")
        continue
    if url in result_dict:
        print(f'Duplicate skipped: {url}')
        continue
    if url is None:
        print(f'None url skipped')
        continue
    
    print(url)
    response = requests.get(url)
    #dodać sprawdzanie czy HTTP200
    
    soup = bs.BeautifulSoup(response.text, 'html.parser')
    paragraph = soup.p
    
    result_dict[url] = paragraph.text
    
    for a in soup.select('p a'):
        new_url = a.get('href')
        if new_url is None:
            continue
        if new_url.startswith('#cite'):
            continue
        if not new_url.startswith('/'):
            continue
        
        full_new_url = 'https://' + rp.host + new_url
        if full_new_url in result_dict:
            continue
        
        urls.append(full_new_url)
    

    time.sleep(1)
    
# response = requests.get('https://pl.wikipedia.org/wiki/Adolf_Hitler')
# soup = bs.BeautifulSoup(response.text, 'html.parser')
# paragraph = soup.p
# print (paragraph.text)\
result_json = json.dumps(result_dict)
with open(f"result_{datetime.now()}.json".replace(':','_'), "w") as f:
    f.write(result_json)

#print(result_dict)