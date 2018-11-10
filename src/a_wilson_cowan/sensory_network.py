from collections import namedtuple, OrderedDict
import copy
import numpy as np
import time
import melopy.utility as music

from src.a_wilson_cowan.sensory_neuron import SensoryWCUnit
from src.stim.stimulus import ABAStimulus

Selectivity = namedtuple("Selectivity", ("best_frequency", "spread", "gain"))

# center, spread for each unit, starting at 440 Hz A and 3 semitones up from there
s_units = [
    Selectivity(music.key_to_frequency(49), 1, 0.8),
    Selectivity(music.key_to_frequency(52), 1, 0.8)
]


class TonotopicNetwork(SensoryWCUnit):
    """ basic tonotopic network; initializes a sensory layer and connects it to a stimulus """
    def __init__(self, selectivities, stimulus, pars_list=None, **kwargs):
        """
        initialize the network
        Args:
            selectivities (list of tuples): each tuple contains (best frequency (Hz), spread (semitones))
            stimulus (src.stim.stimulus.ABAStimulus): ABAStimulus
            pars_list: optional list of pars to pass to unit in indexed form.
                Must be same length as selectivities. Use None for default pars for unit
        """
        SensoryWCUnit.__init__(self, **kwargs)
        self.stimulus = stimulus
        # create the units, name them, hook up stim and pack them into a dict
        self.units = []
        # if selectivities:
        ind = 0
        default_pars = copy.copy(SensoryWCUnit.pars)
        for s in selectivities:
            best_frequency, spread, gain = s
            name = 's({st},{sp},{g})'.format(
                st=int(music.frequency_to_key(best_frequency)),
                sp=spread, g=gain
            )
            if pars_list:
                pars = pars_list[ind]
            else:
                pars = None
            unit = SensoryWCUnit(best_frequency=best_frequency, spread=spread, name=name, **(pars or default_pars))
            unit.add_stim_current(stimulus, weight=gain)
            self.units.append(unit)
            ind += 1

    def update_all(self, n=1):
        for ind in xrange(n):
            for u in self.units:
                u.update_all()

    def add_unit(self, selectivity, **kwargs):
        """
        Add a unit to the network.
        Args:
            selectivity: tuple of (best_frequency, spread, gain)
                best_frequency (float): Hz, e. g., 440.0
                spread (float): by default, standard deviation of norm response curve in semitones away from BF
                gain (float): strength of the stimulus on the cell.
        """
        best_frequency, spread, gain = selectivity
        name = name = 's({st}:{sp}:{g})'.format(
                    st=int(music.frequency_to_key(best_frequency)),
                    sp=spread, g=gain
                )
        unit = SensoryWCUnit(
            best_frequency=best_frequency, spread=spread, name=name, **kwargs)
        unit.add_stim_current(self.stimulus, weight=gain)
        self.units.append(unit)


if __name__ == "__main__":
    tic = time.time()
    stim = ABAStimulus()
    network = TonotopicNetwork(s_units, stim)
    network.update_all(10)
    toc = time.time()
    print(toc-tic)
    print(network.units[0].r, network.units[1].r)
    print(stim.value)

