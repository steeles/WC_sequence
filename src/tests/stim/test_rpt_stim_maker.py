from collections import OrderedDict
import numpy as np

from src.stim.stimulus import ABAStimulus
from src.a_wilson_cowan.sensory_neuron import SensoryWCUnit

# class SensoryWCUnit():
#     # TODO: can i map down to non-integer semitone vals for BF?
#     BF = 440
#     spread = 4
#     r = 0.5
#     currents = dict()
#
#     def add_stim_current(self, tones):


def test_triplets_timing():
    tc = OrderedDict(
        [
            (43.0, 0.1353352832366127), (44.0, 0.24935220877729614), (45.0, 0.41111229050718745),
            (46.0, 0.6065306597126333), (47.0, 0.8007374029168081), (48.0, 0.9459594689067655), (49.0, 1.0),
            (50.0, 0.9459594689067655), (51.0, 0.8007374029168081), (52.0, 0.6065306597126333),
            (53.0, 0.41111229050718745),
            (54.0, 0.24935220877729614)
        ]
    )
    #df, iti, tone_length, dt = 4, .04, .033, .001
    #actual = aba_triplet(tc, df, iti=iti, tone_length=tone_length, dt=dt)
    stim = ABAStimulus()
    actual = stim.generate_triplet_tones()
    # we wanna check the tone length... of all 3...
    tone_time = int(stim.tone_length/stim.dt)
    iti_time = int(stim.iti/stim.dt)
    gap_time = iti_time - tone_time

    # for u_ind in xrange(actual.shape[0]):
    for t_ind in xrange(3):
        start_ind = iti_time * t_ind
        # check the tone length
        assert list(actual[start_ind:]).index(0) == tone_time
        # check the gap length
        if t_ind is not 2:
            assert list(actual[start_ind + tone_time:] > 0).index(True) == gap_time
    # check the period
    assert len(actual) == iti_time * 4
    assert not any([np.isnan(x) for x in actual])


def test_tones_init():
    stim = ABAStimulus()
    # print(stim.__dict__)
    assert len(stim.tax) == len(stim.tones) == stim.ttot
    assert stim.tones[0] == 49
    assert stim.tax[-1] == stim.T # tax[0] is not 0...
    assert not any([np.isnan(x) for x in stim.tones])


def test_map_tones_to_cell():
    u1 = SensoryWCUnit()
    stimulus = ABAStimulus()
    u1.add_stim_current(stimulus, .5)
    # print(u1.currents)
    # assert False
    assert u1.stim[0] == 0
    u1.currents["stim"].update()
    assert u1.currents["stim"].value == 1

