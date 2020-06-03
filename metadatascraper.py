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

#print(df['Websites'].to_string(index=False))

dates = []
pubinfo = []
titles = []
authors = []
for url in df['Websites']:
    print(url)
    datepage = requests.get(url)
    soup = BeautifulSoup(datepage.content, 'html.parser')
    titleSoup = soup.find('i').getText()
    authorSoup = soup.find('i').findNext('br').next_element
    pubSoup = soup.find('i').findNext('br').findNext('br').next_element
    if len(pubSoup) == 1:
        pubSoup = authorSoup
        authorSoup = 'No Author'
    titles.append(titleSoup)
    pubinfo.append(pubSoup)
    authors.append(authorSoup)
    dates.append(pubSoup[-5:-1])

df['author'] = authors
df['title'] = titles
df['pubinfo'] = pubinfo
df['dates'] = dates

print(df)

with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    print(df)

df.to_csv("metadata.csv")
