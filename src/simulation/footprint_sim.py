import matplotlib.pyplot as plt
import seaborn as sns
import melopy.utility as music

from src.stim.stimulus import ABAStimulus
from src.stim.intervals import Intervals
from src.stim.stim_maker import FrequencyToneAxis
from src.a_wilson_cowan.syn_foot_network import Footprint, SynFootNetwork, Selectivity

plt.close('all')

################ PARS
T = 2.

stim1 = ABAStimulus(T=T)
stim2 = Intervals()

s_layer_tones = FrequencyToneAxis(num_tones=24)
# since we're building recurrent excitation into the network we set the pars here to zero
s_layer_pars = dict(gStim=.5, gee=0., spread=1, gSFA=0.1, layer="s_layer")
s_layer_selectivities = []
for tone in s_layer_tones.tone_ax:
    s_layer_selectivities.append(Selectivity(
        best_frequency=music.key_to_frequency(tone), spread=s_layer_pars["spread"], gain=s_layer_pars["gStim"]
    ))
s_layer_pars.pop("spread")
s_layer_footprints = dict(
    s_layer=dict(type="dog", spread1=1, spread2=2, offset=0, gain=1),
    i_layer=dict(type="gauss", spread=5, offset=0, gain=0.)
)
s_layer_pars.update(footprint_pars=s_layer_footprints)

i_layer_tones = FrequencyToneAxis(num_tones=24, dst=2)
i_layer_pars = dict(gStim=0, gee=.0, gSFA=0.1, spread=3, the=0.35, layer="i_layer")
i_layer_selectivities = []
for tone in i_layer_tones.tone_ax:
    i_layer_selectivities.append(Selectivity(
        best_frequency=music.key_to_frequency(tone), spread=i_layer_pars["spread"], gain=i_layer_pars["gStim"]
    ))
i_layer_pars.pop("spread")
i_layer_footprints = dict(
    s_layer=dict(type="gauss", spread=3, offset=0, gain=.3),
    i_layer=dict(type="dog", spread1=2, spread2=4, offset=0, gain=.1)
)
i_layer_pars.update(footprint_pars=i_layer_footprints)
sel = s_layer_selectivities + i_layer_selectivities
pars = [s_layer_pars for x in xrange(len(s_layer_selectivities))] + \
       [i_layer_pars for x in xrange(len(i_layer_selectivities))]

################

sfn = SynFootNetwork(selectivities=sel, stimulus=stim1, pars_list=pars, T=T)

cm = plt.get_cmap('Purples')
with sns.axes_style("white"):
    plt.figure()
    ax = plt.imshow(sfn.syn_weights, cmap=cm,
                    vmin=-1, vmax=1)
    plt.colorbar()

sfn.run()

with sns.axes_style("white"):
    plt.figure()
    s_tones = [x.best_tone for x in sfn.units if x.layer == 's_layer']
    ax = plt.imshow(sfn.R_var_array[[x == "s_layer" for x in sfn.layers],:][::-1,:], aspect='auto', cmap=cm,
                    vmin=-1, vmax=1, extent=[0, sfn.ttot, s_tones[0], s_tones[-1]])
    plt.colorbar()

with sns.axes_style("white"):
    plt.figure()
    i_tones = [x.best_tone for x in sfn.units if x.layer == 'i_layer']
    ax = plt.imshow(sfn.R_var_array[[x == "i_layer" for x in sfn.layers],:][::-1,:], aspect='auto', cmap=cm,
                    vmin=-1, vmax=1, extent=[0, sfn.ttot, s_tones[0], s_tones[-1]])
    plt.colorbar()
