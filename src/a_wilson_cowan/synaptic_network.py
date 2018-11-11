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


stim = ABAStimulus()
s_units = [
    Selectivity(music.key_to_frequency(49), 1, 0.2),
    Selectivity(music.key_to_frequency(52), 1, 0.2),
    Selectivity(music.key_to_frequency(52), 1, 0.)
]

weights = np.array([
    [0, 0, 0], [1, 0, 0], [-2, 1, 0]
])


class SynapticNetwork(TonotopicNetwork, Simulation):
    """ i want to vectorize some of the calculations
    all the vars will get recorded together, but at the end of the sim we'll peel them row by row and stitch them
    together by unit =^.^=
    """
    def __init__(self, syn_weights=weights, selectivities=s_units, stimulus=stim, **kwargs):
        TonotopicNetwork.__init__(self,  selectivities, stimulus, **kwargs)
        Simulation.__init__(self, **kwargs) # is this black magic?
        """ this guy would take a bunch of selectivities and make some units """
        self.syn_weights = syn_weights

        # now we build us some arrays - we're going to vectorize
        self.R_var_array = np.zeros([len(self.units), self.ttot])
        self.A_var_array = np.zeros([len(self.units), self.ttot])
        self.S_var_array = np.zeros([len(self.units), self.ttot])

        # pull out the vars from the vars arrays
        self.vars = [x.split("_")[0] for x in self.__dict__ if x.endswith("_var_array")]

        self.stim_currents = self.build_stimulus_currents()
        # list of units
        units_array = self.units
        self.gstims = np.array([
            x.currents["stim"].weight for x in units_array
        ])
        self.i_0s = np.array([x.i_0 for x in units_array])
        self.gees = np.array([x.gee for x in units_array])
        self.gSFAs = np.array([x.gSFA for x in units_array])
        self.Gs = np.array([x.G for x in units_array])
        self.taus = np.array([x.tau for x in units_array])
        self.tauAs = np.array([x.tauA for x in units_array])
        self.tauNMDAs = np.array([x.tauNMDA for x in units_array])

        # activation function parameters
        self.kes = np.array([x.ke for x in units_array])
        self.thes = np.array([x.the for x in units_array])
        self.f_e = self.f_activation_builder(self.kes, self.thes)
        self.kSs = np.array([x.kS for x in units_array])
        self.thSs = np.array([x.thS for x in units_array])
        self.f_S = self.f_activation_builder(self.kSs, self.thSs, self.b_00)
        # initialize
        self.point_wise_Isyn = np.outer(self.syn_weights, self.R_var_array)

    def run(self):
        while self.t_i < self.ttot-1:
            self.update_all()
        self.point_wise_Isyn = np.outer(self.syn_weights, self.R_var_array)

    def update_all(self, n=1):
        """ we want to calculate all the deltas first then we can add them """
        for ind in xrange(n):
            deltas = {}
            for var in self.vars:
                method = getattr(self, "get_d" + var)
                deltas[var] = method()
            # now apply the deltas
            for var in self.vars:
                array = getattr(self, var + "_var_array")
                array[:, self.t_i + 1] = array[:, self.t_i] + deltas[var]
            self.step()

    def get_dA(self):
        dA = self.delta_A(self.A_var_array[:, self.t_i], self.R_var_array[:, self.t_i], self.tauAs, self.dt * 1000)
        return dA

    @staticmethod
    def delta_A(A, R, tauA, dt):
        return dt/tauA * (-A + R)

    def get_dR(self):
        Iapp = self.SFA() + self.Isyn() + self.i_0s + self.rec_exc() + \
            self.gstims * self.stim_currents[:, np.clip(self.t_i, 0, max(self.stim_currents.shape)-1)]
        dR = self.delta_R(self.R_var_array[:, self.t_i], Iapp, self.taus, self.f_e, self.dt * 1000)
        return dR

    @staticmethod
    def delta_R(R, Iapp, tau, fe, dt, gee=0):
        """ defaults to letting you put rec exc in there manually but you can also get dr(r)"""
        dr = dt / tau * (-R + fe(Iapp + gee * R))
        return dr

    def get_dS(self):
        dS = self.delta_S(
            self.S_var_array[:, self.t_i], self.tauNMDAs, self.f_S,
            self.Gs, self.R_var_array[:, self.t_i], self.dt * 1000)
        return dS

    @staticmethod
    def delta_S(S, tauNMDA, fS, G, R, dt):
        #     vv decay             vv activation
        dS = (-S / tauNMDA + (1 - S) * G * fS(R)) * dt
        return dS

    def SFA(self):
        return abs(self.gSFAs)*-1 * self.A_var_array[:, self.t_i]

    def rec_exc(self):
        return self.gees * self.R_var_array[:, self.t_i]

    def Isyn(self):
        return np.dot(self.syn_weights, self.R_var_array[:, self.t_i])

    def build_stimulus_currents(self):
        """
        map out the effective current for the stimulus to each unit and return as a numpy array
        Returns:
            np.array: effective current from the stimulus to each unit, one unit each row
        """
        out = []
        for unit in self.units:
            arr = np.zeros(self.ttot)
            tc = unit.tuning_curve
            tones = [tc[x] for x in self.stimulus.tones]
            arr[:len(tones)] = tones
            out.append(arr)
        return np.array(out)

    def unit_traces_to_dict_arrays(self, unit_ind):
        n_units = len(self.units)
        unit_dict = OrderedDict()
        unit_dict["tax"] = self.tax
        for var in self.vars:
            # pull out the traces of all the vars
            unit_dict[var] = getattr(self, "{}_var_array".format(var))[unit_ind]
        unit_dict["FR"] = unit_dict["R"]
        unit_dict["stim"] = self.stim_currents[unit_ind] * self.gstims[unit_ind]
        unit_dict["SFA"] = self.A_var_array[unit_ind] * abs(self.gSFAs[unit_ind]) * -1
        unit_dict["rec_exc"] = self.R_var_array[unit_ind] * self.gees[unit_ind]
        syn_ind = n_units * unit_ind
        syn_currents = self.point_wise_Isyn[syn_ind:syn_ind + n_units, :]
        for s_ind in xrange(syn_currents.shape[0]):
            syn = syn_currents[unit_ind, :]
            if any(syn):
                unit_dict["Isyn_u{}".format(s_ind)] = syn
        return unit_dict

    def build_unit_dfs(self):
        n_units = len(self.units)
        unit_dfs = []
        for ind in xrange(n_units):
            unit_dict = self.unit_traces_to_dict_arrays(ind)
            ndf = pd.DataFrame(unit_dict, index=self.tax)
            ndf["unit"] = "u{}".format(ind)
            unit_dfs.append(ndf)
        # TODO: make sure this doesn't clobber columns when u0, 1, etc get involved... i think it shouldn't...
        return pd.concat(unit_dfs)

    def get_dR_R(self, unit_ind, Iapp=None, bPlot=True):
        """
        create a plot of the change in R with R under the current regime
        Args:
            unit_ind: which unit's pars to use
            Iapp:
            bPlot:
        Returns:
            pd.DataFrame: ["R', "dR"]
        """
        if Iapp is None:
            Iapp = self.i_0s[unit_ind]
        tau = self.taus[unit_ind]
        gee = self.gees[unit_ind]
        fe = self.f_activation_builder(self.kes[unit_ind], self.thes[unit_ind])
        r_arr = np.linspace(-.1, 1., 1000)
        dR_arr = self.delta_R(r_arr, Iapp=Iapp, tau=tau, fe=fe, dt=self.dt*1000, gee=gee)
        out = pd.DataFrame({"R_ax": r_arr, "dR": dR_arr})
        if bPlot: generic_plot(out["R_ax"], out["dR"])
        return out


if __name__ == "__main__":
    network = SynapticNetwork()
    network.run()
    data = network.build_unit_dfs()
    g = sns.FacetGrid(data, col='unit', col_wrap=1)
    g.map_dataframe(plot_more_generic_traces)
    plt.show()
    dRR = network.get_dR_R(0, 0, bPlot=False)
    dRR["zline"]=0
    dRR.plot(x="R_ax")








