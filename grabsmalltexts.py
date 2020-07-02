import pandas as pd

date_buckets = ["1470-1494","1495-1519","1520-1544","1545-1569",
                "1570-1594","1595-1619","1620-1644","1645-1669",
                "1670-1700"]


# retrieves every text in our database with string length less than length.\
# returns a dataframe containing all the information
def grab_length_texts(length):
    texts = []
    urls = []
    titles = []
    authors = []
    pubs = []
    dates = []
    for date in date_buckets:
        df = pd.read_csv("CSVs/"+date+".csv")
        books = df["booktext"].tolist()
        links = df["website"].tolist()
        names = df["title"].tolist()
        writers = df["author"].tolist()
        pubinfos = df["publishinfo"].tolist()
        years = df["dates"].tolist()
        for i in range(len(books)):
            if len(books[i]) <= length:
                texts.append(books[i])
                urls.append(links[i])
                titles.append(names[i])
                authors.append(writers[i])
                pubs.append(pubinfos[i])
                dates.append(years[i])
    result = pd.DataFrame()
    result["website"] = urls
    result["title"] = titles
    result["author"] = authors
    result["publishinfo"] = pubs
    result["dates"] = dates
    result["booktext"] = texts
    return result

ans = grab_length_texts(300)
print(ans)