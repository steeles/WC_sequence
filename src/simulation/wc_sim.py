" Feed stim to a WC Unit "

import matplotlib.pyplot as plt
import numpy as np
from src.a_wilson_cowan.wc_unit import WCUnit
from src.stim.stim_maker import aba_triplet
from src.sim_plots.make_figures import generic_plot
from src.stim.stimulus import ABAStimulus
from src.simulation.simulation import Simulation




class WCTripletsSimulation(Simulation):
    """ basic wc unit simulation """

    def __init__(self, wc_unit=None, T=5, dt=.001, **kwargs):
        """
        Pass in a wc unit, set up recordings, get ready to run.
        Args:
            wc_unit (WCUnit): it should already have everything you want connected to it
            T (float): T in seconds
            dt (float): integration timestep
            **kwargs:
        Derived attributes:
            self.tax (numpy.array): time axis
            self.ttot (int): total number of time steps
            self.t_i (int): the current time step
            self.traces (dict): traces
        """
        Simulation.__init__(self, T=T, dt=dt, **kwargs)
        self.unit = wc_unit

        trace_sources = {
            "u1_r": wc_unit.r,
            "stim": wc_unit.stim,
            "u1_a": wc_unit.a,
            # "u1_S": wc_unit.S
        }
        for k, v in trace_sources.items():
            self.add_new_trace(source=v, trace_name=k)

    def run(self):
        while self.t_i < self.ttot:
            # drive the stimulus forward
            u1.currents["stim"].set_time(self.t_i)
            for current in self.unit.currents.values():
                current.update()
            # update response
            self.unit.update()
            # update traces
            for trace in self.traces.keys():
                self.update_trace(trace)

            self.t_i += 1


if __name__ == '__main__':
    u1 = WCUnit(name="u1")
    # TODO: the stimulus should get made with the same dt as sim
    triplet = aba_triplet(iti=.08)
    u1.add_stim_current(stimulus=triplet,weight=0.8)
    u1.add_SFA_current(weight=5)

    sim = WCTripletsSimulation(wc_unit=u1, T=0.32)
    sim.run()
    generic_plot(sim.tax, np.array(sim.traces.values()))
    plt.show()
