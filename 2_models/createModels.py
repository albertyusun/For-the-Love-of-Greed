import numpy as np
import pandas as pd
import nltk
import gensim
from gensim.test.utils import datapath
from gensim import utils
import multiprocessing
import time

quarter_date_buckets = ["1470-1494", "1495-1519", "1520-1544", "1545-1569",
                        "1570-1594", "1595-1619", "1620-1644", "1645-1669",
                        "1670-1700"]

decade_date_buckets = ["1470-1479", "1480-1489", "1490-1499",
                       "1500-1509", "1510-1519", "1520-1529", "1530-1539", "1540-1549", "1550-1559",
                       "1560-1569", "1570-1579", "1580-1589", "1590-1599", "1600-1609", "1610-1619",
                       "1620-1629", "1630-1639", "1640-1649", "1650-1659", "1660-1669", "1670-1679",
                       "1680-1689", "1690-1700"]

j = 1

for date in quarter_date_buckets[:1]:
    before = time.time()
    df = pd.read_csv("C:/Users/Albert/Box Sync/For the Love of Greed Data Storage/CSV_quartercentury/" + date + ".csv",
                     encoding="ISO-8859-1")
    print(j, "/", len(quarter_date_buckets), date, ": read the document!")
    df['booktext'] = df['booktext'].str.split()

    model = gensim.models.word2vec.Word2Vec(sentences=df["booktext"], workers=4, min_count=1, size=50)

    model.save(date)

    after = time.time() - before
    print("Time elapsed for ", date, "=", after)

    j += 1  # iterate counter

    '''
    model.vocabulary.save("../output/"+date[:4]+"-vocab.pkl")
    elapsed = time.time() - elapsed
    print("time elapsed: ", elapsed)
    model.wv.save("../output/"+date[:4]+"-w.npy")
    elapsed = time.time() - elapsed
    print("time elapsed: ", elapsed)
    '''

'''
j=0
for i, word in enumerate(model.wv.vocab):
    j+=1
print("words count:", j)
'''

# model.wv.save_word2vec_format("../CSVs/1590w2v.txt")
