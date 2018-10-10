import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
# import seaborn as sns

# from pylab import *
# from numpy import *
# from matplotlib.mlab import *
from numbers import Number
from collections import OrderedDict
import melopy.utility as music


def fq_tuning_curve(num_tones=25, center=440, spread=3, func=norm.pdf):
    """
    Function to produce the proper raw inputs for frequency-selective neuronal populations.
    We will have tones in terms of frequency, and spread in terms of semitones.
    Args:
        num_tones (int): how many tones should be represented at semitone intervals
        center (int, float, str): if number, the fq; if str, the note name; melopy.utilities.note_to_frequency
        spread (int, float): inverse of selectivity, in terms of semitones to standard deviations
        func (callable): we're using normpdf; we'll expect center and spread to be obvious
    Returns:

    """
    # we'll start from the center
    if isinstance(center, str):
        center_freq = music.note_to_frequency(center)

    else:
        center_freq = center

    # melopy uses keys for semitones! easy
    num_steps_below = np.ceil(num_tones / 2)

    semitone = music.frequency_to_key(center_freq) - num_steps_below
    center_key = music.frequency_to_key(center_freq)
    tuning_curve = OrderedDict()

    while len(tuning_curve) < num_tones:
        tuning_curve.update(
            {semitone: func(semitone, loc=center_key, scale=spread)}  # , #music.key_to_frequency(semitone)}
        )
        semitone += 1

    max_val = np.max(tuning_curve.values())
    tuning_curve.update((x, y / max_val) for x, y in tuning_curve.items())
    return tuning_curve

    # fq_axis = 440 * (2. ** (1 / 12.)) ** arange(-12, 13)
    # tuning_curve = normpdf(linspace(-7, 7, len(fq_axis)), 0, 3)
    # tuning_curve /= max(tuning_curve)  # rescale to equal 1

    # create fq_axis - ordered dict, ['A']:440, fqs is fq_axis.values

    # get lower and upper bounds
# iti=.05
# a_semitone=49
# b_semitone=None
# tone_length=0.30
# dt=.001

def aba_triplet(tuning_curve, df, iti=.05, a_semitone=49, b_semitone=None, tone_length=0.030, dt=.001):
    """
    basic function to create an ABA stimulus with a particular time granularity.
    Option to either identify an A tone and a df interval in semitones, or specify two absolute tones.
    Tone units are in melopy 'keys' ie keys of a piano; if key=1, note='A0' and frequency=27.5 (Hz)
    Args:
        tuning_curve (OrderedDict): create with fq_tuning_curve
        df (int): semitone difference between tones
        iti (float): inter-tone-interval in seconds
        a_semitone (int, float): default 49 <as in key of a piano>, A 440; you can get frequency in Hz with
                music.key_to_frequency(a_semitone)
        b_semitone (Optional[int, float]): if you want to specify manually
        tone_length (float): duration of an individual tone in seconds
        dt (float): timescale of simulation (in seconds)
    Returns:
        numpy.ndarray: the specified triplet scaled by the tuning curve [to be presented as a raw stimulus]
    """
    # map out the tone repetition rate to convert to simulation timesteps
    trt = int(iti / dt)
    period = 4 * trt
    tone_time = int(tone_length / dt)

    triplet = np.zeros((3, period))
    if df:
        b_semitone = a_semitone - df
    triplet[0, :tone_time] = tuning_curve[a_semitone]
    triplet[1, trt:trt + tone_time] = tuning_curve[b_semitone]
    triplet[2, 2*trt:2*trt + tone_time] = tuning_curve[a_semitone]

    all_vals = triplet.sum(0)
    out = np.zeros((3, period))
    for ind in xrange(out.shape[0]):
        out[ind, :] = all_vals

    # TODO: if bPlot
    return out

    # stim[0, :tone_length] = tuning_curve[A_ind]
    # stim[1, trt:trt + tone_length] = tuning_curve[B_ind]
    # stim[2, 2 * trt:2 * trt + tone_length] = tuning_curve[A_ind]

    # measure how long the tone , dt, scale


#
# def rpt_stim_maker(T=T, dt=dt, nUnits=nUnits, ITI=ITI, df=df, bPlot=False):
#     tone_length = .030
#     # exc_gain = 300
#     tax = arange(0, T, dt)  # s
#     stim_length = len(tax)
#     fq_axis = 440 * (2. ** (1 / 12.)) ** arange(-12, 13)
#     tuning_curve = normpdf(linspace(-7, 7, len(fq_axis)), 0, 3)
#     tuning_curve /= max(tuning_curve)  # rescale to equal 1
#     tone_length = int(tone_length / dt)
#     # df = 5
#     TRT = int(ITI / dt)
#     stim = zeros((nUnits, stim_length))
#
#     A_ind = 12;
#     B_ind = A_ind - df
#     # pdb.set_trace()
#     stim[0, :tone_length] = tuning_curve[A_ind]
#     stim[1, TRT:TRT + tone_length] = tuning_curve[B_ind]
#     stim[2, 2 * TRT:2 * TRT + tone_length] = tuning_curve[A_ind]
#
#     period = 4 * TRT
#     ncycles = int(ceil(stim_length / period))
#     triplet = stim[:, :period]
#     tmp = tile(triplet, [1, ncycles])
#     stim[:, :tmp.shape[1]] = tmp
#
#     if bPlot:
#         fig = figure() # pylab figure
#         foo = gca()
#         title('ITI = ' + str(ITI * 1000) + ' ms, df = ' + str(df))
#         foo.axes.get_xaxis().set_ticks([])  # turn off those nasty ticks
#         foo.axes.get_yaxis().set_ticks([])
#         xlabel('time')
#
#         for ind in xrange(nUnits):
#             ax = fig.add_subplot(nUnits, 1, ind + 1)
#             ylabel('u' + str(ind + 1))
#             ylim(-.2, 1)
#             #	ax.plot(tax,E[ind,:],'b');
#             #	ax.plot(tax,a[ind,:],'r');
#             ax.plot(tax, stim[ind, :], 'g')
#         #	ax.plot(tax,Isyn[ind,:],'c')
#         # title(str(ind+1))
#         # plot(tax,E,'b')
#         # plot(tax,I,'r')
#         # plot(tax,Inp_e,'g')
#         show(block=False)
#
#     # trip_activation = zeros(ITI*4)
#     # trip_activation[:tone_length] = tuning_curve[A_ind]
#     # trip_activation[ITI:ITI+tone_length] = tuning_curve[B_ind]
#     # trip_activation[2*ITI:2*ITI+tone_length] = tuning_curve[A_ind]
#
#     return stim

def habituator(tau_h, T, dt, bPlot=True):
    tax = arange(0, T, dt)  # s
    habituation = 1. - exp(-tax / tau_h)

    if bPlot:
        fig = figure()
        foo = gca()  # pylab , matplotlib.pyplot
        title(r'ITI attenuation $\tau$ = ' + str(tau_h))
        # foo.axes.get_xaxis().set_ticks([0,1,2])  # turn off those nasty ticks
        # foo.axes.get_yaxis().set_ticks([0,1])
        xlabel('time')

        # for ind in xrange(nUnits):
        ax = fig.add_subplot(1, 1, 1)
        ylabel('p2/p1')
        ylim(-.2, 1.1)
        #	ax.plot(tax,E[ind,:],'b');
        #	ax.plot(tax,a[ind,:],'r');
        ax.plot(tax, habituation, 'g')
        #	ax.plot(tax,Isyn[ind,:],'c')
        # title(str(ind+1))
        # plot(tax,E,'b')
        # plot(tax,I,'r')
        # plot(tax,Inp_e,'g')
        show(block=False)
