import numpy as np
from scipy.stats import norm
import seaborn as sns

from collections import OrderedDict
import melopy.utility as music

from src.sim_plots.make_figures import generic_plot, plot_triplet_stimuli


def fq_tuning_curve(num_tones=25, center=440, spread=3, func=norm.pdf, bPlot=False):
    """
    Function to produce the proper raw inputs for frequency-selective neuronal populations.
    We will have tones in terms of frequency, and spread in terms of semitones.
    Args:
        num_tones (int): how many tones should be represented at semitone intervals
        center (int, float, str): if number, the fq; if str, the note name; melopy.utilities.note_to_frequency
        spread (int, float): inverse of selectivity, in terms of semitones to standard deviations
        func (callable): we're using normpdf; we'll expect center and spread to be obvious
        bPlot (bool): whether or not to plot
    Returns:
        OrderedDict: {semitone: response}

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
    tuning_curve.update({0: 0})
    if bPlot:
        fig = generic_plot(tuning_curve.keys(), tuning_curve.values())
        fig.show()
    return tuning_curve


TUNE = fq_tuning_curve()


#################
# i think this can all go... replace main in wc_sim with the stim class
def aba_triplet(tuning_curve=TUNE, df=3, iti=.05, a_semitone=49, b_semitone=None, tone_length=0.030, dt=.001):
    """
    basic function to create an ABA stimulus with a particular time granularity.
    Option to either identify an A tone and a df interval in semitones, or specify two absolute tones.
    Tone units are in melopy 'keys,' i.e., keys of a piano; if key=1, note='A0' and frequency=27.5 (Hz).
    Args:
        tuning_curve (OrderedDict): create with fq_tuning_curve
        df Optional(int): semitone difference between tones
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
    return all_vals


def habituator(tau_h, T, dt, bPlot=True):
    tax = np.arange(0, T, dt)  # s
    habituation = 1. - np.exp(-tax / tau_h)

    if bPlot:
        fig = generic_plot(tax, habituation)
        fig.show()