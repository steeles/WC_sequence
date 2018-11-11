

import numpy as np
from src.stim.stimulus import ABAStimulus


class ABInterval(ABAStimulus):

    def __init__(self, **kwargs):
        print("AB")
        ABAStimulus.__init__(self, **kwargs)
        self.tones = self.repeating_tones(self.generate_ab_interval())

    def generate_ab_interval(self):
        """ returns 1d numpy.array with the tones in a single triplet """
        ab_interval = np.zeros(self.period)
        ab_interval[:self.tone_time] = self.a_semitone
        ab_interval[self.trt:self.trt + self.tone_time] = self.b_semitone
        ab_interval[2 * self.trt:2 * self.trt + self.tone_time] = 0.0 #self.a_semitone
        return ab_interval


class BAInterval(ABAStimulus):
    def __init__(self, **kwargs):
        print("BA")
        ABAStimulus.__init__(self, **kwargs)
        self.tones = self.repeating_tones(self.generate_ba_interval())

    def generate_ba_interval(self):
        """ returns 1d numpy.array with the tones in a single triplet """
        ba_interval = np.zeros(self.period)
        ba_interval[:self.tone_time] = self.b_semitone
        ba_interval[self.trt:self.trt + self.tone_time] = self.a_semitone
        ba_interval[2 * self.trt:2 * self.trt + self.tone_time] = 0.0 #self.a_semitone
        return ba_interval


class Intervals(ABInterval, BAInterval):
    # i guess this defaults to init for the first class declared

    def set_ab(self):
        self.tones = self.repeating_tones(self.generate_ab_interval())

    def set_ba(self):
        self.tones = self.repeating_tones(self.generate_ba_interval())

    def set_ba_ab(self):
        self.set_ba()
        ab = self.repeating_tones(self.generate_ab_interval())
        mid = self.ttot/2
        self.tones[mid:] = ab[:mid]

