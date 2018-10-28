" Feed stim to a WC Unit "
import datetime
from collections import OrderedDict, namedtuple
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import melopy.utility as music

from src.a_wilson_cowan.sensory_network import Selectivity, TonotopicNetwork

# from src.sim_plots.make_figures import generic_plot
from src.stim.stimulus import ABAStimulus
from src.simulation.simulation import Simulation, Trace
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
        self.traces = OrderedDict()

        for name, unit in self.network.units.items():
            trace_sources = OrderedDict(
                u_r=unit.r, stim=unit.stim, u_a=unit.a
            )
            self.traces[unit.name] = OrderedDict()

            for k, v in trace_sources.items():
                self.add_new_trace(unit, source=v, trace_name=k)

    def add_new_trace(self, unit, source, trace_name=None):
        if not trace_name:
            trace_name = source

        # Trace needs a target to update into
        # self.sources[unit.name][trace_name] = source
        trc = Trace(sim=self, source=source, target=self.traces[unit.name], trace_name=trace_name)

    def update_all_traces(self):
        #print(self.traces)
        for u in self.traces.values():
            #print u
            for t in u.values():
                t.update_trace()

    def run(self):
        while self.t_i < self.ttot:
            # drive the stimulus forward
            # u1.currents["stim"].set_time(self.t_i)
            self.network.update_all()
            self.update_all_traces()
            self.t_i += 1


if __name__ == '__main__':
    tic = datetime.datetime.now()

    stim = ABAStimulus()
    Selectivity = namedtuple("Selectivity", ("best_frequency", "spread", "gain"))

    # center, spread for each unit, starting at 440 Hz A and 3 semitones up from there
    s_units = [
        Selectivity(music.key_to_frequency(49), 1, 0.8),
        Selectivity(music.key_to_frequency(52), 1, 0.8)
    ]
    stim = ABAStimulus(a_semitone=44, df=9)
    network = TonotopicNetwork(s_units, stim)
    sim = TonotopicTripletsSimulation(network=network)
    sim.run()
    # f1 = generic_plot(sim.tax, np.array(sim.traces.values()))
    toc = datetime.datetime.now()
    print (toc - tic).microseconds / 10e6
    # #plt.show()
    # g = sns.FacetGrid(df, col='trace', col_wrap=1)
    # g.map(plot_sensory_traces, 'tax', 'values')
    #
    units = {}
    units.update(
        [(k, {tk: tv.trace for tk, tv in v.items()}) for k, v in sim.traces.items()]
    )
    df = pd.DataFrame(units.items()[0][1], index=sim.tax)
    df["unit"] = units.items()[0][0]
    df["tax"] = sim.tax
    df.head()
    for k, v in units.items()[1:]:
        ndf = pd.DataFrame(units.items()[0][1], index=sim.tax)
        ndf["unit"] = units.items()[0][0]
        ndf["tax"] = sim.tax
        # ndf.head()
        df.add(ndf)
        pass
    df.head()

