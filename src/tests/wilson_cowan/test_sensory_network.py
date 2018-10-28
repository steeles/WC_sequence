from collections import namedtuple, OrderedDict
import numpy as np
import melopy.utility as music


from src.stim.stimulus import ABAStimulus
from src.a_wilson_cowan.sensory_network import TonotopicNetwork

def test_selectivity():
    Selectivity = namedtuple("Selectivity", ("best_frequency", "spread", "gain"))

    # center, spread for each unit, starting at 440 Hz A and 3 semitones up from there
    s_units = [
        Selectivity(music.key_to_frequency(49), 1, 0.8),
        Selectivity(music.key_to_frequency(52), 1, 0.8)
    ]
    stim = ABAStimulus()
    network = TonotopicNetwork(s_units, stim)
    network.update_all(10)
    assert network.units.values()[0].r > network.units.values()[1].r


def test_add_selectivity():
    Selectivity = namedtuple("Selectivity", ("best_frequency", "spread", "gain"))
    # center, spread for each unit, starting at 440 Hz A and 3 semitones up from there
    s_units = [
        Selectivity(music.key_to_frequency(49), 1, 0.8),
        Selectivity(music.key_to_frequency(52), 1, 0.8)
    ]
    stim = ABAStimulus()
    network = TonotopicNetwork(s_units, stim)
    network.add_unit((music.key_to_frequency(50), 1, .8))
    network.update_all(10)
    assert network.units.values()[0].r > network.units.values()[1].r
    assert network.units.values()[2].r > network.units.values()[1].r
    assert network.units.values()[0].r > network.units.values()[2].r
