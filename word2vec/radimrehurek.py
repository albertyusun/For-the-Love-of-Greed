# import packages

from gensim.test.utils import datapath
from gensim import utils
import tempfile
import gensim.models

# memory friendly iterator that reads corpus line-by-line

class MyCorpus(object):
    """An interator that yields sentences (lists of str)."""

    def __iter__(self):
        corpus_path = datapath('lee_background.cor')
        for line in open(corpus_path):
            # assume there's one document per line, tokens separated by whitespace
            yield utils.simple_preprocess(line)

# train a model on the corpus

sentences = MyCorpus()
model = gensim.models.Word2Vec(sentences=sentences)

vec_king = model.wv['king']

# retrieve vocab

for i, word in enumerate(model.wv.vocab):
    if i == 10:
        break
    print(word)


# storing and loading models

with tempfile.NamedTemporaryFile(prefix='gensim-model-', delete=False) as tmp:
    temporary_filepath = tmp.name
    model.save(temporary_filepath)
    #
    # The model is now safely stored in the filepath.
    # You can copy it to other machines, share it with others, etc.
    #
    # To load a saved model:
    #
    new_model = gensim.models.Word2Vec.load(temporary_filepath)