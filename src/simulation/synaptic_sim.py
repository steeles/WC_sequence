"""
new network simulation! a few changes-
- the units in the network just provide pars; the network does the computations
- all variables are in arrays comprising all units
- correspondingly we don't need this complicated trace system anymore. we can record all traces at once.
- one thing- i may want to compute all the deltas in one step and apply them in a separate step, cuz R depends on A
and A depends on R- so i don't want the order to matter.
(ie update a before r, now r sees a[t+1
] not a[t]
"""

import numpy as np
import melopy.utility as music
from collections import OrderedDict
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from src.sim_plots.make_figures import generic_plot
from src.sim_plots.sns_plots import plot_more_generic_traces
from src.stim.stimulus import ABAStimulus
from src.a_wilson_cowan.sensory_network import SensoryWCUnit, TonotopicNetwork, Selectivity
from src.simulation.simulation import Simulation
from src.a_wilson_cowan.synaptic_network import SynapticNetwork

pars_list = [
    {"gee": 0.5, "i_0": -.2},
{"gee": 0.5, "i_0": -.2}, {"gee": 0.5, "i_0": -.2, "the": 0.3}
]

stim = ABAStimulus()
s_units = [
    Selectivity(music.key_to_frequency(49), 1, 0.2),
    Selectivity(music.key_to_frequency(52), 1, 0.2),
    Selectivity(music.key_to_frequency(52), 1, 0.)
]

weights = np.array([
    [0, 0, 0], [0, 0, 0], [-2, 1, 0]
])

network = SynapticNetwork(pars_list=pars_list, selectivities=s_units, syn_weights=weights)
network.run()
data = network.build_unit_dfs()
g = sns.FacetGrid(data, col='unit', col_wrap=1)
g.map_dataframe(plot_more_generic_traces)
plt.show()
dRR = network.get_dR_R(0, bPlot=False)
dRR["zline"]=0
dRR.plot(x="R_ax")

