# Initialize empty list of cosine similarities
# For each csv:
# Randomly select documents from csv.
#       Use row index as key. Get number of rows (pd command)  (df.index) (done)
#       Create list of indices, np.random.choice to get set of indices. range(n) (done)
#       Retrieve texts corresponding to randomly selected indices. Convert to list of texts (done)
#           For each index, grab the text at that row. Append to list. (done)
#       Tokenize the list of texts (done)
# Create 300 dimensional word embedding of tokenized sample. (done)
#       Create keyed vectors file also (automatic with load_models, so done)
#       *** Extract desired statistics ***
#           Get cosine similarity between 'consume' and 'luxury' and for 'consume' and 'disease'
#               (done, thanks to cosine_over_time)
#           Add cosine similarity to a list
#           Add list to csv
#       Delete word embedding. os.remove() (done)
#

import readModels as rm
import pandas as pd
import csv
import numpy as np
import scipy
import gensim
import os

date_buckets = ["1470-1494", "1495-1519","1520-1544","1545-1569",
                "1570-1594","1595-1619","1620-1644","1645-1669",
                "1670-1700"]


def get_sample_indices(index, sample_size):
    """
     :param index: pd.DataFrame().index intended input; takes in any range of integers
     :param sample_size: size of desired sample
     :return: a numpy.ndarray object containing sample_size entries of randomly selected integers
     from the range of index
     """
    sample = np.random.choice(index, size=sample_size)
    return sample


def get_sample_texts(key_sample, dataframe):
    """
     :param key_sample: nparray of sample indices
     :param dataframe: pandas dataframe of desired csv
     :return: list of desired sample texts
     """
    texts = []
    for index in key_sample:
        document = dataframe.at[index, 'booktext']
        texts.append(document)
    return texts


def tokenize(texts):
    """
     :param texts: list of texts
     :return: order-preserving list of lists of words; texts tokenized
     """
    tokenized = []
    for text in texts:
        tokenized.append(text.split())
    return tokenized


def bootstrap_model(label, tokenized_texts):
    """
     :param label: a simple name for the saved model
     :param tokenized_texts: list of lists of words; tokenized texts
     :return: saves word2vec model to disk.
     """
    model = gensim.models.word2vec.Word2Vec(sentences=tokenized_texts, workers=4, min_count=1,
                                            size=300)
    model.save('bootstrapping/' + label)
    return model


def purge_model(label):
    """
    deletes every file in 'bootstrapping' containing the given label in its name

    :param label: keyword for identifying target files
    :return: returns None
    """
    directory = os.listdir("bootstrapping")
    for file in directory:
        if label in file:
            os.remove("bootstrapping/" + file)


def create_sample_text(file_path):
    """
    :param file_path: full name of csv file to create sample out of
    :return: tokenized sample of texts
    """
    df = pd.read_csv(file_path)
    keys = get_sample_indices(df.index, 10) # 10 is completely arbitrary and can be changed later
    sample = get_sample_texts(keys, df)
    tokenized_sample = tokenize(sample)
    return tokenized_sample


def semantic_similarity_data(label, tokenized_text, shared_word, word1, word2):
    """
    generates data on cosine similarity for one sample (i.e. one word embedding, one time period)
    :param label: identifiable label for word embedding model
    :param tokenized_text: output of tokenize(), or any list of lists of words
    :param shared_word: word to compare to two different words
    :param word1: first word to compare to shared_word
    :param word2: second word to compare to shared_word
    :return: pair of cosine similarity between shared_word and word1/word2 in sample text
    """
    model = bootstrap_model(label, tokenized_text)
    try:
        sim1 = model.wv.similarity(shared_word, word1)
    except KeyError:
        sim1 = None
    try:
        sim2 = model.wv.similarity(shared_word, word2)
    except KeyError:
        sim2 = None
    purge_model(label)
    return sim1, sim2


def simple_bootstrap():
    for date in date_buckets:
