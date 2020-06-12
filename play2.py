from sklearn.neighbors import KernelDensity
import numpy as np

import matplotlib.pyplot as plt
import pdb
from rest import RESTClient


ayy = RESTClient("https://www.twitchmetrics.net/c/71092938-xqcow")
res = ayy.make_request("/recent_viewership_values")
pdb.set_trace()


X = np.array([-1, -2, -1.5, -1.25, -1.23 -3, 1, 2, 3])
plt.plot(X, len(X) * [0], "x")
X_plot = np.linspace(-4, 4, 1000)[:, np.newaxis]
#X_fit = list(map(lambda x: [x], X))
#X = np.array([[-1], [-2], [-3], [1], [2], [3]])
pdb.set_trace()
kde = KernelDensity(kernel='gaussian', bandwidth=0.2).fit(X[:, np.newaxis])
X_plot = np.linspace(-4, 4, 1000)[:, np.newaxis]
log_dens = kde.score_samples(X_plot)
pdb.set_trace()
plt.plot(X_plot[:, 0], np.exp(log_dens))
plt.show()
pdb.set_trace()