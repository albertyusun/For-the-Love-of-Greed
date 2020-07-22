# Import packages
import concurrent
import time
from bs4 import BeautifulSoup, SoupStrainer
import requests
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

def extract_row(url):
    datepage = requests.get(url)
    soup = BeautifulSoup(datepage.content, 'html.parser')
    titleSoup = soup.find('i').getText()
    authorSoup = soup.find('i').findNext('br').next_element
    pubSoup = soup.find('i').findNext('br').findNext('br').next_element
    if len(pubSoup) == 1:
        pubSoup = authorSoup
        authorSoup = 'No Author'
    row = [url, titleSoup, authorSoup, pubSoup, pubSoup[-5:-1]]
    print("Just got the metadata from: ", url)
    time.sleep(1.5) #modify as necessary
    #.5 gives me 426 results until it stops, 1 gives me 486 results until it stops
    return row


def extract_book(book_link):
    page = requests.get(book_link)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(id='doccontent')
    text = ''
    if results is not None:
        r = results.text
        text = r.replace('\n', ' ')
    time.sleep(1.5) # modify as necessary
    print("just copied a book text from ", book_link)
    return text


if __name__ == '__main__':
    # 1. Uncomment out the section you're scraping:

    df = pd.read_csv('CSVs/addresses-short.csv')
    # df = pd.read_csv('CSVs/addresses_TCP_1_1.csv')
    # df = pd.read_csv('CSVs/addresses_TCP_1_2_first500.csv')
    # df = pd.read_csv('CSVs/addresses_TCP_1_3.csv')
    # df = pd.read_csv('CSVs/addresses_TCP_1_4.csv')

    listInList = [["website", "title", "author", "publishinfo", "dates"]]

    print("Let's extract the initial metadata:")

    # just metadata
    start = time.time()
    with ThreadPoolExecutor(max_workers=3) as executor:
        future_titles = {executor.submit(extract_row, url): url for url in df['Websites']}
        for future in concurrent.futures.as_completed(future_titles):
            listInList.append(future.result())

    mid = time.time()
    print("time for metadata: ", mid - start)  # time it takes to run the metadata scraping

    new_df = pd.DataFrame(listInList[1:],columns=listInList[0])

    print("metadata besides book text completed, now onto book text")

    # get book links
    book_links = []
    for url in df['Websites']:
        temp = url[:-8]
        temp = temp + 'rgn=main;view=fulltext'  # clicks on the link that holds the full text
        book_links.append(temp)

    print("book links finished, now onto book text")

    book_text = []
    # now book text
    with ThreadPoolExecutor(max_workers=4) as executor:
        future_titles = {executor.submit(extract_book, url): url for url in book_links}
        for future in concurrent.futures.as_completed(future_titles):
            book_text.append(future.result())
    print("length: ", len(book_text))
    #print(book_text)


    new_df["booktext"] = book_text

    with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
        print(new_df)

    finish = time.time()
    print("time for total: ", finish - start)  # time it takes to run the metadata scraping

    # 2. Uncomment out the section you're scraping:

    new_df.to_csv("CSVs/metadata-short.csv")
    # new_df.to_csv("CSVs/metadata_TCP_1_1.csv")
    # new_df.to_csv("CSVs/metadata_TCP_1_2.csv")
    # new_df.to_csv("CSVs/metadata_TCP_1_2_first500.csv")
    # new_df.to_csv("CSVs/metadata_TCP_1_3.csv")
    # new_df.to_csv("CSVs/metadata_TCP_1_4.csv")
