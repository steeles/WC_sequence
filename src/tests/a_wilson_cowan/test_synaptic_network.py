import melopy.utility as music

from src.a_wilson_cowan.synaptic_network import SynapticNetwork
from src.a_wilson_cowan.sensory_network import Selectivity, TonotopicNetwork

# from src.sim_plots.make_figures import generic_plot
from src.stim.stimulus import ABAStimulus



def test_build_stimulus_currents():
    stim = ABAStimulus()

    # center, spread for each unit, starting at 440 Hz A and 3 semitones up from there
    s_units = [
        Selectivity(music.key_to_frequency(49), 1, 0.6),
        Selectivity(music.key_to_frequency(52), 1, 0.6)
    ]
    stim = ABAStimulus(a_semitone=49, df=3)
    network = SynapticNetwork(selectivities=s_units, stimulus=stim)
    out = network.build_stimulus_currents()
    assert out[0][0] > out[1][0]
    assert out[0][50] < out[1][50]

