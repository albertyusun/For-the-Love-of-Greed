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
    edited_links = []
    http = httplib2.Http() #creates Http client that can send requests and get responses
    status, response = http.request(url) #"request" the url
    for link in BeautifulSoup(response, 'html.parser', parse_only=SoupStrainer('a')): #only collect the <a> tags
        if link.has_attr('href'): #href is a clickable link
            total_links.append(link['href'])
    for x in total_links:
        if 'http' in x: #to differentiate between links at the bottom of the page and the browse links
            edited_links.append(x)
    return edited_links


# get_books - This function clicks "View entire text" button on the book page

def get_books(url):
    total_links = []
    edited_links = []
    http = httplib2.Http()
    status, response = http.request(url)
    for link in BeautifulSoup(response, 'html.parser', parse_only=SoupStrainer('a')): #only <a> tags
        if link.has_attr('href'):
            total_links.append(link['href'])
    for x in total_links:
        if 'http' in x:
            if 'view' in x: #view is in the url for the next page we need to get to
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

print("Main author links", len(author_links))
print("Author complete")

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

print("How many sub authors were collected: ", len(sub_authors))
print("Sub authors complete")

# combine all author links

s_authors = list(set(sub_authors))

combined = author_links + s_authors
print("Num of combined: ", len(combined))

# get all book links

books = []
for link in combined:
    b = get_books(link)
    for i in range(len(b)):
        books.append(b[i])
        print(i, b[i])

print("books complete", "length is ", len(books))

with open('addresses.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(books)
