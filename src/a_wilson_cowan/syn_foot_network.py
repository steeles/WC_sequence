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
import matplotlib.pyplot as plt
import melopy.utility as music

from src.a_wilson_cowan.synaptic_network import SynapticNetwork, Selectivity
from src.stim.stim_maker import FrequencyToneAxis
from src.stim.stimulus import ABAStimulus
from src.stim.intervals import Intervals


class Footprint(FrequencyToneAxis):
    def __init__(self, num_tones=64, center=440, spread=3, func=norm.pdf, dst=1, **kwargs):
        FrequencyToneAxis.__init__(self, num_tones, center, spread, func, dst, **kwargs)

    def dog(self, x, spread1, spread2, b_positive=True, **kwargs):
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

    def gauss(self, x, **kwargs):
        return self.tuning_func(x)

stim1 = ABAStimulus()
stim2 = Intervals()

s_layer_tones = FrequencyToneAxis(num_tones=24)
s_layer_pars = dict(gStim=.15, gee=0., spread=1, gSFA=0.3, layer="s_layer")
s_layer_selectivities = []
for tone in s_layer_tones.tone_ax:
    s_layer_selectivities.append(Selectivity(
        best_frequency=music.key_to_frequency(tone), spread=s_layer_pars["spread"], gain=s_layer_pars["gStim"]
    ))
s_layer_pars.pop("spread")
s_layer_footprints = dict(
    s_layer=dict(type="dog", spread1=1, spread2=2, offset=0, gain=0.05),
    i_layer=dict(type="gauss", spread=5, offset=0, gain=0.)
)
s_layer_pars.update(footprint=s_layer_footprints)
i_layer_tones = FrequencyToneAxis(num_tones=24, dst=2)
i_layer_pars = dict(gStim=0, gee=.0, gSFA=0.1, spread=3, the=0.35, layer="i_layer")
i_layer_selectivities = []
for tone in i_layer_tones.tone_ax:
    i_layer_selectivities.append(Selectivity(
        best_frequency=music.key_to_frequency(tone), spread=i_layer_pars["spread"], gain=i_layer_pars["gStim"]
    ))
i_layer_pars.pop("spread")
i_layer_footprints = dict(
    s_layer=dict(type="gauss", spread=3, offset=0),
    i_layer=dict(type="dog", spread1=2, spread2=4, offset=0)
)
i_layer_pars.update(footprint=i_layer_footprints)
sel = s_layer_selectivities + i_layer_selectivities
pars = [s_layer_pars for x in xrange(len(s_layer_selectivities))] + \
[i_layer_pars for x in xrange(len(i_layer_selectivities))]


class SynFootNetwork(SynapticNetwork):

    def __init__(self, selectivities, stimulus, **kwargs):
        SynapticNetwork.__init__(self, selectivities=selectivities, stimulus=stimulus, **kwargs)
        # build the syn_weights matrix row by row for each unit
        n_units = len(self.units)
        layers = [u.layer for u in self.units]
        weights = np.zeros([n_units, n_units])
        for ind in xrange(n_units):
            unit = self.units[ind]
            foot_funcs = self.get_layer_foot_funcs(unit)
            out = np.zeros(n_units)
            for layer in foot_funcs:
                mask = [x == layer for x in layers]
                out[mask] = self.curve_to_weights(
                    foot_func=foot_funcs[layer], unit_array=[k for (k, v) in zip(self.units, mask) if v]
                )
            weights[ind, :] = out
        self.syn_weights = weights            # weights_row = [foot_funcs]

    @staticmethod
    def get_layer_foot_funcs(unit):
        out = {}
        for layer in unit.footprint:
            foot_pars = unit.footprint[layer]
            footprint = Footprint(center_tone=unit.best_tone + foot_pars.get("offset"), **foot_pars)
            func = getattr(footprint, foot_pars["type"])
            out[layer] = lambda x: func(x, **foot_pars)
        return out

    @staticmethod
    def curve_to_weights(foot_func, unit_array):
        """
        Args:
            foot_func (function): mappings from BFs to weights
            unit_array (List[SensoryUnits]: list of units who have selectivities; their BF will be used to map weights
        Returns:
            List[float]: the weights to apply to those neurons' synapses
        """
        bfs = [u.best_frequency for u in unit_array]
        return foot_func(bfs)


if __name__ == "__main__":
    sfn = SynFootNetwork(selectivities=sel, stimulus=stim1, pars_list=pars)
    sfn.run()
    plt.imshow(sfn.R_var_array)




