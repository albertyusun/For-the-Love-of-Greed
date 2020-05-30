# Purpose: eeboscrapper.py scrapes all the text from one phase at a time.

# Import packages

from bs4 import BeautifulSoup, SoupStrainer
import requests
import re
import pandas as pd
import urllib
from urllib.request import urlopen
import httplib2

# get_links - get all associated links on EEBO TCP

def get_links(url):
    total_links = []
    edited_links = []
    http = httplib2.Http()
    status, response = http.request(url)
    for link in BeautifulSoup(response, 'html.parser', parse_only = SoupStrainer('a')):
        if link.has_attr('href'):
            total_links.append(link['href'])
    for x in total_links:
        if 'http' in x:
            edited_links.append(x)
    return edited_links

# get_books - get books on each page

def get_books(url):
    total_links = []
    edited_links = []
    http = httplib2.Http()
    status, response = http.request(url)
    for link in BeautifulSoup(response, 'html.parser', parse_only = SoupStrainer('a')):
        if link.has_attr('href'):
            total_links.append(link['href'])
    for x in total_links:
        if 'http' in x:
            if 'view' in x:
                edited_links.append(x)
    return edited_links

#replace this link with the starting page for phase II. here it is phase I.

total_links = get_links("https://quod.lib.umich.edu/cgi/t/text/text-idx?page=browse&cc=eebo&c=eebo")

author_links = []
for x in total_links:
    if 'key=author' in x:
        author_links.append(x)

print("author complete")

sub_authors = []
for x in author_links:
    links = get_links(x)
    for i in links:
        if 'key=author;page=browse;value' in i:
            sub_authors.append(i)
            
print("s authors complete")
            
s_authors = list(set(sub_authors))

combined = author_links + s_authors

books = []
for link in combined:
    b = get_books(link)
    for i in b:
        books.append(i)

print("books complete")
    
edited_books = []
for x in books:
    temp = x[:-8]
    temp = temp + 'rgn=main;view=fulltext'
    edited_books.append(temp)

remove_duplicated = list(set(edited_books))

print("edited books complete")

d = {}
i = 0
for book in remove_duplicated:
    i = i + 1
    page = requests.get(book)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(id='doccontent')
    if results is not None:
        r = results.text
        text = r.replace('\n', '')
        title = soup.find(id='itemTextmdata')
        t = title.text
        redit = t.replace('\n', '')
        d[redit] = text
        print(i)
        
df = pd.DataFrame(d)
df.to_csv('phase1data.csv')

'''
total_links2 = get_links('https://quod.lib.umich.edu/cgi/t/text/text-idx?page=browse&cc=eebo2&c=eebo2')

d = {}
for book in edited_books:
    page = requests.get(boo)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(id='doccontent')
    if results is not None:
        r = results.text
        text = r.replace('\n', '')
        title = soup.find(id='itemTextmdata')
        t = title.text
        tedit = t.replace('\n', '')
        d[tedit] = text
    
df = pd.DataFrame(d)
df.to_csv('phase1data.csv')
'''
