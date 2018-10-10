
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
        bad_access = y.shape[1]
        num_plots = y.shape[0]
        for ind in xrange(num_plots):
            ax = fig.add_subplot(num_plots, 1, ind + 1)
            ax.plot(x, y[ind, :])
    except IndexError:
        ax.plot(x, y)

    plt.show(block=False)
    return fig


def plot_triplet_stimuli(tax, stim, title=None, labels=None):
    """
    Pre-fab function to plot stimuli
    Args:
        tax (numpy.array): time axis (should be in seconds, or provide a label
        stim (nump.ndarray): 3 x triplet period in simulation timesteps
        title (str): title for the figure
        labels (array): labels[0] for xlabel, labels[1] for ylabel
    Returns:
        matplotlib.pyplot.figure
    """
    fig = plt.figure()  # pylab figure
    foo = plt.gca()
    plt.title(title)
    #title('ITI = ' + str(ITI * 1000) + ' ms, df = ' + str(df))
    # foo.axes.get_xaxis().set_ticks([])  # turn off those nasty ticks
    # foo.axes.get_yaxis().set_ticks([])
    if labels[0]:
        plt.xlabel(labels[0])

    else:
        plt.xlabel('time (s)')
    n_units = stim.shape[0]
    for ind in xrange(n_units):
        ax = fig.add_subplot(n_units, 1, ind + 1)
        plt.ylabel('u' + str(ind + 1))
        plt.ylim(-.2, 1)
        #	ax.plot(tax,E[ind,:],'b');
        #	ax.plot(tax,a[ind,:],'r');
        ax.plot(tax, stim[ind, :], 'g')
    #	ax.plot(tax,Isyn[ind,:],'c')
    # title(str(ind+1))
    # plot(tax,E,'b')
    # plot(tax,I,'r')
    # plot(tax,Inp_e,'g')
    plt.show(block=False)
    return fig