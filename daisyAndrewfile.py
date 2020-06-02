# Purpose: eebotcpscrapper.py scrapes all the text from one phase at a time.

# Import packages

from bs4 import BeautifulSoup, SoupStrainer
import requests
import re
import pandas as pd
import urllib
from urllib.request import urlopen
import httplib2
'''
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
        print(x)

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
            print(i)

print("How man sub authors were collected: ", len(sub_authors))
print("Sub authors complete")

# combine all author links

s_authors = list(set(sub_authors))

combined = author_links + s_authors
print("Num of combined: ", len(combined))

# get all book links

books = []
for link in combined:
    b = get_books(link)
    for i in b:
        books.append(i)

print("books complete")

'''

urlLink = 'https://quod.lib.umich.edu/e/eebo/B06712.0001.001?view=toc'
"""other_link = ['https://quod.lib.umich.edu/e/eebo/B03160.0001.001?view=toc',
              'https://quod.lib.umich.edu/e/eebo/A19523.0001.001?view=toc',
              'https://quod.lib.umich.edu/e/eebo/A34855.0001.001?view=toc',
              'https://quod.lib.umich.edu/e/eebo/B06712.0001.001?view=toc',
              'https://quod.lib.umich.edu/e/eebo/B03160.0001.001?view=toc',
              'https://quod.lib.umich.edu/e/eebo/A47095.0001.001?view=toc',
              'https://quod.lib.umich.edu/e/eebo/A47086.0001.001?view=toc',
              'https://quod.lib.umich.edu/e/eebo/A47614.0001.001?view=toc',
              'https://quod.lib.umich.edu/e/eebo/A47613.0001.001?view=toc',
              'https://quod.lib.umich.edu/e/eebo/A47611.0001.001?view=toc',
              'https://quod.lib.umich.edu/e/eebo/A47607.0001.001?view=toc',
              'https://quod.lib.umich.edu/e/eebo/A47612.0001.001?view=toc',
              'https://quod.lib.umich.edu/e/eebo/A47606.0001.001?view=toc',
              'https://quod.lib.umich.edu/e/eebo/A47605.0001.001?view=toc',
              'https://quod.lib.umich.edu/e/eebo/A47602.0001.001?view=toc',
              'https://quod.lib.umich.edu/e/eebo/A47601.0001.001?view=toc',
              'https://quod.lib.umich.edu/e/eebo/A47599.0001.001?view=toc',
              'https://quod.lib.umich.edu/e/eebo/A47591.0001.001?view=toc'
]"""

other_link = ['https://quod.lib.umich.edu/e/eebo/A45913.0001.001?view=toc']

authorNames = []
for url in other_link:
    i = 0
    page = requests.get(url)    
    soup = BeautifulSoup(page.content, 'html.parser') #parse_only=SoupStrainer('tr'))
    deeperSouper = soup.find('tr', valign='top').getText()
    if (deeperSouper)[0:6] == "\nTitle":
        authorNames.append("")
    else:
        authorNames.append(str(deeperSouper))
    print(deeperSouper)
    print(authorNames)

'''    
    if deepestSoup not in authorNames:
        authorNames.append(str(deepestSoup)) 
        print(url, i)
    i+=1
print(authorNames)
'''




'''


edited_books = []
for x in books:
    temp = x[:-8]
    temp = temp + 'rgn=main;view=fulltext' #clicks on the link that holds the full text
    edited_books.append(temp)

remove_duplicated = list(set(edited_books))
print(len(remove_duplicated))#Seems to only collect 19408

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
'''