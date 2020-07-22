from MulticoreTSNE import MulticoreTSNE as TSNE
import matplotlib.pyplot as plt
import gensim
from gensim.models.word2vec import Word2Vec

model = gensim.models.Word2Vec.load("C:/Users/andre/Documents/1470-1494")
print (model.wv.most_similar('libido'))

X = model.wv[model.wv.vocab]

tsne = TSNE(n_components=2)
X_tsne = tsne.fit_transform(X)

plt.scatter(X_tsne[:, 0], X_tsne[:, 1])
plt.show()
