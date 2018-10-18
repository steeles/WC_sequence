
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
    xmin, xmax = np.min(x), np.max(x)
    margx = np.max((np.abs(xmin), np.abs(xmax))) * 0.1

    fig = plt.figure()
    ax = plt.gca()
    ax.axes.get_yaxis().set_ticks([])
    ax.axes.get_xaxis().set_ticks([])
    try:
        bad_access = y.shape[1]
        num_plots = y.shape[0]
        for ind in xrange(num_plots):
            yi = y[ind, :]
            ymin, ymax = np.min(yi), np.max(yi)
            marg = np.max((np.abs(ymin), np.abs(ymax))) * 0.1
            ax = fig.add_subplot(num_plots, 1, ind + 1)
            ax.plot(x, yi)
            ax.set_yticks(np.linspace(ymin, ymax, 4))
            ax.set_ylim(ymin - marg, ymax + marg)
    except IndexError:
        yi = y
        ymin, ymax = np.min(yi), np.max(yi)
        marg = np.max((np.abs(ymin), np.abs(ymax))) * 0.1
        ax.plot(x, y)
        ax.set_yticks(np.linspace(ymin, ymax, 4))
        ax.set_ylim(ymin - marg, ymax + marg)
        ax.set_xticks(x[0::4])
        foo = plt.xlim(xmin-marg, xmax+marg)
        print(foo)
        #ax.set_xlim(xmin=xmin, xmax=xmax)
    # ax.set_xticks(x[0::4])

    plt.show(block=False)
    return fig


def plot_triplet_stimuli(tax, stim, title=None, labels=[None, None]):
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

    if len(stim.shape) > 1:
        n_units = stim.shape[0]
        foo.axes.get_xaxis().set_ticks([])  # turn off those nasty ticks
        foo.axes.get_yaxis().set_ticks([])
    else:
        n_units = 1

    if labels[0]:
        plt.xlabel(labels[0])
    else:
        plt.xlabel('time (s)')

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