import numpy as np

from src.stim.stim_maker import fq_tuning_curve # , aba_triplet
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
        # can it use its own method to create an attribute on init?
        self.trt = int(self.iti / self.dt)
        self.period = 4 * self.trt
        self.tone_time = int(self.tone_length / self.dt)
        self.tones = self.repeating_tones()
        # we also have ttot, tax

    def generate_triplet_tones(self):
        """ returns 1d numpy.array with the tones in a single triplet """
        triplet = np.zeros(self.period)
        triplet[:self.tone_time] = self.a_semitone
        triplet[self.trt:self.trt + self.tone_time] = self.b_semitone
        triplet[2 * self.trt:2 * self.trt + self.tone_time] = self.a_semitone
        return triplet

    def repeating_tones(self):
        """
        create sequence of tones (unit: melopy.key, semitone) on a time grid of dt
        Returns:
            numpy.array: 1D array of tones
        """
        triplet = self.generate_triplet_tones()
        tones = np.zeros(self.ttot)
        n_cycles = int(np.ceil(self.ttot/self.period))
        tmp = np.tile(triplet, [1, n_cycles])
        tones[:, :tmp.shape[1]] = tmp
        return tones

    def map_tones_to_cell(self, unit):
        """

        Args:
            unit (SensoryWCUnit): has attr BF and spread
        Result:
            Use the sensory unit's tuning properties to find the input current through their tuning curve

        """
        pass

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
                OrderedDict: {semitone: response}
        """
        return fq_tuning_curve(**kwargs)
