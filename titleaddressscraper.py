# Purpose: eebotcpscrapper.py scrapes all the text from one phase at a time.

# Import packages

from bs4 import BeautifulSoup, SoupStrainer
import requests
import re
import pandas as pd
import urllib
from urllib.request import urlopen
import httplib2
import csv

# get_links - get all associated links on EEBO TCP


def get_links(url):
    total_links = []
    http = httplib2.Http() # creates Http client that can send requests and get responses
    status, response = http.request(url) # "request" the url
    for link in BeautifulSoup(response, 'html.parser', parse_only=SoupStrainer('a')): # only collect the <a> tags
        if link.has_attr('href') and ('http' in link.get('href')): # href is a clickable link
            total_links.append(link['href'])
    return total_links


# get_books - This function grabs all book links on a page.

def get_books(url):
    total_links = get_links(url)
    edited_links = []
    for x in total_links:
        if 'view' in x: #view is in the url for the next page we need to get to
            edited_links.append(x)
    return edited_links


# phase I and phase II links saved as variables:

phaseI = "https://quod.lib.umich.edu/e/eebo?key=title;page=browse"
phaseII = "https://quod.lib.umich.edu/cgi/t/text/text-idx?page=browse&cc=eebo2&c=eebo2"

# use phaseI OR phaseII for that phase's texts

total_links = get_links(phaseI)

# title_links - add every "larger" title link to title_links

title_links = []
for x in total_links:
    if 'key=title' in x:
        title_links.append(x)

print("Main title links", len(title_links))
print("Titles complete")

# sub_titles - add every sub title link to sub_titles.
# NOTE: We should make sure the code runs more efficiently by not checking *every* link on the page. We can also skip
# this entirely and manually input the links, which would save a lot of time, so we don't have to go through a nested
# for loop.

titles = []
for x in title_links:
    links = get_links(x)
    for i in links:
        if 'key=title;page=browse;value' in i and i not in titles:
            if (i+'+') not in titles:
                titles.append(i)

print("How many sub titles were collected: ", len(titles))
print("Sub titles complete")

# get all book links

books = []
j = 0
for link in titles:
    b = get_books(link)
    for i in range(len(b)):
        j += 1
        books.append(b[i])
        print(j, b[i])

print("books complete", "length is ", len(books))

write_file="addresses.csv"
with open('addresses.csv', 'w') as output:
    for line in books:
        output.write(line+'\n')