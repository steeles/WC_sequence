import numpy as np

from src.a_wilson_cowan.sensory_neuron import SensoryWCUnit


class ABAStimulus:
    tones = np.ones(10) * 49
    t_i = 0
    ttot = 10
    value = tones[0]

    def update(self):
        # print(self.t_i)
        self.value = self.tones[self.t_i]
        self.t_i += 1


def test_init():
    su = SensoryWCUnit()
    pass


def test_tuning_curve():
    pass


def test_add_stim_current():
    u1 = SensoryWCUnit(name="u1")
    stim = ABAStimulus()
    u1.add_stim_current(stim, weight=0.5)
    u1.update_all(10)
    u2 = SensoryWCUnit(name="u1", best_frequency=880)
    stim.t_i = 0
    u2.add_stim_current(stim, weight=0.5)
    u2.update_all(10)
    assert u2.r[0] < u1.r[0]


def test_selectivity():
    pass

