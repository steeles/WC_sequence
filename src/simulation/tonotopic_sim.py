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
from src.simulation.traces import Trace, CurrentTrace
from src.sim_plots.sns_plots import plot_generic_traces


pd.options.mode.chained_assignment = None


class TonotopicTripletsSimulation(Simulation):
    """
    THIS TIME WE PACK IT IN WITH THE UNITS
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

        # just slap a trace on there?
        for unit in self.network.units:
            # we'll just staple the traces to the unit, maybe this is wrong but it should make things easier
            unit.trace_dict = OrderedDict()

            trace_sources = OrderedDict(
                FR=unit.r)  # , stim=unit.stim, SFA=unit.a
            # )
            for k, v in trace_sources.items():
                self.add_new_trace(unit, source=v, trace_name=k)

            current_trace_sources = unit.currents
            for k, v in current_trace_sources.items():
                self.add_new_current_trace(unit, source=v, trace_name=k)
            # self.traces[unit.name] = OrderedDict()

    def add_new_trace(self, unit, source, trace_name=None):
        # TODO: it would be simpler if trace read a current; would need analogy for FR
        if not trace_name:
            trace_name = source
        # Trace needs a target to update into
        trc = Trace(sim=self, source=source, target=unit.trace_dict, trace_name=trace_name)

    def add_new_current_trace(self, unit, source, trace_name):
        """
        record a current in a simulation
        Args:
            unit (WCUnit:
            source (Current):
            trace_name (str):
        """
        if not trace_name:
            trace_name = unit.name + source.name
        trc = CurrentTrace(sim=self, source=source, target=unit.trace_dict, trace_name=trace_name)

    def update_all_traces(self):
        for u in self.network.units:
            for t in u.trace_dict.values():
                t.update_trace()

        # print(self.traces) TODO: NOOOOOO
        # for u in self.traces.values():
        #     #print u
        #     for t in u.values():
        #         t.update_trace()

    def run(self):
        while self.t_i < self.ttot:
            # drive the stimulus forward
            # u1.currents["stim"].set_time(self.t_i)
            self.network.stimulus.set_time(self.t_i)
            self.network.update_all()
            self.update_all_traces()
            self.t_i += 1

    def unit_traces_to_dict_arrays(self, unit):
        """ THIS IS SO MUCH CLEANER """
        traces = [(k, v.trace) for k, v in unit.trace_dict.items()]
        return dict(traces)

    def unit_df(self, unit):
        return pd.DataFrame(self.unit_traces_to_dict_arrays(unit), index=sim.tax)

    def traces_to_df(self):
        ulst = []
        for k in self.network.units:
            ndf = self.unit_df(k)  # units.items()[0][1], index=sim.tax)
            ndf["unit"] = k.name  # units.items()[0][0]
            ndf["tax"] = sim.tax
            ulst.append(ndf)

        df_out = pd.concat(ulst)
        return df_out


if __name__ == '__main__':
    tic = datetime.datetime.now()

    stim = ABAStimulus()
    Selectivity = namedtuple("Selectivity", ("best_frequency", "spread", "gain"))

    # center, spread for each unit, starting at 440 Hz A and 3 semitones up from there
    s_units = [
        Selectivity(music.key_to_frequency(49), 1, 0.6),
        Selectivity(music.key_to_frequency(52), 1, 0.6)
    ]

    stim = ABAStimulus(a_semitone=49, df=3)
    network = TonotopicNetwork(s_units, stim)
    sim = TonotopicTripletsSimulation(network=network)
    sim.run()
    data = sim.traces_to_df()
    g = sns.FacetGrid(data, col='unit', col_wrap=1)
    g.map_dataframe(plot_generic_traces)
    # f1 = generic_plot(sim.tax, np.array(sim.traces.values()))
    toc = datetime.datetime.now()
    print (toc - tic).microseconds / 10e6

    plt.show()


    # g = sns.FacetGrid(df, col='trace', col_wrap=1)
    # g.map(plot_sensory_traces, 'tax', 'values')
    #

    # df.head()

