import numpy as np
import melopy.utility as music
from src.a_wilson_cowan.wc_unit import WCUnit
from src.stim.stim_maker import fq_tuning_curve
from src.stim.stimulus import ABAStimulus, ToneCurrent


class SensoryWCUnit(WCUnit):
    """ unit with frequency selectivity"""
    pars = dict(
        ke=.1, the=.2,  # IO params
        kS=.1, thS=.5,
        r0=0., a0=0., S0=0., stim0=0.,  # time varying values
        gee=.57,
        gStim=1.,
        gSFA=0.7,
        tau=10., tauNMDA=100., tauA=2000., G=.64, b_00=False,
        i_0 = -.2, timescale = 1000 # milliseconds
    )

    def __init__(self, name=None, best_frequency=440., spread=4., **kwargs):
        """
        all the same things as WCUnit, but also has a bf and selectivity
        Args:
            best_frequency (float): the frequency (in hz) that best excites the cell
            spread (float): inverse of selectivity, in terms of semitones to standard deviations
            **kwargs:
        """
        if not name:
            name = "S" + str(best_frequency) + "-" + str(spread)
        WCUnit.__init__(self, name=name, **kwargs)
        key = music.frequency_to_key(best_frequency)
        if music.key_to_frequency(key) != best_frequency:
            print("warning- cell's response has been shifted to nearest semitone")
        self.best_frequency = best_frequency
        self.spread = spread
        self.tuning_curve = self.fq_tuning_curve()

    #@staticmethod
    def fq_tuning_curve(self, **kwargs):
        """
            Function to produce the proper raw inputs for frequency-selective neuronal populations.
            We will have tones in terms of frequency, and spread in terms of semitones.
            Args:
                num_tones (int): how many tones should be represented at semitone intervals
                -center (int, float, str): if number, the fq; if str, the note name; melopy.utilities.note_to_frequency
                -spread (int, float): inverse of selectivity, in terms of semitones to standard deviations
                func (callable): we're using normpdf; we'll expect center and spread to be obvious
                bPlot (bool): whether or not to plot
            Returns:
                OrderedDict: {semitone: response}
        """
        return fq_tuning_curve(center=self.best_frequency, spread=self.spread, **kwargs)


    def add_stim_current(self, stimulus, weight, name="stim"):
        """
        going to take an ABAStimulus object and respond to its tones through a tuning curve
        Args:
            stimulus (src.stim.ABAStimulus): object with the tones and the tuning curve
            weight (float): strength of the current on the target (self)
            name (str): what to call it in self.currents[name]
        Result:
            self.currents.update({name: ToneCurrent (contains the ABAStimulus in .stimulus}
            so if you don't change the name, you can get to stim with self.currents["stim"].stimulus
        """
        tone_current = ToneCurrent(stimulus=stimulus, weight=weight, target=self, name=name)
        self.currents[name] = tone_current
