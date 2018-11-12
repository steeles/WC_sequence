""" use a neuron's .fq_tuning_curve() function, and its selectivity pars
(best_frequency, spread, gain), and certain rules to define connection footprints with other neurons by their
selectivities
ie option to take symmetric inputs from some neurons and asymmetric inputs from others.

indexing is going to be hard. each row of syn_weights describes input of all neurons on cell.
selectivities tells each neuron's tonotopy
we need a layer array to tell which layer a neuron is in and how it connects to neurons of other layers

to define a synaptic footprint according to """

import numpy as np
from scipy.stats import norm
import melopy.utility as music

from src.a_wilson_cowan.synaptic_network import SynapticNetwork, Selectivity
from src.stim.stim_maker import FrequencyToneAxis


class Footprint(FrequencyToneAxis):
    def __init__(self, num_tones=64, center=440, spread=3, func=norm.pdf, dst=1):
        FrequencyToneAxis.__init__(self, num_tones, center, spread, func, dst)

    def dog(self, x, spread1, spread2, b_positive=True):
        """
        difference of gaussians on the fq tone axis
        Args:
            x (scalar or array-like): what to compute dog for
            spread1: spread of initial; meant to be smaller gaussian
            spread2: spread of bg; meant to be larger gaussian
            b_positive: default True; output will be g1 - g2, not vice versa
        Returns:
            whatever x was with dog computed on it
        """
        g1 = self.func(x, self.fq_to_key(self.center), spread1)
        g2 = self.func(x, self.fq_to_key(self.center), spread2)
        if b_positive:
            out = g1 - g2
        else:
            out = g2 - g1
        return out


# stim
# layers
# pars
# selectivities

s_layer_tones = FrequencyToneAxis(num_tones=24)
s_layer_pars = dict(gStim = .15, gee = 0.05, spread = 1)
s_layer_selectivities = []
for tone in s_layer_tones.tone_ax:
    s_layer_selectivities.append(Selectivity(
        best_frequency=music.key_to_frequency(tone), spread=s_layer_pars["spread"], gain=s_layer_pars["gStim"]
    ))
s_layer_footprints = dict(
    s_layer=dict(type="dog", spread1=1, spread2=2, offset=0)
    i_layer=dict(type=)
)

class SynFootNetwork(SynapticNetwork):

    def __init__(self, selectivities, stimulus, **kwargs):
        SynapticNetwork.__init__(selectivities=selectivities, stimulus=stimulus)


    @staticmethod
    def curve_to_weights(tuning_func, unit_array):
        """
        Args:
            tuning_curve (function): mappings from BFs to weights
            unit_array (List[SensoryUnits]: list of units who have selectivities; their BF will be used to map weights
        Returns:
            List[float]: the weights to apply to those neurons' synapses
        """
        bfs = [u.best_frequency for u in unit_array]


    # def







