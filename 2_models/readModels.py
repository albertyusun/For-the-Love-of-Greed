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

jewish = ["jew", "jews", "jewe", "jewes", "jewish", "jewishe", "jue", "jues", "iew", "iews", "iewe",
          "iewes", "israelite", "israelites", "israelyte", "israelytes", "jewry", "jeueri", "jeuerie",
          "jeuri", "jeurie", "juweri", "juwerie", "jouerie", "iwri", "giwrie", "giwerie", "judaism",
          "judaisme", "juhede", "jewess", "jewesse", "iewess", "iewesse", "iewesses", "jewesses",
          "jeues", "jeuesse", "jues", "juesse", "juwesse", "gywes"]

jewish_matched = ["jew", "jews", "jewe", "jewes", "jewish", "jewishe", "jue", "jues", "iew", "iews",
                  "iewe", "iewes", "israelite", "israelites", "jewry", "jeueri", "jeuerie", "jeuri",
                  "jeurie", "judaism", "judaisme", "juhede"]

christian = ["christian", "christians", "cristen", "cristens", "christian", "cristien", "cristin",
             "cristins", "cresten", "crestens", "christein", "christeins", "christen", "christens",
             "christendom", "cristendom", "cristendam", "cristendon", "cristendham", "christianity",
             "christianite", "cristenhede"]

slavery = ["slave", "slavery", "enslaved", "servus", "black", "blac", "negro"]

freedom = ["owner", "liberation", "free", "master", "white", "whit", "europid"]


def load_saved_model(date):
    """
    Load saved model.
    :param date: Date of the quarter century file you want to load
    :return: model
    """
    model = gensim.models.Word2Vec.load("C:/Users/djpep/Box Sync/For the Love of Greed Data Storage/"
                                        "models_blank_suffix_quarter_50/"+date)
    return model


def print_random_n(model):
    """
    Print 10 random words from the word embedding model

    :param model:
    :return: nothing, but prints out 10 random words
    """
    n = 5
    print("Ten random words:")
    for i, word in enumerate(model.wv.vocab):
        if i == n:
            break
        print(word)


def most_similar(model, lexicon_words, date_bucket):
    """
    Print and return top 20 most-similar words for a list of given words

    :param model: Loaded word embedding model
    :param lexicon_words: list of lexicon words in a given quarter century
    :param date_bucket: date to check
    :return: top 20-most similar words for a list of given words
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
    """
    Convert dictionary to CSV
    :param file_location: file location
    :param dict: dictionary you want to save
    :return: nothing. it returns the file
    """
    file = open(file_location, "w")
    writer = csv.writer(file)
    for key, value in dict.items():
        writer.writerow([key, value])
    file.close()


def cosine_over_time(word1, word2):
    """
    find cosine similarity over time between two words
    :param word1: first word
    :param word2: second word
    :return: list of similarities
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
    """
    find distance over time between two words
    :param word1: first word
    :param word2: second word
    :return: list of distances
    """
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


def get_vocab(date):
    """
    Get entire vocab of a timespan's word embedding model
    :param date: date
    :return: list of vocabulary
    """
    model = load_saved_model(date)
    vocab = model.wv.vocab
    return vocab


def get_all_vocab():
    # create complete vocabulary before everything else
    print("starting words")
    words = set()
    # add custom words
    custom = []
    for date in date_buckets:
        vf = pd.read_csv("CSVs/spellingvariations/wordVariation" + date + ".csv")
        for col in vf.columns:
            word = col[4:].lower()
            if word not in words:
                custom.append(word)
    words = words.union(set(custom))
    print("finished handling custom words")

    # add the rest of the words
    for date in date_buckets:
        vocab = get_vocab(date)
        words = words.union(vocab)
    return list(words)


def avg_vector(vector_list):
    """
    Turns a list of numpy vectors and returns their average as a numpy vector
    :param vector_list: list of numpy vectors
    :return: numpy vector
    """
    average_vector = np.asarray(vector_list[0])  # how to initialize a numpy vector?
    for vec in vector_list[1:]:
        average_vector = np.add(average_vector, vec)
    average_vector = average_vector / len(vector_list)
    return average_vector


def avg_consumption_spelling_vectors(date):
    """
    Generates the average vectors of each word (given its spelling variants) and returns a dictionary of words and their
    vectors that represent the average of all of its' spelling variations' numpy

    :param date:
    :return: dictionary of words and their average vectors
    """
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


def consumption_assessment(date, vectors):
    vecs = load_model_vectors(date)

    # need to create cultural vector
    culture_vector = avg_vector(list(avg_consumption_spelling_vectors(date).values()))

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


def one_sided_consumption_over_time():
    df = pd.DataFrame()
    words = get_all_vocab()
    df["Words"] = words
    print("words finished")

    for date in date_buckets:
        word_vectors = avg_consumption_spelling_vectors(date)

        full_cosine_dict = consumption_assessment(date, word_vectors)
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
        print(date, "consumerism", "finished")

        df[date + " Consumerism Similarities"] = pd.Series(cosines)
        df[date + " Consumerism Z-Scores"] = pd.Series(z_scores)
    print("writing csv")
    df.to_csv("OneSidedConsumerismAxisSimilarities.csv")


def twosided_assessment(dimension1, dimension2, date, vectors):
    vecs = load_model_vectors(date)

    axis_vector = twosided_cultural_dimension_vector(dimension1, dimension2, date)

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


def twosided_cultural_dimension_vector(dimension1, dimension2, date):
    vecs = load_model_vectors(date)

    # need to create axis vector
    differences = []
    for i in range(len(dimension1)):
        try:
            dim1_temp = get_vector(dimension1[i], vecs)
            dim2_temp = get_vector(dimension2[i], vecs)
            differences.append(np.subtract(dim1_temp, dim2_temp))
        except KeyError:
            print("Could not find", dimension1[i], "or", dimension2[i], "in", date)

    # now average all the difference vectors together
    axis_vector = avg_vector(differences)
    return axis_vector


def onesided_assessment(dimension, date, vectors):
    """
    dimension should be the list of cultural words to be measured, like masculine or feminine for a given csv,
    calculates the cosine of every word relative to one side of the dimension outputs this as a dictionary

    :param dimension: list of words from one side of cultural dimension
    :param date: date
    :param vectors: vector list (one with spelling variation created through avg
    :return: cosine_similarities: dictionary with words paired with their cosine similarities
    """
    vecs = load_model_vectors(date)

    culture_vector = onesided_cultural_dimension_vector(dimension, date)

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


def onesided_cultural_dimension_vector(dimension, date):
    vectors = load_model_vectors(date)
    vecs = []

    for word in dimension:
        try:
            vecs.append(get_vector(word, vectors))
        except KeyError:
            print(word, "not found in", date)
    avg = avg_vector(vecs)
    return avg


# compare a word vector to masculine and feminine clusters to see individual relationships with those ve
def gender_ztest_assessment(word):
    for date in date_buckets:
        vecs = load_model_vectors(date)
        masculine_vectors = []
        feminine_vectors = []
        for i in range(len(masculine)):
            try:
                masculine_vectors.append(get_vector(masculine[i], vecs))
            except KeyError:
                print("Could not find", masculine[i], " in ", date)
        for i in range(len(feminine)):
            try:
                feminine_vectors.append(get_vector(feminine[i], vecs))
            except KeyError:
                print("Could not find", feminine[i], " in ", date)
        avg_man = 1 - scipy.spatial.distance.cosine(vecs[word], avg_vector(masculine_vectors))
        avg_woman = 1 - scipy.spatial.distance.cosine(vecs[word], avg_vector(feminine_vectors))
        print(date, word, "average man cos sim:", avg_man, "average woman cos sim:", avg_woman)
    return (masculine_vectors, feminine_vectors)


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
    cosines = []
    for date in date_buckets:
        average = onesided_cultural_dimension_vector(jewish, date)
        # axis = avg_vector(list(avg_consumption_spelling_vectors(date).values()))
        axis = twosided_cultural_dimension_vector(feminine, masculine, date)
        cosine = 1 - scipy.spatial.distance.cosine(average, axis)
        cosines.append(cosine)
    for i in cosines:
        print(i)

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
