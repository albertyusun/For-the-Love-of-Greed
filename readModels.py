import gensim
import time
import numpy
import pandas as pd
import csv
import scipy
import numpy as np

quarter_date_buckets = ["1470-1494", "1495-1519", "1520-1544", "1545-1569",
                        "1570-1594", "1595-1619", "1620-1644", "1645-1669",
                        "1670-1700"]

date_buckets = ["1470-1494", "1495-1519", "1520-1544", "1545-1569",
                        "1570-1594", "1595-1619", "1620-1644", "1645-1669",
                        "1670-1700"]

decade_date_buckets = ["1470-1479", "1480-1489", "1490-1499",
                       "1500-1509", "1510-1519", "1520-1529", "1530-1539", "1540-1549", "1550-1559",
                       "1560-1569", "1570-1579", "1580-1589", "1590-1599", "1600-1609", "1610-1619",
                       "1620-1629", "1630-1639", "1640-1649", "1650-1659", "1660-1669", "1670-1679",
                       "1680-1689", "1690-1700"]

lexicon = ['consumption', 'consume', 'cupidity', 'cupiditas', 'curiosity', 'curiositas',
           'greed', 'desire', 'appetite', 'lust', 'libido', 'covetousness', 'avarice',
           'possess', 'possession', 'possessing', 'busy', 'businesse', 'need', 'necessity',
           'necessary', 'needing', 'meed', 'bowgeor', 'bougeor', 'budge', 'wastour',
           'waster', 'wasture', 'wastoure', 'speculation', 'debt', 'debitum', 'expense',
           'gain', 'miser', 'fortune', 'fortuna', 'use', 'usury', 'interest',
           'interesse', 'consumptioner']

masculine = ["man", "manne", "mannes", "men", "mennes", "he", "his", "him", "son",
                 "sons", "father", "fathers", "boy", "boys", "himself", "male", "males", "brother",
                 "brothers", "uncle", "uncles", "nephew", "nephews", "lord", "lords", "king", "kings",
                 "duke", "dukes", "prince", "princes"]

feminine = ["woman", "womman", "wommans", "women", "wommens", "she", "hers", "her", "daughter",
                "daughters", "mother", "mothers", "girl", "girls", "herself", "female", "females",
                "sister", "sisters", "aunt", "aunts", "niece", "nieces", "lady", "ladies", "queen",
                "queens", "duchess", "duchesses", "princess", "princesses"]


def create_model(input):
    df = pd.read_csv(input, encoding="utf-8")
    print("1. Read csv.")
    df['booktext'] = df['booktext'].str.split()
    print("2. Split csv.")
    model = gensim.models.word2vec.Word2Vec(sentences=df["booktext"], workers=4, min_count=1, size=300)
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


def load_saved_model(date):
    model = gensim.models.Word2Vec.load("C:/Users/djpep/Box Sync/For the Love of Greed Data Storage/"
                                        "models_blank_suffix_quarter_50/"+date)
    return model


def read_model(address):
    new_model = gensim.models.Word2Vec.load(
        "C:/Users/Albert/Box Sync/For the Love of Greed Data Storage/models/1470-vocab.pkl")


def print_random_n(model, topn):
    """
    Print 10 random words from the word embedding model
    """
    print("Ten random words:")
    for i, word in enumerate(model.wv.vocab):
        if i == topn:
            break
        print(word)


def most_similar(model, lexicon_words, date_bucket):
    """
    Receive model and list of lexicon words in a quarter century

    Print and return top 20 most-similar words for a list of given words
    """
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
    prints cosine similarity over time and returns list of similarities
    """
    similarity_list = []
    similarity = "NA"
    for date_bucket in date_buckets:
        try:
            model = load_saved_model(date_bucket)
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
            model = load_saved_model(date_bucket)
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
            "C:/Users/Albert/Box Sync/For the Love of Greed Data Storage/models_blank_suffix/" + date)
        vectors = model.wv
        vectors.save("C:/Users/Albert/Box Sync/For the Love of Greed Data Storage/models_blank_suffix/" + date + ".kv")


def get_vocab(date):
    model = load_saved_model(date)
    vocab = model.wv.vocab
    return vocab


def gender_dimension(date):
    """
    for a given csv, calculates the cosine of every word relative to the gender dimension.
    outputs this as a list (ideally should output as a numpy vector?)
    """
# takes in a list of numpy vectors and returns their average as a numpy vector
def avg_vector(vector_list):
    average_vector = np.asarray(vector_list[0])  # how to initialize a numpy vector?
    for vec in vector_list[1:]:
        average_vector = np.add(average_vector, vec)
    average_vector = average_vector / len(vector_list)
    return average_vector


# generates the average vectors of each word (given its spelling variants) and returns a dictionary
# of words and their average vectors
def avg_spelling_vectors(date):
    df = pd.read_csv("CSVs/spellingvariations/wordVariation" + date + ".csv")
    vectors = load_model_vectors(date)
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
                    vecs.append(get_vector(variant, vectors))
                except KeyError:
                    print(variant, "not found in", date)
        word_vectors[base_words[i]] = avg_vector(vecs)
    return word_vectors


# for a given csv, calculates the cosine of every word relative to the gender dimension.
# outputs this as a dictionary
def gender_dimension(date):
    vecs = load_model_vectors(date)

    # need to create axis vector
    differences = []
    for i in range(len(feminine)):
        try:
            male_temp = get_vector(masculine[i], vecs)
            female_temp = get_vector(feminine[i], vecs)
            differences.append(np.subtract(female_temp, male_temp))
        except KeyError:
            print("Could not find", masculine[i], "or", feminine[i], "in", date)

    # now average all the difference vectors together
    axis_vector = avg_vector(differences)

    # now, we need to produce the cosine similarities
    cosine_similarities = {}
    for i, word in enumerate(get_vocab(date)): # change if just doing lexicon
        cosine_similarities[word] = 1 - scipy.spatial.distance.cosine(vecs[word], axis_vector)
    return cosine_similarities


# dimension should be the list of cultural words to be measured, like masculine or feminine
# for a given csv, calculates the cosine of every word relative to one side of the dimension
# outputs this as a dictionary
def one_sided_assessment(dimension, date, vectors):
    vecs = load_model_vectors(date)

    # need to create cultural vector
    culture_vectors = []
    for i in range(len(dimension)):
        try:
            culture_temp = get_vector(dimension[i], vecs)
            culture_vectors.append(culture_temp)
        except KeyError:
            print("Could not find", dimension[i], "in", date)
    culture_vector = avg_vector(culture_vectors)

    # now, we need to produce the cosine similarities
    cosine_similarities = {}
    for i, word in enumerate(get_vocab(date)):
        if word not in vectors.keys():
            cosine_similarities[word] = 1 - scipy.spatial.distance.cosine(vecs[word], culture_vector)
        else:
            cosine_similarities[word] = 1 - scipy.spatial.distance.cosine(vectors[word], culture_vector)
    for word in vectors.keys():
        if word not in cosine_similarities.keys():
            cosine_similarities[word] = 1 - scipy.spatial.distance.cosine(vectors[word], culture_vector)
    return cosine_similarities


# creates a table like custom_gender_over_time, but is one-sided
def onesided_gender_over_time():
    # create complete vocabulary before everything else
    print("starting words")
    words = set()
    # add custom words
    custom = []
    for date in date_buckets[0:2]:
        vf = pd.read_csv("CSVs/spellingvariations/wordVariation" + date + ".csv")
        for col in vf.columns:
            word = col[4:].lower()
            if word not in words:
                custom.append(word)
    words = words.union(set(custom))
    print("finished handling custom words")

    # add the rest of the words
    for date in date_buckets[0:2]:
        vocab = get_vocab(date)
        words = words.union(vocab)
    print("uploading words")
    df = pd.DataFrame()
    df["Words"] = list(words)
    print("words finished")

    for date in date_buckets[0:2]:
        word_vectors = avg_spelling_vectors(date)

        for dim in [masculine, feminine]:
            full_cosine_dict = one_sided_assessment(dim, date, word_vectors)
            full_z_dict = z_test(full_cosine_dict)

            cosines = []
            z_scores = []

            for word in words:
                try:
                    cosines.append(full_cosine_dict[word])
                    z_scores.append(full_z_dict[word])
                except KeyError:
                    cosines.append(None)
                    z_scores.append(None)
            print(date, dim[0], "finished")

            df[date + " " + dim[0] + " Similarities"] = pd.Series(cosines)
            df[date + " " + dim[0] + " Z-Scores"] = pd.Series(z_scores)

    print("writing csv")
    df.to_csv("OneSidedGenderData.csv")


# for a given csv, calculates the cosine of every word relative to the gender dimension.
# outputs this as a dictionary. This version takes in a specific dictionary of word vectors.
# This assumes that all of the vectors actually exist in the specified date.
def gender_dimension(date, vectors):
    vecs = load_model_vectors(date)

    # need to create axis vector
    differences = []
    for i in range(len(feminine)):
        try:
            male_temp = get_vector(masculine[i], vecs)
            female_temp = get_vector(feminine[i], vecs)
            differences.append(np.subtract(female_temp, male_temp))
        except KeyError:
            print("Could not find", masculine[i], "or", feminine[i], "in", date)

    # now average all the difference vectors together
    axis_vector = avg_vector(differences)

    # now, we need to produce the cosine similarities
    cosine_similarities = {}
    for i, word in enumerate(get_vocab(date)):
        if word not in vectors.keys():
            cosine_similarities[word] = 1 - scipy.spatial.distance.cosine(vecs[word], axis_vector)
        else:
            cosine_similarities[word] = 1 - scipy.spatial.distance.cosine(vectors[word], axis_vector)
    for word in vectors.keys():
        if word not in cosine_similarities.keys():
            cosine_similarities[word] = 1 - scipy.spatial.distance.cosine(vectors[word], axis_vector)
    return cosine_similarities


def z_test(word_dict):
    """
    input a dictionary of words as keys and cosine similarities as values.
    get back a dictionary containing only the words with statistically significant similarities
    this assumes a confidence level of .05
    """
    keys = list(word_dict.keys())
    values = np.array(list(word_dict.values()))
    scores = scipy.stats.zscore(values)
    scores = scores.tolist()

    sig_dict = {}
    for j in range(len(keys)):
        if scores[j] != 0:
            sig_dict[keys[j]] = scores[j]
    return sig_dict

def gender_over_time():
    """
    creates a csv finding the cosine similarity of every word in each quarter-century to the gender axis.
    also finds z-scores for each word
    """

    # code to go through all vocabulary:
    # print("starting words")
    # words = []
    # for date in date_buckets:
    #     vocab = get_vocab(date)
    #     for i, word in enumerate(vocab):
    #         if word not in words:
    #             words.append(word)
    # print("uploading words")
    # df = pd.DataFrame()
    # df["Words"] = words
    # print("words finished")

    df = pd.DataFrame()
    df["Words"] = lexicon

    for date in date_buckets:
        cosine_dict = gender_dimension(date)
        z_dict = z_test(cosine_dict)

        cosines = []
        z_scores = []

        for word in lexicon:
            try:
                cosines.append(cosine_dict[word])
                z_scores.append(z_dict[word])
            except KeyError:
                cosines.append(0)
                z_scores.append(0)

        df[date+" Similarities"] = pd.Series(cosines)
        df[date+" Z-Scores"] = pd.Series(z_scores)

    df.to_csv("GenderDimensionData.csv")


# creates a csv finding the cosine similarity of every word in each quarter-century to the gender axis.
# creates a csv finding the cosine similarity of every word in each quarter-century to the gender axis.
# also finds z-scores for each word. This one uses the avg vectors of our lexicon words
def custom_gender_over_time():
    # create complete vocabulary before everything else
    print("starting words")
    words = set()
    # add custom words
    custom = []
    for date in date_buckets[0:2]:
        vf = pd.read_csv("CSVs/spellingvariations/wordVariation" + date + ".csv")
        for col in vf.columns:
            word = col[4:].lower()
            if word not in words:
                custom.append(word)
    words = words.union(set(custom))
    print("finished handling custom words")

    # add the rest of the words
    for date in date_buckets[0:2]:
        vocab = get_vocab(date)
        words = words.union(vocab)
    print("uploading words")
    df = pd.DataFrame()
    df["Words"] = list(words)
    print("words finished")

    for date in date_buckets[0:2]:
        word_vectors = avg_spelling_vectors(date)
        full_cosine_dict = gender_dimension(date, word_vectors)
        full_z_dict = z_test(full_cosine_dict)

        cosines = []
        z_scores = []

        for word in words:
            try:
                cosines.append(full_cosine_dict[word])
                z_scores.append(full_z_dict[word])
            except KeyError:
                cosines.append(None)
                z_scores.append(None)
        print(date, "finished")

        df[date+" Similarities"] = pd.Series(cosines)
        df[date+" Z-Scores"] = pd.Series(z_scores)

    print("writing csv")
    df.to_csv("NewGenderDimensionData.csv")


def load_model_vectors(date_bucket):
    """
    Load model vectors for one vector date_bucket
    """
    try:
        vectors = gensim.models.KeyedVectors.load("output/" + date_bucket + ".kv")
    except FileNotFoundError:
        model = load_saved_model(date_bucket)
        vectors = model.wv
        vectors.save("output/" + date_bucket + ".kv")
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
            model = load_model_vectors(date)
            print(date, "", a1, "is to", a2, "as", b1, "is to",
                  model.wv.most_similar_cosmul(positive=[a2, b1], negative=[a1])[0])
        except KeyError:
            print("can't find 1-3 vectors in", date)


def average(lst):
    return sum(lst) / len(lst)


def distance_vector(control_word, date, lexicon):
    """
    calculate average embedding bias between a specific signal word and a lexicon words
    """
    model = load_saved_model(date)
    distance = []
    for lexicon_word in lexicon:
        distance.append(model.wv.distance(control_word, lexicon_word))
    # [print(x) for x in distance]
    return distance


def extract_lexicon_words(year):
    ret = []
    df = pd.read_csv(
        "C:/Users/Albert/Box Sync/For the Love of Greed Data Storage/word_variation/wordVariation" + year + ".csv",
        encoding="utf-8")
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
    return scipy.stats.kstest(list1, list2)

if __name__ == "__main__":
    print(gender_ztest_assessment("consume"))

    # print gender dimension
    # year = "1470-1494"
    # cosine_dict = gender_dimension(year)
    # i = 0
    # # print the first 20:
    # for k, v in cosine_dict.items():
    #     print(k, v)
    #     i += 1
    #     if i == 20:
    #         break

    # conduct ks test between lexicon words:
    # lexicon = extract_lexicon_words(year)
    # print(ks_test(distance_vector("man", year, lexicon), distance_vector("woman", year, lexicon)))
    # print("average distance from man and lexicon words is", average(distance_vector("man", year, lexicon)))
    # print("average distance from man and lexicon words is", average(distance_vector("woman", year, lexicon)))

    # find analogies:
    # analogy_over_time("sun","moon","king")
    # analogy_over_time("man","woman","king")

    # find cosine similarity:
    # print(cosine_over_time('family', 'luxury'))
    # print(cosine_over_time('family', 'consume'))

    # make top similar words csv:
    # final_dict = find_lexicon_top_words("CSVs/lexiconCount1470-1700.csv")
    # print(final_dict)
    # dict_to_csv("CSVs/most_similar_lexicon_1400-1700_top20.csv", final_dict)
