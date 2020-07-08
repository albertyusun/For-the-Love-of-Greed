import gensim
import time
import pandas as pd
import csv
from scipy import stats
import numpy as np

quarter_date_buckets = ["1470-1494", "1495-1519", "1520-1544", "1545-1569",
                        "1570-1594", "1595-1619", "1620-1644", "1645-1669",
                        "1670-1700"]

decade_date_buckets = ["1470-1479", "1480-1489", "1490-1499",
                       "1500-1509", "1510-1519", "1520-1529", "1530-1539", "1540-1549", "1550-1559",
                       "1560-1569", "1570-1579", "1580-1589", "1590-1599", "1600-1609", "1610-1619",
                       "1620-1629", "1630-1639", "1640-1649", "1650-1659", "1660-1669", "1670-1679",
                       "1680-1689", "1690-1700"]


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


def print_random_n(model, topn):
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
        [print(n) for n in words_dict[lex_word_without_star + "_" + date_bucket]]  # print for aesthetic
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
        model = gensim.models.Word2Vec.load(
            "C:/Users/Albert/Box Sync/For the Love of Greed Data Storage/models_blank_suffix/" + date_bucket)
        final_dict.update(most_similar(model, df[date_bucket + "words"],
                                       date_bucket))  # add the output from most_similar to the returned dictionary
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
    similarity_list = []
    similarity = "NA"
    for date_bucket in decade_date_buckets:
        try:
            model = gensim.models.Word2Vec.load(
                "C:/Users/albert/Box Sync/For the Love of Greed Data Storage/models_blank_suffix_decade_300/" + date_bucket)
            similarity = model.wv.similarity(word1, word2)
            similarity_list.append(similarity)
            print(date_bucket, "Cosine similarity between", word1, "and", word2, "=", similarity)
        except KeyError:
            print("can't find 1-2 of the words in ", date_bucket)
            similarity_list.append("NA")
    return similarity_list


def distance_over_time(word1, word2):
    distance_list = []
    distance = "NA"
    for date_bucket in date_buckets:
        try:
            model = gensim.models.Word2Vec.load(
                "C:/Users/Albert/Box Sync/For the Love of Greed Data Storage/models_blank_suffix_decade/" + date_bucket)
            distance = model.wv.distance(word1, word2)
            distance_list.append(distance)
            print(date_bucket, "Distance between", word1, "and", word2, "=", distance)
        except KeyError:
            print("can't find 1-2 of the words in", date_bucket)
            distance_list.append("NA")
    return distance_list


def model_to_vec():
    for date in date_buckets:
        model = gensim.models.Word2Vec.load(
            "C:/Users/djpep/Box Sync/For the Love of Greed Data Storage/models_blank_suffix/" + date)
        vectors = model.wv
        vectors.save("C:/Users/djpep/Box Sync/For the Love of Greed Data Storage/models_blank_suffix/" + date + ".kv")




# for a given csv, calculates the cosine of every word relative to the gender dimension.
# outputs this as a list (ideally should output as a numpy vector?)
def gender_dimension(date):
    masculine = ["man", "manne", "mannes", "men", "mennes", "he", "his", "him", "son",
                 "sons", "father", "fathers", "boy", "boys", "himself", "male", "males", "brother",
                 "brothers", "uncle", "uncles", "nephew", "nephews", "lord", "lords", "king", "kings",
                 "duke", "dukes", "prince", "princes"]

    feminine = ["woman", "womman", "wommans", "women", "wommens", "she", "hers", "her", "daughter",
                "daughters", "mother", "mothers", "girl", "girls", "herself", "female", "females",
                "sister", "sisters", "aunt", "aunts", "niece", "nieces", "lady", "ladies", "queen",
                "queens", "duchess", "duchesses", "princess", "princesses"]

    vecs = load_model_vectors(date)

    # need to create axis vector
    differences = []
    for i in range(len(feminine)):
        try:
            male_temp = get_vector(masculine[i], vecs)
            female_temp = get_vector(feminine[i], vecs)
            differences.append(female_temp - male_temp)
        except KeyError:
            print("Could not find", masculine[i], "or", feminine[i], "in", date)

    # now average all the difference vectors together
    axis_vector = np.asarray() # how to initialize a numpy vector?
    for vec in differences:
        axis_vector += vec
    axis_vector = axis_vector / len(masculine)




def load_model_vectors(date_bucket):
    """
    Load model vectors for one vector date_bucket
    """
    vectors = gensim.models.KeyedVectors.load(
        "C:/Users/djpep/Box Sync/For the Love of Greed Data Storage/models_blank_suffix/" + date_bucket + ".kv")
    return vectors


def get_vector(word, vectors):
    """
    Takes a system of vectors from load_model_vectors to find vectors
    """
    return vectors[word]


# given analogy a1 : a2 :: b1 : __, it fills in the blank.
def analogy_over_time(a1, a2, b1):
    for date in quarter_date_buckets:
        try:
            model = gensim.models.Word2Vec.load("C:/Users/djpep/Box Sync/For the Love of Greed Data Storage/models_blank_suffix/" + date)
            print(date, "", a1, "is to", a2, "as", b1, "is to", model.wv.most_similar_cosmul(positive=[a2, b1], negative=[a1])[0])
        except KeyError:
            print("can't find 1-3 vectors in", date)


def average(lst):
    return sum(lst) / len(lst)


def distance_vector(control_word, date, lexicon):
    """
    calculate average embedding bias between a specific signal word and a lexicon words
    """
    model = gensim.models.Word2Vec.load(
        "C:/Users/Albert/Box Sync/For the Love of Greed Data Storage/models_blank_suffix_quarter_50/" + date)
    distance = []
    for lexicon_word in lexicon:
        distance.append(model.wv.distance(control_word, lexicon_word))
    # [print(x) for x in distance]
    return distance


def extract_lexicon_words(year):
    ret = []
    df = pd.read_csv(
        "C:/Users/Albert/Box Sync/For the Love of Greed Data Storage/word_variation/wordVariation" + year + ".csv",
        encoding="ISO-8859-1")
    columns = list(df)
    for column in columns:
        [ret.append(x) for x in df[column].values.tolist()]
    cleaned_list = [x for x in ret if str(x) != 'nan']
    print("lexicon total", cleaned_list)
    return cleaned_list


def ks_test(list1, list2):
    """
    Compares 2 distributions given 2 lists
    """
    return stats.kstest(list1, list2)


if __name__ == "__main__":
    year = "1470-1494"
    lexicon = extract_lexicon_words(year)
    print(ks_test(distance_vector("man", year, lexicon), distance_vector("woman", year, lexicon)))
    print("average distance from man and lexicon words is", average(distance_vector("man", year, lexicon)))
    print("average distance from man and lexicon words is", average(distance_vector("woman", year, lexicon)))

    # code to find analogies:
    # analogy_over_time("sun","moon","king")
    # analogy_over_time("man","woman","king")

    # code to find cosine similarity:
    # print(cosine_over_time('family', 'luxury'))
    # print(cosine_over_time('family', 'consume'))

    '''
    # code to make top similar words csv:
    final_dict = find_lexicon_top_words("CSVs/lexiconCount1470-1700.csv")
    print(final_dict)
    dict_to_csv("CSVs/most_similar_lexicon_1400-1700_top20.csv", final_dict)
    '''
