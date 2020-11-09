# Import packages
import concurrent
import time
from bs4 import BeautifulSoup, SoupStrainer
import requests
import pandas as pd
from concurrent.futures import ThreadPoolExecutor


def extract_metadata(summary_url):
    """
    Extract book metadata and link to book text from the summary page.

    :param url: link to the summary url
    :return: List of book url, title, author, publisher, date
    """
    datepage = requests.get(summary_url)
    soup = BeautifulSoup(datepage.content, 'html.parser')
    titleSoup = soup.find('i').getText()
    authorSoup = soup.find('i').findNext('br').next_element
    pubSoup = soup.find('i').findNext('br').findNext('br').next_element
    if len(pubSoup) == 1:
        pubSoup = authorSoup
        authorSoup = 'No Author'
    row = [summary_url, titleSoup, authorSoup, pubSoup, pubSoup[-5:-1]]
    print("Just got the metadata from: ", summary_url)
    time.sleep(1.5)  # Necessary for their servers to process our parallel requests.
    return row


def extract_full_text(book_link):
    """
    Extract book text from the book link.

    :param book_link: link to the book contents
    :return:
    """
    page = requests.get(book_link)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(id='doccontent')
    text = ''
    if results is not None:
        r = results.text
        text = r.replace('\n', ' ')
    time.sleep(1.5)  # Necessary for their servers to process our parallel requests.
    print("just copied a book text from ", book_link)
    return text


if __name__ == '__main__':

    start = time.time()

    df = pd.read_csv('CSVs/addresses.csv')

    print("Let's extract the metadata (url, title, author, publishing info, dates):")

    # Part 1: Metadata Scraping

    rows = [["summary_url", "title", "author", "pub", "dates"]]
    with ThreadPoolExecutor(max_workers=3) as executor:
        future_titles = {executor.submit(extract_metadata, url): url for url in df['Websites']}
        for future in concurrent.futures.as_completed(future_titles):
            rows.append(future.result())

    new_df = pd.DataFrame(rows[1:], columns=rows[0])

    print("Metadata collection completed. Now, let's collect the full text of the books:")

    # Part 2: Full Text Scraping

    full_text_links = [url[:-8] + 'rgn=main;view=fulltext' for url in df['Websites']]  # full text link

    full_text = []
    with ThreadPoolExecutor(max_workers=4) as executor:
        future_titles = {executor.submit(extract_full_text, url): url for url in full_text_links}
        for future in concurrent.futures.as_completed(future_titles):
            full_text.append(future.result())

    print("Length: ", len(full_text))

    new_df["fulltext"] = full_text  # add to df

    new_df.to_csv("CSVs/output.csv")

    print("Total time elapsed: ", time.time() - start)