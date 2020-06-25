import time

from sklearn.decomposition import IncrementalPCA  # inital reduction
from sklearn.datasets import load_digits
#from sklearn.manifold import TSNE  # final reduction
from cuml.manifold import TSNE

import numpy as np  # array handling
from gensim.models import Word2Vec
from plotly.offline import init_notebook_mode, iplot, plot
import plotly.graph_objs as go
import pandas as pd


def reduce_dimensions(model):
    num_dimensions = 2  # final num dimensions (2D, 3D, etc)

    vectors = []  # positions in vector space
    labels = []  # keep track of words to label our data again later
    i=0
    for word in model.wv.vocab:
        vectors.append(model.wv[word])
        labels.append(word)
        print(word)
        i+=1
        print(i)
    print("done with adding words to lists")

    # convert both lists into numpy vectors for reduction
    vectors = np.asarray(vectors)
    labels = np.asarray(labels)
    print("done converting to numpy vectors")

    # reduce using T-Distributed Stochastic Neighbor Embedding
    vectors = np.asarray(vectors)
    tsne = TSNE(n_components=num_dimensions, random_state=0)
    vectors = tsne.fit_transform(vectors)
    print("done reducing")

    x_vals = [v[0] for v in vectors]
    y_vals = [v[1] for v in vectors]
    return x_vals, y_vals, labels


def plot_with_plotly(x_vals, y_vals, labels, plot_in_notebook=True):
    trace = go.Scatter(x=x_vals, y=y_vals, mode='text', text=labels)
    data = [trace]

    if plot_in_notebook:
        init_notebook_mode(connected=True)
        iplot(data, filename='word-embedding-plot')
    else:
        plot(data, filename='word-embedding-plot.html')


def plot_with_matplotlib(x_vals, y_vals, labels):
    import matplotlib.pyplot as plt
    import random

    random.seed(0)

    plt.figure(figsize=(12, 12))
    plt.scatter(x_vals, y_vals)

    #
    # Label randomly subsampled 25 data points
    #
    indices = list(range(len(labels)))
    selected_indices = random.sample(indices, 25)
    for i in selected_indices:
        plt.annotate(labels[i], (x_vals[i], y_vals[i]))


def main():
    before = time.time()
    model = Word2Vec.load("../CSVs/1580w2v.model")
    mid = time.time() - before
    print("uploaded model, ", mid)
    x_vals, y_vals, labels = reduce_dimensions(model)
    data = {'Labels': labels,
            'x': x_vals,
            'y': y_vals
            }
    df = pd.DataFrame(data, columns=['Labels', 'x', 'y'])
    print(df)


'''
    try:
        get_ipython()
    except Exception:
        plot_function = plot_with_matplotlib
    else:
        plot_function = plot_with_plotly

    plot_function(x_vals, y_vals, labels)
'''

if __name__ == "__main__":
    main()
