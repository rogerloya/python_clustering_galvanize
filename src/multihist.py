from __future__ import division
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as scs


def multihist(x, y, bins=None, binsize=None, left=None, right=None, ymax=None,
              density=1, kde=False, alpha=0.3, figsize=(12, 8), title=None):
    '''
    Plot a set of overlapping histograms with identical bins
    INPUT:
    x:      numpy array; data points to plot
    y:      numpy array of the same length;
            will plot histogram for each unique value of y
    bins:   int; number of bins in histogram
    binsize:float: size of bins (overrides bins)
    left:   lower limit (or None to set to min of data)
    right:   upper limit (or None to set to max of data)
    ymax:   upper limit of y
    density: normalize w each histograph; pass to matplotlib
    kde:    add kde plot
    alpha:  float; opacity; pass to matplotlib
    figsize:tuple; width and height of figure; pass to matplotlib
    title:  str; title of plot
    '''

    fig, ax = plt.subplots(figsize=figsize)

    if not title is None:
        ax.set_title(title)

    # handle specifying left/right by clipping values to that range
    if (left is None) and (right is None):
        xc = x
    else:
        xc = np.clip(x, a_min=left, a_max=right)
    
    xbinmin, xbinmax = xc.min(), xc.max()
    if left is not None:
        xbinmin = min(xbinmin, left)
    if right is not None:
        xbinmax = max(xbinmax, right)

    if binsize == None:
        if bins == None:
            bins = 20
        binsize = (xc.max() - xc.min())/bins
        binarray = np.linspace(xbinmin, xbinmax, bins + 1)
    else:
        binarray = np.arange(xbinmin, xbinmax, binsize)

    if kde:
        xvals = np.linspace(xc.min(), xc.max(), 100)
        kde_scale = 1

    # We need to get the default color cycle to get the same color
    # for the hist and kde line.
    props = plt.rcParams['axes.prop_cycle']

    for yval, prop in zip(np.unique(y), props):
        color = prop['color']
        h = ax.hist(list(xc[y == yval]), alpha=alpha, bins=binarray,
                     density=density, label=str(yval), color=color)
        if kde:
            kde_func = scs.gaussian_kde(xc[y == yval])
            if not density:
                kde_scale = np.sum(y == yval) * binsize
            ax.plot(xvals, kde_scale * kde_func(xvals), color=color)
    ax.set_xlim(left=left, right=right)
    ax.set_ylim(ymax=ymax)

    ax.legend()
    plt.show()
