import numpy as np
import melopy.utility as music
from src.a_wilson_cowan.wc_unit import WCUnit
from src.a_wilson_cowan.currents import StimCurrent
from src.stim.rpt_stim_maker import ABAStimulus


class SensoryWCUnit(WCUnit):
    """ unit with frequency selectivity"""
    def __init__(self, best_frequency=440., spread=4., **kwargs):
        """
        all the same things as WCUnit, but also has a bf and selectivity
        Args:
            best_frequency (float): the frequency (in hz) that best excites the cell
            spread (float): inverse of selectivity, in terms of semitones to standard deviations
            **kwargs:
        """
        WCUnit.__init__(self, **kwargs)
        key = music.frequency_to_key(best_frequency)
        if music.key_to_frequency(key) != best_frequency:
            print("warning- cell's response has been shifted to nearest semitone")
        self.best_frequency=best_frequency
        self.center = best_frequency
        self.spread = spread

    def add_stim_current(self, stimulus, weight, name="stim"):
        """
        going to take an ABAStimulus object and respond to its tones through a tuning curve
        Args:
            stimulus (src.stim.ABAStimulus): object with the tones and the tuning curve
            weight (float): strength of the current on the target (self)
            name (str): what to call it in self.currents[name]
        Result:
            self.currents.update({name: StimCurrent}
        """

        tc = stimulus.fq_tuning_curve(center=self.center, spread=self.spread)
        cell_inputs = np.array([tc[x] for x in stimulus.tones])
        stim_current = StimCurrent(stimulus=cell_inputs, weight=weight, name=name, target=self)
        self.currents[name] = stim_current
