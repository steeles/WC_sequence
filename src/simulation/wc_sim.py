from src.a_wilson_cowan.wc_unit import WCUnit
from src.stim.stim_maker import aba_triplet
from src.sim_plots.make_figures import generic_plot

from simulation import Simulation


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
        Simulation.__init__(T=T, dt=dt, **kwargs)
        self.unit = wc_unit

        trace_sources = {
            "u1_r": wc_unit.r
            # "u1_a": wc_unit.a,
            # "u1_S": wc_unit.S
        }
        for k, v in trace_sources:
            self.add_new_trace(source=v, name=k)

    def run(self):
        while self.t_i < self.ttot:
            for current in self.unit.currents.values():
                current.update()
            # update response
            self.unit.update()
            # update traces
            for trace in self.traces:
                value = self.sources[trace]
                self.update_trace(trace, value)



if __name__ == '__main__':
    u1 = WCUnit(name="u1")
    triplet = aba_triplet()
    u1.add_stim_current(triplet)

    sim = WCTripletsSimulation(u1)
    sim.run()
    generic_plot(sim.tax, sim.traces)

