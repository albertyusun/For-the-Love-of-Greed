# Purpose: metadatascraper scrapes the metadata from the addresses.csv file and
# adds corresponding columns for the specific metadata from those files

# Import packages

from bs4 import BeautifulSoup, SoupStrainer
import requests
import pandas as pd

# 1. Uncomment out the section you're scraping:

df = pd.read_csv('CSVs/addresses-short.csv')
# df = pd.read_csv('CSVs/addresses_TCP_1_1.csv')
# df = pd.read_csv('CSVs/addresses_TCP_1_2.csv')
# df = pd.read_csv('CSVs/addresses_TCP_1_3.csv')
# df = pd.read_csv('CSVs/addresses_TCP_1_4.csv')

print(df)

dates = []
pubinfo = []
titles = []
authors = []
pages = []
for url in df['Websites']:
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
    print("metadata scraping completed for " + url)

print("metadata besides book text completed, now onto book text")

book_links = []
for url in df['Websites']:
    temp = url[:-8]
    temp = temp + 'rgn=main;view=fulltext'  # clicks on the link that holds the full text
    book_links.append(temp)

# add book lines to csv file called 'phase1data.csv':

for book in book_links:
    page = requests.get(book)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(id='doccontent')
    if results is not None:
        r = results.text
        text = r.replace('\n', ' ')
        pages.append(text)
        print("book text scraping completed for " + url)

print("book text scraping completed.")

df['author'] = authors
df['title'] = titles
df['pubinfo'] = pubinfo
df['dates'] = dates
df['book'] = pages

print(df)

with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    print(df)

# 2. Uncomment out the section you're scraping:

df.to_csv("CSVs/metadata-short.csv")
# df.to_csv("CSVs/metadata_TCP_1_1.csv")
# df.to_csv("CSVs/metadata_TCP_1_2.csv")
# df.to_csv("CSVs/metadata_TCP_1_3.csv")
# df.to_csv("CSVs/metadata_TCP_1_4.csv")
