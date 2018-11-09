import numpy as np
import melopy.utility as music

from src.stim.stimulus import ABAStimulus
from src.a_wilson_cowan.sensory_network import SensoryWCUnit, TonotopicNetwork, Selectivity

stim = ABAStimulus()
s_units = [
    Selectivity(music.key_to_frequency(49), 1, 0.8),
    Selectivity(music.key_to_frequency(52), 1, 0.8),
    Selectivity(music.key_to_frequency(52), 1, 0.)
]

weights = np.array([
    [0, 0, 0], [1, 0, 0], [-2, 1, 0]
])


class SynapticNetwork(TonotopicNetwork):
    """ i want to vectorize some of the calculations so we'll be taking away some of the mechanics from
    WCUnit... which is buried in there somewhere.
    We'll create arrays for all the vars in the unit, compute all the
    currents at once...
    all the vars will get recorded together, but at the end of the sim we'll unzip them row by row and stitch them
    together by unit =^.^=
    """
    def __init__(self, syn_weights=weights, selectivities=s_units, stimulus=stim, **kwargs):
        TonotopicNetwork.__init__(self,  selectivities, stimulus, **kwargs)
        """ this guy would take a bunch of selectivities and make some units """
        self.syn_weights = syn_weights

        # now we build us some arrays - we're going to vectorize
        self.r_array = np.zeros(len(self.units))
        self.a_array = np.zeros(len(self.units))
        self.S_array = np.zeros(len(self.units))
        self.stim_currents = self.build_stimulus_currents()
        # list of units
        units_array = self.units.values()
        self.gstims = np.array([
            x.currents["stim"].weight for x in units_array
        ])

        self.gees = np.array([x.gee for x in units_array])
        self.gSFAs = np.array([x.gSFA for x in units_array])
        self.taus = np.array([x.tau for x in units_array])
        self.tauAs = np.array([x.tauA for x in units_array])

        # activation function parameters
        self.kes = np.array([x.ke for x in units_array])
        self.thes = np.array([x.the for x in units_array])
        self.f_e = self.f_activation_builder(self.kes, self.thes)

    @staticmethod
    def delta_A(A, R, tauA):
        return 1/tauA * (-A + R)

    def update_A(self):
        self.a_array += self.delta_A(self.a_array, self.r_array, self.tauAs)

    def update_R(self, t):
        Iapp = self.SFA() + self.Isyn() + self.rec_exc() + self.gstims * self.stim_currents[:, t]
        # make sure we don't double count the gee
        dr = self.delta_R(self.r_array, Iapp, self.taus, self.f_e, gee=0)
        self.r_array += dr

    @staticmethod
    def delta_R(R, Iapp, tau, fe, gee=0):
        """ defaults to letting you put rec exc in there manually but you can also get dr(r)"""
        dr = 1 / tau * (-R + fe(Iapp + gee * R))
        return dr

    def SFA(self):
        return abs(self.gSFAs)*-1 * self.a_array

    def rec_exc(self):
        return self.gees * self.r_array

    def Isyn(self):
        return self.syn_weights * self.r_array

    def build_stimulus_currents(self):
        """
        map out the effective current for the stimulus to each unit and return as a numpy array
        Returns:
            np.array: effective current from the stimulus to each unit, one unit each row
        """
        out = []
        for unit in self.units.values():
            tc = unit.tuning_curve
            out.append([tc[x] for x in self.stimulus.tones])
        return np.array(out)








