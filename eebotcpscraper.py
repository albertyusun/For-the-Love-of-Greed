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
    for link in BeautifulSoup(response, 'html.parser', parse_only=SoupStrainer('a')):
        if link.has_attr('href'):
            total_links.append(link['href'])
    for x in total_links:
        if 'http' in x:
            edited_links.append(x)
    return edited_links


# get_books - This function clicks "View entire text" button on the book page

def get_books(url):
    total_links = []
    edited_links = []
    http = httplib2.Http()
    status, response = http.request(url)
    for link in BeautifulSoup(response, 'html.parser', parse_only=SoupStrainer('a')):
        if link.has_attr('href'):
            total_links.append(link['href'])
    for x in total_links:
        if 'http' in x:
            if 'view' in x:
                edited_links.append(x)
    return edited_links


# phase I and phase II links saved as variables:

phaseI = "https://quod.lib.umich.edu/cgi/t/text/text-idx?page=browse&cc=eebo&c=eebo"
phaseII = "https://quod.lib.umich.edu/cgi/t/text/text-idx?page=browse&cc=eebo2&c=eebo2"

# use phaseI OR phaseII for that phase's texts

total_links = get_links(phaseI)

# author_links - add every "larger" author link to author_links

author_links = []
for x in total_links:
    if 'key=author' in x:
        author_links.append(x)
        print(x)

print("author complete")

# sub_authors - add every sub author link to sub_authors.
# NOTE: We should make sure the code runs more efficiently by not checking *every* link on the page. We can also skip
# this entirely and manually input the links, which would save a lot of time, so we don't have to go through a nested
# for loop.

sub_authors = []
for x in author_links:
    links = get_links(x)
    for i in links:
        if 'key=author;page=browse;value' in i and i not in sub_authors:
            sub_authors.append(i)
            print(i)

print("s authors complete")

# combine all author links

s_authors = list(set(sub_authors))

combined = author_links + s_authors

# get all book links

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

# add book lines to csv file called 'phase1data.csv':

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

# EEBO 2 code, commented out:

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
