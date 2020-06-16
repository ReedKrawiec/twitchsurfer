
from sklearn.neighbors import KernelDensity
from PIL import Image, ImageDraw
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

def draw_activity_chart(probs):
    SQUARE_SIZE = 20
    LABEL_SIZE = 40

    w, h = (48 * SQUARE_SIZE), (7 * SQUARE_SIZE)
    
    # creating new Image object 
    img = Image.new("RGB", (w + LABEL_SIZE, h + LABEL_SIZE)) 
    
    # create rectangle image 
    img1 = ImageDraw.Draw(img)

    x = 0
    y = 0
    for i in range(len(probs)):
        prob = probs[i]
        img1.rectangle([(x, y), (x + SQUARE_SIZE, y + SQUARE_SIZE)], fill =(0, int(255 * prob), 0, 128), outline ="red")
        img1.text((x, y), str(round(prob, 1)), fill=(255,255,255,128), spacing=1)
        x += SQUARE_SIZE

        if (i + 1) % 48 == 0:
            x = 0
            y += SQUARE_SIZE

    #for y in range(0, h, SQUARE_SIZE):
    #    for x in range(0, w, SQUARE_SIZE):
    #        img1.rectangle([(x, y), (x + SQUARE_SIZE, y + SQUARE_SIZE)], fill ="#ffff33", outline ="red")
    #        #img1.text((x, y), "(" + str(x) + "," + str(y) + ")", fill=(0,0,0,128))
    img.show() 