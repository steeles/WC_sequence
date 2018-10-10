
import matplotlib.pyplot as plt
import numpy as np


def generic_plot(x,y,**kwargs):
    """
    generic plot function
    Args:
        x (numpy.array): x axis
        y (numpy.array): will make subplot for each row
        **kwargs:

    Returns:
        matplotlib.pyplot.figure
    """
    fig = plt.figure()
    ax = plt.gca()
    try:
        num_plots = y.shape[1]
        for ind in xrange(num_plots):
            ax.plot(x, y[ind, :])
    except IndexError:
        ax.plot(x, y)

    plt.show(block=False)
    return fig



def plot_stimuli(xax, stim, title, labels):
    pass