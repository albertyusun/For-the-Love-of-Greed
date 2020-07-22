import pandas as pd

date_buckets = ["1490-1499", "1500-1509",
                "1510-1519", "1520-1529", "1530-1539", "1540-1549",
                "1550-1559", "1560-1569", "1570-1579", "1580-1589",
                "1590-1599", "1600-1609", "1610-1619", "1620-1629",
                "1630-1639", "1640-1649", "1650-1659", "1660-1669",
                "1670-1679", "1680-1689", "1690-1700"]

lexicon = {'consumption', 'consume', 'cupidity', 'cupiditas', 'curiosity', 'curiositas',
           'greed', 'desire', 'appetite', 'lust', 'libido', 'covetousness', 'avarice',
           'possess', 'possession', 'possessing', 'busy', 'businesse', 'need', 'necessity',
           'necessary', 'needing', 'meed', 'bowgeor', 'bougeor', 'budge', 'wastour',
           'waster', 'wasture', 'wastoure', 'speculation', 'debt', 'debitum', 'expense',
           'gain', 'miser', 'fortune', 'fortuna', 'use', 'usury', 'interest',
           'interesse', 'consumptioner'}

for date in date_buckets:
    df = pd.read_csv("C:/Users/Albert/Box Sync/For the Love of Greed Data Storage/"+date+".csv", encoding="ISO-8859-1")
    decade_words = set()
    books = df['booktext'].tolist()
    for book in books:
        book_list = set(book.split(' '))
        lexicon_appears = lexicon & book_list
        decade_words = decade_words.union(lexicon_appears)
    decade_words = list(decade_words)
    print(date + ":" + ', '.join(e for e in decade_words))

'''
for date in date_buckets:
    df = pd.read_csv("CSVs/"+date+".csv")
    books = df['booktext'].tolist()
    words = []

    # first, turn every book into a list
    # then, add every word in that list to words
    for book in books:
        book_list = book.split(' ')
        for book_word in book_list:
            if book_word not in words:
                words.append(book_word)

    print(date+":")
    for word in words:
        if word in lexicon:
            print(word)

'''
