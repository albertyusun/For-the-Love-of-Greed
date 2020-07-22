# Initialize empty list of cosine similarities
# For each csv:
# Randomly select documents from csv.
#       Use row index as key. Get number of rows (pd command)  (df.index) (done)
#       Create list of indices, np.random.choice to get set of indices. range(n) (done)
#       Retrieve texts corresponding to randomly selected indices. Convert to list of texts (done)
#           For each index, grab the text at that row. Append to list. (done)
#       Tokenize the list of texts (done)
#
# Create 300 dimensional word embedding of tokenized sample. (done)
#       *** Extract desired statistics ***
#           Get cosine similarity between 'consume' and 'luxury' and for 'consume' and 'disease'
#               (done, thanks to cosine_over_time)
#           Add cosine similarity to a list
#           Add list to csv
#       Delete word embedding. os.remove() (done)
#   For Gender over time:
#       *** Extract desired statistics ***
#           Vocabulary is variable across resamples. Thus, we need to find the vocab new every
#           time. And we need to regenerate the cultural axes, since the embedding is also
#           variable. And I need to call avg_spelling_vectors anew every time.
#
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
     :return: a numpy.ndarray object containing sample_size entries of randomly selected
        integers from the range of index
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
    model = gensim.models.word2vec.Word2Vec(sentences=tokenized_texts, workers=4, min_count=5,
                                            size=300)
    # model.save('bootstrapping/' + label)
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
    keys = get_sample_indices(df.index, len(df.index))
    sample = get_sample_texts(keys, df)
    tokenized_sample = tokenize(sample)
    return tokenized_sample


def semantic_similarity_data(label, tokenized_text, shared_word, word1, word2):
    """
    generates data on cosine similarity for one sample (i.e. one word embedding, one time
    period)
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
    return sim1, sim2


def simple_bootstrap(shared_word, word1, word2):
    """
    uses a monte carlo bootstrapping algorithm to produce resamples of our desired statistic,
    in this case the cosine similarity between shared_word and word1, and the cosine similarity
    between shared_word and word2.

    :param shared_word: the word examined twice
    :param word1: word compared to shared_word
    :param word2: word compared to shared_word
    :return: returns None, but writes to a csv all of the cosine similarities in each resample,
        for each csv.
    """
    df = pd.DataFrame()
    for date in date_buckets:
        # number of samples in each csv
        print("starting", date)
        sample_num = 100
        count = 0
        sim1_list = []
        sim2_list = []
        for i in range(sample_num):
            print("sample", count)
            text = create_sample_text("CSVs/" + date + "clean.csv")
            file_label = date + "_" + str(count)
            temp1, temp2 = semantic_similarity_data(file_label, text, shared_word, word1,
                                                    word2)
            sim1_list.append(temp1)
            sim2_list.append(temp2)
            count += 1
        df["Similarity in " + date + " between " + shared_word + " and " + word1] = sim1_list
        df["Similarity in " + date + " between " + shared_word + " and " + word2] = sim2_list
    df.to_csv("wordsOverTimeBootstrapped.csv")


def global_vocab():
    """
    :return: gets the complete vocabulary of the dataset.
    """
    words = set()
    custom = []
    for date in date_buckets:
        vf = pd.read_csv("CSVs/spellingvariations/wordVariation" + date + ".csv")
        for col in vf.columns:
            word = col[4:].lower()
            if word not in words:
                custom.append(word)
    words = words.union(set(custom))

    for date in date_buckets:
        vocab = rm.get_vocab(date)
        words = words.union(vocab)
    return list(words)


def avg_spelling_vectors(date, model):
    """
    just like the function of the same name in readModels.py, but takes in a word2vec model.

    :param date: time period of concern; used mostly for finding desired range of spelling variants
    :param model: model to draw vocabulary from.
    :return: dictionary mapping lexicon words to the average vector of spelling variant vectors.
    """
    df = pd.read_csv("CSVs/spellingvariations/wordVariation" + date + ".csv")
    vectors = model.wv
    base_words = []
    columns = df.columns
    word_vectors = {}

    # get principal words
    for col in columns:
        base_words.append(col[4:].lower())

    # for each word, average together the vectors of all of its spelling variations.
    # this average is the new vector for that word
    for i in range(len(columns)):
        vecs = []
        for variant in df[columns[i]]:
            if type(variant) is str:
                try:
                    vecs.append(rm.get_vector(variant, vectors))
                except KeyError:
                    print(variant, "not found in", date)
        if len(vecs) != 0:
            word_vectors[base_words[i]] = rm.avg_vector(vecs)
    return word_vectors


def gender_dimension_bootstrap(model, vectors):
    """
    nearly just like gender_dimension(date, vectors) except this takes in a model instead of a date.
    also, this considers the possibility that no spelling variants of a lexicon word appear.

    :param model: word2vec model to draw vocab from.
    :param vectors: extra vectors outside the model to be considered separately.
    :return: dictionary of every vocab word in model's cosine similarity to the gender cultural axis.
    """
    vecs = model.wv

    # need to create axis vector
    differences = []
    for i in range(len(rm.feminine)):
        try:
            male_temp = rm.get_vector(rm.masculine[i], vecs)
            female_temp = rm.get_vector(rm.feminine[i], vecs)
            differences.append(np.subtract(female_temp, male_temp))
        except KeyError:
            print("Could not find", rm.masculine[i], "or", rm.feminine[i], "in model")

    # now average all the difference vectors together
    axis_vector = rm.avg_vector(differences)

    # now, we need to produce the cosine similarities
    cosine_similarities = {}
    for i, word in enumerate(vecs.vocab):
        if word not in vectors.keys():
            cosine_similarities[word] = 1 - scipy.spatial.distance.cosine(vecs[word], axis_vector)
        else:
            cosine_similarities[word] = 1 - scipy.spatial.distance.cosine(vectors[word], axis_vector)
    for word in vectors.keys():
        if word not in cosine_similarities.keys():
            cosine_similarities[word] = 1 - scipy.spatial.distance.cosine(vectors[word], axis_vector)
    return cosine_similarities


def two_sided_gender_bootstrap(date):
    """
    uses a monte carlo bootstrapping algorithm to produce resamples of our desired statistic,
    in this case the cosine similarity between every vocabulary word and a cultural axis.

    :param date: time range to resample
    :return: creates csv of data.
    """
    df = pd.DataFrame()
    df["Words"] = rm.get_vocab(date)
    print("starting", date)
    sample_num = 100
    count = 0
    while count < sample_num:
        print("sample", count)
        text = create_sample_text("CSVs/" + date + "clean.csv")

        file_label = date + "_" + str(count)

        model = bootstrap_model(file_label, text)
        lexicon = avg_spelling_vectors(date, model)
        if len(lexicon.keys()) == 0:
            print("No lexicon words found. Cancelling this run.")
            continue
        cosine_dict = gender_dimension_bootstrap(model, lexicon)

        cosines = []
        for word in df["Words"].tolist():
            try:
                cosines.append(cosine_dict[word])
            except KeyError:
                cosines.append(None)
        df["Sample " + str(count) + " Similarities"] = pd.Series(cosines)
        count += 1
    df.to_csv("CSVs/" + date + "TwoSidedGenderBootstrap.csv")


simple_bootstrap("consume", "luxury", "disease")
