
from sklearn.neighbors import KernelDensity
import numpy as np

import matplotlib.pyplot as plt
import pdb

# Transforms 1D data to a density graph
# https://scikit-learn.org/stable/modules/density.html
def arr_to_kde(X, debug=False, sample_start=-4, sample_end=4, sample_num=1000, bandwidth=0.2, kernel='gaussian'):
    X = np.array(X)
    X_plot = np.linspace(sample_start, sample_end, sample_num)[:, np.newaxis]
#    X_plot = np.linspace(sample_num,sample_end, sample_num)[:, np.newaxis]
    kde = KernelDensity(kernel=kernel, bandwidth=bandwidth).fit(X[:, np.newaxis])
    log_dens = kde.score_samples(X_plot)
    dens = np.exp(log_dens)

    if debug:
        plt.plot(X, len(X) * [0], "x")
        plt.plot(X_plot[:, 0], dens)

    return dens


# Plot a 1d array
def plot_arr(X):
    X = np.array(X)
    plt.plot(X, len(X) * [0], "x")
    plt.show()