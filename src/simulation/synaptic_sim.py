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
# from src.sim_plots.sns_plots import plot_more_generic_traces
from src.stim.stimulus import ABAStimulus
from src.a_wilson_cowan.sensory_network import SensoryWCUnit, TonotopicNetwork, Selectivity
from src.simulation.simulation import Simulation
from src.a_wilson_cowan.synaptic_network import SynapticNetwork
from src.stim.intervals import Intervals

plt.close()

sensory_pars = dict(i_0 = -.02, gee = 0.45, gSFA = 0.5)
integration_pars = dict(i_0 = -0.05, tau=50, gee=0.3, SFA = 0.1, the = 0.4)


pars_list = [
    sensory_pars,
sensory_pars, integration_pars
]
T = 1.

# from micheyl
stim = Intervals(T=T, ITI=125, tone_length=125)
stim.set_ba_ab()
s_units = [
    Selectivity(music.key_to_frequency(49), 1, 0.15),
    Selectivity(music.key_to_frequency(46), 1, 0.15),
    Selectivity(music.key_to_frequency(46), 1, 0.)
]

weights = np.array([
    [0, 0, 0], [0, 0, 0], [.25, .15, 0]
])

network = SynapticNetwork(pars_list=pars_list, selectivities=s_units, stimulus=stim, syn_weights=weights, T=T, b_00=True)
network.run()
data = network.build_unit_dfs()

to_plot = ["FR", "SFA", 'Isyn_u0', 'Isyn_u1', 'rec_exc', 'stim', 'S']

plot_df = data[to_plot + ['tax', 'unit']].melt(
    id_vars=['tax', 'unit'], var_name = 'name', value_name='response'
)

g = sns.FacetGrid(data=plot_df, hue='name', col='unit', col_wrap=1)
g.map_dataframe(plt.plot, "tax", "response")
g.add_legend()
plt.show()
dRR = network.get_dR_R(0, bPlot=False)
dRR["zline"]=0
dRR.plot(x="R_ax")

