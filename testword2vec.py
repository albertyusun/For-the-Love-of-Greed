import numpy as np
import pandas as pd
import nltk
import gensim
from gensim.test.utils import datapath
from gensim import utils
import multiprocessing
import time

train = pd.read_csv("CSVs/1550-1559.csv", encoding="ISO-8859-1")
# train = pd.read_csv("CSVs/1470-1479dirty.csv")
train['booktext'] = train['booktext'].str.split()

# time before
before = time.time()

# create vector
model = gensim.models.word2vec.Word2Vec(sentences=train["booktext"], workers=4, min_count=0)

# calculate time elapsed
elapsed = time.time() - before

j=0
for i, word in enumerate(model.wv.vocab):
    j+=1
print("words count:", j)

print("time elapsed: ", elapsed)

model.wv.save_word2vec_format("output/word2vec.txt")