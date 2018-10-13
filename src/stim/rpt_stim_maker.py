import numpy as np

from src.stim.stim_maker import fq_tuning_curve, aba_triplet
from src.simulation.simulation import TimeAxis

class ABAStimulus(TimeAxis):
    """ master stimulus class; subclass of TimeAxis, with time granularity functions """
    def __init__(self, df=3, iti=.05, a_semitone=49, b_semitone=None, tone_length=0.03, T=5, dt=.001, **kwargs):
        """
        create a new ABAStimulus object
        Args:
            df Optional(int): difference in frequency for ABA triplet. Preferred.
            iti (float): inter-tone-interval
            a_semitone (int): default 49 <as in key of a piano>, A 440; you can get frequency in Hz with
                music.key_to_frequency(a_semitone)
            b_semitone Optional(int):
            tone_length (float):
            T (float): total time in seconds
            dt (float): timescale of simulation in seconds (also integration time step)
            **kwargs:
        """
        TimeAxis.__init__(self, T, dt, **kwargs)
        self.df = df
        self.iti = iti
        self.a_semitone = a_semitone
        self.b_semitone = b_semitone
        self.tone_length = tone_length
        self.stim_length = len(self.tax)
        # we also have ttot, tax

    def generate_triplet_tones(self):
        """ returns 1d numpy.array with the tones """
        trt = int(self.iti / self.dt)
        period = 4 * trt
        tone_time = int(self.tone_length / self.dt)

        triplet = np.zeros(period)
        triplet[:tone_time] = self.a_semitone
        triplet[trt:trt + tone_time] = self.b_semitone
        triplet[2 * trt:2 * trt + tone_time] = self.a_semitone
        return triplet

    def repeating_tones(self):
        stim_length = self.ttot
        triplet = self.generate_triplet_tones()
        period=len(triplet)
        stim = np.zeros(stim_length)
        n_cycles = int(np.ceil(stim_length/period))
        tmp = np.tile(triplet, [1, n_cycles])
        stim[:, :tmp.shape[1]] = tmp

    def tuning_curve(self, **kwargs):
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



# def rpt_stim_maker(e):
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
