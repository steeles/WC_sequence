from collections import namedtuple
import numpy as np

import melopy.utility as music

from src.a_wilson_cowan.sensory_neuron import SensoryWCUnit
from src.stim.stimulus import ABAStimulus

Selectivity = namedtuple("Selectivity", ("best_frequency", "spread", "weight"))

# center, spread for each unit, starting at 440 Hz A and 3 semitones up from there
s_units = [
    (music.key_to_frequency(49), 1, 0.8),
    (music.key_to_frequency(52), 1, 0.8)
]


class TonotopicNetwork():
    """ basic tonotopic network; initializes a sensory layer and connects it to a stimulus """

    def __init__(self, selectivities, stimulus, **kwargs):
        """
        initialize the network
        Args:
            selectivities (list of tuples): each tuple contains (best frequency (Hz), spread (semitones))
            stimulus (src.stim.stimulus.ABAStimulus): ABAStimulus
        """
        # create the units, name them, hook up stim and pack them into a dict
        self.units = dict()
        for s in selectivities:
            name = "S" + str(selectivities[0]) + "_" + str(selectivities[1])
            unit = SensoryWCUnit(best_frequency=s[0], spread=s[1], **kwargs)
            unit.add_stim_current(stimulus)
            self.units.update((name, unit))