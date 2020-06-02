# Purpose: metadatascraper scrapes the metadata from the addresses.csv file and
# adds corresponding columns for the specific metadata from those files

# Import packages

from bs4 import BeautifulSoup, SoupStrainer
import requests
import re
import pandas as pd
import urllib
from urllib.request import urlopen
import httplib2
import csv
'''
authorNames = []
for url in other_link:
    i = 0
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser') #parse_only=SoupStrainer('tr'))
    deeperSouper = soup.find('tr', valign='top').getText()
    authorNames.append(str(deeperSouper))
    print(deeperSouper)
    print(authorNames)
'''
df = pd.read_csv('addresses-short.csv')
print(df)

print(df['Websites'].to_string(index=False))

authorNames = []
for url in df['Websites']:
    print(url)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')  # parse_only=SoupStrainer('tr'))
    deeperSouper = soup.find('tr', valign='top').getText()
    authorNames.append(str(deeperSouper))
    print(deeperSouper)
    print(authorNames)

df['author'] = authorNames

print(df)