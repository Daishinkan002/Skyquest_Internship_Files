import requests
import selenium.webdriver as webdriver
import pandas as pd
from bs4 import BeautifulSoup
import re

url = 'https://www.fortunebusinessinsights.com/bleaching-clay-market-102762'
r = requests.get(url)
soup = BeautifulSoup(r.content, 'lxml')
all_tags = soup.find_all(['h2', 'h3', 'p', 'ul'])


companies_final_final = []
key_player_internal_content = None
for i, tags in enumerate(all_tags):
    indicator_symbol = str(tags)[1]
    if(indicator_symbol == 'h'):
        x=re.compile('key companies|key market companies|mlist of companies|key market player|key players|market players',re.IGNORECASE)
        print(tags.text.lower())
        
        if(x.search(tags.text.lower())):
            
            key_player_tag = tags
            key_player_internal_content = all_tags[i+1]

ul = key_player_internal_content
if ul:
    lis=ul.find_all('li')
    for li in lis:
        companies_final_final.append(li.text)
else:
    companies_final_final.append('NA')