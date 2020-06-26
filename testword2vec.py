import numpy as np
import pandas as pd
import nltk
import gensim
from gensim.test.utils import datapath
from gensim import utils
import multiprocessing
import time

train = pd.read_csv("../CSVs/1580-1589.csv", encoding="ISO-8859-1")
print("read the document!")

train['booktext'] = train['booktext'].str.split()
print("split the document into words!")

# time before
before = time.time()

# create vector
model = gensim.models.word2vec.Word2Vec(sentences=train["booktext"], workers=4, min_count=1, size=50)

# calculate time elapsed
elapsed = time.time() - before

j=0
for i, word in enumerate(model.wv.vocab):
    j+=1
print("words count:", j)

print("time elapsed for word2vec: ", elapsed)

# model.wv.save_word2vec_format("../CSVs/1590w2v.txt")
model.save("../CSVs/1580w2v-50.model")
