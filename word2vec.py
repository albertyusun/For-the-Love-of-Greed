import numpy as np
import pandas as pd
import nltk
import gensim
from gensim.test.utils import datapath
from gensim import utils
import multiprocessing
import time

date_buckets = ["1470-1494","1495-1519","1520-1544","1545-1569",
                "1570-1594","1595-1619","1620-1644","1645-1669",
                "1670-1700"]

j=1

for date in date_buckets:
    df = pd.read_csv("C:/Users/Albert/Box Sync/For the Love of Greed Data Storage/"+date+".csv", encoding="ISO-8859-1")
    print(j, "/", len(date_buckets), ": read the document!")
    df['booktext'] = df['booktext'].str.split()
    print("split the document into words!")
    # time before
    before = time.time()
    # create vector
    model = gensim.models.word2vec.Word2Vec(sentences=df["booktext"], workers=4, min_count=1, size=50)
    # calculate time elapsed
    elapsed = time.time() - before
    print("time elapsed for word2vec: ", elapsed, " ", j, "/", len(date_buckets))
    j+=1

    model.save("../output/"+date[:4]+"-vocab.pkl")
    elapsed = time.time() - elapsed
    print("time elapsed: ", elapsed)
    model.save("../output/"+date[:4]+"-w.npy")
    elapsed = time.time() - elapsed
    print("time elapsed: ", elapsed)

'''
j=0
for i, word in enumerate(model.wv.vocab):
    j+=1
print("words count:", j)
'''


# model.wv.save_word2vec_format("../CSVs/1590w2v.txt")

