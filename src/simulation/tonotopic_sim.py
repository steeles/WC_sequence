" Feed stim to a WC Unit "
import datetime
from collections import OrderedDict
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from src.a_wilson_cowan.sensory_network import Selectivity, TonotopicNetwork

# from src.sim_plots.make_figures import generic_plot
from src.stim.stimulus import ABAStimulus
from src.simulation.simulation import Simulation
from src.sim_plots.sns_plots import plot_sensory_traces


class LeanSim(Simulation):
    """ don't copy current values to mutables... just access them directly to update trace """
    def update_trace(self, trace_name):
        """
                recorder- takes data coming in and marks it on the trace at time self.t_i
                Args:
                    trace_name (str): the name of the trace
                    value (float): the value to set at time self.t_i on the trace
                """
        value = self.sources[trace_name].value
        self.traces[trace_name][self.t_i] = value


class TonotopicTripletsSimulation(Simulation):
    """
    first network with fq selectivity;
    desired characteristics of sensory units given,
    """

    def __init__(self, network, T=5, dt=.001, **kwargs):
        """
        Pass in a wc unit, set up recordings, get ready to run.
        Args:
            sensory_units (SensoryWCUnit): it should already have everything you want connected to it
            T (float): T in seconds
            dt (float): integration timestep (seconds)
            **kwargs:
        Derived attributes:
            self.tax (numpy.array): time axis
            self.ttot (int): total number of time steps
            self.t_i (int): the current time step
            self.traces (dict): traces
        """
        Simulation.__init__(self, T=T, dt=dt, **kwargs)
        self.network = network
        self.traces = OrderedDict
        self.sources = OrderedDict

        for name, unit in self.network.units.items():
            trace_sources = {
                "u1_r": unit.r,
                "stim": unit.stim,
                "u1_a": unit.a,
                # "u1_S": wc_unit.S
            }
            self.traces[name]
        # or units.currents...

            for k, v in trace_sources.items():
                self.add_new_trace(source=v, trace_name=k)

    def add_new_trace(self, unit, source, trace_name=None):
        if not trace_name:
            trace_name = source
        blank_trace = np.zeros(self.ttot)
        self.traces[unit][trace_name] = blank_trace
        self.sources[unit][trace_name] = source


    def run(self):
        while self.t_i < self.ttot:
            # drive the stimulus forward
            # u1.currents["stim"].set_time(self.t_i)
            for current in self.unit.currents.values():
                current.update()
            # update response
            self.unit.update()
            # update traces
            for trace in self.traces.keys():
                self.update_trace(trace)
            self.t_i += 1


if __name__ == '__main__':
    tic = datetime.datetime.now()

    sim = TonotopicTripletsSimulation(sensory_unit=u1, T=5)

    sim.run()
    f1 = generic_plot(sim.tax, np.array(sim.traces.values()))
    toc = datetime.datetime.now()
    print (toc - tic).microseconds / 10e6
    #plt.show()
    g = sns.FacetGrid(df, col='trace', col_wrap=1)
    g.map(plot_sensory_traces, 'tax', 'values')
