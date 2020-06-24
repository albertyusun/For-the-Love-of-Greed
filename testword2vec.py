import numpy as np
import pandas as pd
import nltk
import gensim
from gensim.test.utils import datapath
from gensim import utils
import multiprocessing

train = pd.read_csv("CSVs/1470-1479dirty.csv")
train['booktext'] = train['booktext'].str.split()

model = gensim.models.word2vec.Word2Vec(sentences=train["booktext"])
for i, word in enumerate(model.wv.vocab):
    if i == 100:
        break
    print(word)
