import numpy as np
import melopy.utility as music

from src.stim.stimulus import ABAStimulus
from src.a_wilson_cowan.sensory_network import SensoryWCUnit, TonotopicNetwork, Selectivity
from src.simulation.simulation import Simulation


stim = ABAStimulus()
s_units = [
    Selectivity(music.key_to_frequency(49), 1, 0.8),
    Selectivity(music.key_to_frequency(52), 1, 0.8),
    Selectivity(music.key_to_frequency(52), 1, 0.)
]

weights = np.array([
    [0, 0, 0], [1, 0, 0], [-2, 1, 0]
])


class SynapticNetwork(TonotopicNetwork, Simulation):
    """ i want to vectorize some of the calculations so we'll be taking away some of the mechanics from
    WCUnit... which is buried in there somewhere.
    We'll create arrays for all the vars in the unit, compute all the
    currents at once...
    all the vars will get recorded together, but at the end of the sim we'll unzip them row by row and stitch them
    together by unit =^.^=
    """
    def __init__(self, syn_weights=weights, selectivities=s_units, stimulus=stim, **kwargs):
        TonotopicNetwork.__init__(self,  selectivities, stimulus, **kwargs)
        Simulation.__init__(self, **kwargs) # is this black magic?
        """ this guy would take a bunch of selectivities and make some units """
        self.syn_weights = syn_weights

        # now we build us some arrays - we're going to vectorize
        self.R_array = np.zeros([len(self.units), self.ttot])
        self.A_array = np.zeros([len(self.units), self.ttot])
        self.S_array = np.zeros([len(self.units), self.ttot])

        # pull out the vars from the vars arrays
        self.vars = [x.split("_")[0] for x in self.__dict__ if x.endswith("_array")]

        self.stim_currents = self.build_stimulus_currents()
        # list of units
        units_array = self.units
        self.gstims = np.array([
            x.currents["stim"].weight for x in units_array
        ])

        self.gees = np.array([x.gee for x in units_array])
        self.gSFAs = np.array([x.gSFA for x in units_array])
        self.Gs = np.array([x.G for x in units_array])
        self.taus = np.array([x.tau for x in units_array])
        self.tauAs = np.array([x.tauA for x in units_array])
        self.tauNMDAs = np.array([x.tauNMDA for x in units_array])

        # activation function parameters
        kes = np.array([x.ke for x in units_array])
        thes = np.array([x.the for x in units_array])
        self.f_e = self.f_activation_builder(kes, thes)
        kSs = np.array([x.kS for x in units_array])
        thSs = np.array([x.thS for x in units_array])
        self.f_S = self.f_activation_builder(kSs, thSs)

    def run(self):
        while self.t_i < self.ttot:
            self.update_all()

    def update_all(self, n=1):
        """ we want to calculate all the deltas first then we can add them """
        for ind in xrange(n):
            deltas = {}
            for var in self.vars:
                method = getattr(self, "get_d" + var)
                deltas[var] = method()
            # now apply the deltas
            for var in self.vars:
                array = getattr(self, var + "_array")
                array[:, self.t_i + 1] = array[:, self.t_i] + deltas[var]
            self.step()

    def get_dA(self):
        dA = self.delta_A(self.A_array[:, self.t_i], self.R_array[:, self.t_i], self.tauAs, self.dt * 1000)
        return dA

    @staticmethod
    def delta_A(A, R, tauA, dt):
        return dt/tauA * (-A + R)

    def get_dR(self):
        Iapp = self.SFA() + self.Isyn() + self.rec_exc() + self.gstims * self.stim_currents[:, self.t_i]
        dR = self.delta_R(self.R_array[:,self.t_i], Iapp, self.taus, self.f_e, self.dt * 1000)
        return dR

    @staticmethod
    def delta_R(R, Iapp, tau, fe, dt, gee=0):
        """ defaults to letting you put rec exc in there manually but you can also get dr(r)"""
        dr = dt / tau * (-R + fe(Iapp + gee * R))
        return dr

    def get_dS(self):
        #     VV decay
        dS = self.delta_S(
            self.S_array[:, self.t_i], self.tauNMDAs, self.f_S,
            self.Gs, self.R_array[:, self.t_i], self.dt * 1000)
        return dS

    @staticmethod
    def delta_S(S, tauNMDA, fS, G, R, dt):
        #     vv decay
        dS = (-S / tauNMDA + (1 - S) * G * fS(R)) * dt
        return dS

    def SFA(self):
        return abs(self.gSFAs)*-1 * self.A_array[:, self.t_i]

    def rec_exc(self):
        return self.gees * self.R_array[:, self.t_i]

    def Isyn(self):
        return np.dot(self.syn_weights, self.R_array[:, self.t_i])

    def build_stimulus_currents(self):
        """
        map out the effective current for the stimulus to each unit and return as a numpy array
        Returns:
            np.array: effective current from the stimulus to each unit, one unit each row
        """
        out = []
        for unit in self.units:
            tc = unit.tuning_curve
            out.append([tc[x] for x in self.stimulus.tones])
        return np.array(out)


if __name__ == "__main__":
    network = SynapticNetwork()
    network.update_all(1000)






