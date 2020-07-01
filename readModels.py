import gensim
import time
import pandas as pd


def create_model(input):
    df = pd.read_csv(input, encoding="ISO-8859-1")
    print("read csv")
    df['booktext'] = df['booktext'].str.split()
    print("split csv")
    model = gensim.models.word2vec.Word2Vec(sentences=df["booktext"], workers=4, min_count=1, size=50)
    print("created model")
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

def most_similar(model, words):
    start = time.time()  # take time
    for word in words:
        result = model.wv.most_similar(word)
        print(result)
    end = time.time()  # take time
    print(end - start)

if __name__ == "__main__":
    model = create_model("C:/Users/Albert/Box Sync/For the Love of Greed Data Storage/1470-1494.csv")
    for i, word in enumerate(model.wv.vocab):
        if i == 10:
            break
        print(word)
    words = ['god']
    most_similar(model, words)
