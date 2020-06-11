from bs4 import BeautifulSoup, SoupStrainer
import requests
import re
import pandas as pd
import urllib
from urllib.request import urlopen
import httplib2
import csv


dataframe = pd.read_csv('CSVs/metasplit5.csv')

book_texts = dataframe["booktext"].tolist()

# extract links from csv then prepare to open full texts

book_links = []
for url in dataframe['website']:
    temp = url[:-8]
    temp = temp + 'rgn=main;view=fulltext'  # clicks on the link that holds the full text
    book_links.append(temp)

# verify full text on page matches full text in csv.

error = 0
for i in range(len(book_links)):
    print(book_links[i])
    page = requests.get(book_links[i])
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(id='doccontent')

    if results is not None:
        r = results.text
        text = r.replace('\n', ' ')
        if type(book_texts[i]) != str or text[0:150] != book_texts[i][0:150]:
            print("Book text fixed.")
            error += 1
            book_texts[i] = text
        else:
            print("Book text fine.")
    else:
        print("Book text empty.")
        error += 1
        book_texts[i] = "ERROR LOADING BOOK"

print(error)

dataframe["booktext"] = book_texts
dataframe.to_csv("CSVs/newmetasplit5.csv")