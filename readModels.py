import gensim
import time
import pandas as pd
import csv

date_buckets = ["1470-1494", "1495-1519","1520-1544","1545-1569",
                "1570-1594","1595-1619","1620-1644","1645-1669",
                "1670-1700"]

def create_model(input):
    df = pd.read_csv(input, encoding="ISO-8859-1")
    print("1. Read csv.")
    df['booktext'] = df['booktext'].str.split()
    print("2. Split csv.")
    model = gensim.models.word2vec.Word2Vec(sentences=df["booktext"], workers=4, min_count=1, size=50)
    print("3. Created model.")
    return model

def save_model(model):
    import tempfile
    with tempfile.NamedTemporaryFile(prefix='gensim-model-', delete=False) as tmp:
        temporary_filepath = tmp.name
        model.save(temporary_filepath)
        #
        # The model is now safely stored in the filepath.
        # You can copy it to other machines, share it with others, etc.
        #
    return temporary_filepath

def load_saved_model(temporary_filepath):
    new_model = gensim.models.Word2Vec.load(temporary_filepath)

def read_model(address):
    new_model = gensim.models.Word2Vec.load(
        "C:/Users/Albert/Box Sync/For the Love of Greed Data Storage/models/1470-vocab.pkl")

def print_random_n(model,topn):
    '''
    Print 10 random words from the word embedding model
    '''
    print("Ten random words:")
    for i, word in enumerate(model.wv.vocab):
        if i == topn:
            break
        print(word)

def most_similar(model, lexicon_words, date_bucket):
    '''
    Receive model and list of lexicon words in a quarter century

    Print and return top 20 most-similar words for a list of given words
    '''
    words_dict = {}
    for lexicon_word in lexicon_words:
        try:
            lex_word_without_star = lexicon_word[:-1]
        except TypeError:
            break
        print("Most Similar words for " + lex_word_without_star + " in " + date_bucket)
        words_with_cosine = []
        try:
            words_with_cosine = model.wv.most_similar(lex_word_without_star, topn=20)
        except KeyError:
            print("cannot find " + lex_word_without_star)
        words_dict[lex_word_without_star + "_" + date_bucket] = [n[0] for n in words_with_cosine]
        [print(n) for n in words_dict[lex_word_without_star + "_" + date_bucket]] # print for aesthetic
    return words_dict

def find_lexicon_top_words(csv):
    """
    Goal: Take in Andrew's CSV of top words and find the most similar words for each of them in each quarter-century
    time period

    Returns a dictionary, final_dict, which is a dictionary with keys in the format: "lexiconword_datebucket" and values
    of similar words in its years' models.
    """
    final_dict = {}
    df = pd.read_csv(csv)
    for date_bucket in date_buckets:
        model = gensim.models.Word2Vec.load("C:/Users/Albert/Box Sync/For the Love of Greed Data Storage/models_blank_suffix/" + date_bucket)
        final_dict.update(most_similar(model, df[date_bucket + "words"], date_bucket)) # add the output from most_similar to the returned dictionary
    return final_dict

def dict_to_csv(file_location, dict):
    file = open(file_location, "w")
    writer = csv.writer(file)
    for key, value in dict.items():
        writer.writerow([key, value])
    file.close()

def cosine_over_time(word1, word2):
    """
    prints cosine similarity over time
    """
    for date_bucket in date_buckets:
        try:
            model = gensim.models.Word2Vec.load("C:/Users/djpep/Box Sync/For the Love of Greed Data Storage/models_blank_suffix/" + date_bucket)
            print(date_bucket, "Cosine similarity between", word1, "and", word2, "=", model.wv.similarity(word1, word2))
        except KeyError:
            print("can't find 1-2 of the words in ", date_bucket)


def distance_over_time(word1, word2):
    for date_bucket in date_buckets:
        try:
            model = gensim.models.Word2Vec.load("C:/Users/djpep/Box Sync/For the Love of Greed Data Storage/models_blank_suffix/" + date_bucket)
            print(date_bucket, "Distance between", word1, "and", word2, "=", model.wv.distance(word1, word2))
        except KeyError:
            print("can't find 1-2 of the words in", date_bucket)

if __name__ == "__main__":
    # code to find cosine similarity:
    cosine_over_time('consume', 'luxury')
    cosine_over_time('consume', 'disease')
    '''
    # code to make top similar words csv:
    final_dict = find_lexicon_top_words("CSVs/lexiconCount1470-1700.csv")
    print(final_dict)
    dict_to_csv("CSVs/most_similar_lexicon_1400-1700_top20.csv", final_dict)
    '''
