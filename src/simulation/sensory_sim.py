" Feed stim to a WC Unit "
import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from src.a_wilson_cowan.sensory_neuron import SensoryWCUnit
from src.stim.stimulus import ABAStimulus
from src.sim_plots.make_figures import generic_plot
from src.sim_plots.sns_plots import plot_sensory_traces
from src.stim.stimulus import ABAStimulus
from src.simulation.simulation import Simulation


class SensoryTripletsSimulation(Simulation):
    """ basic wc unit simulation """

    def __init__(self, sensory_unit=None, T=5, dt=.001, **kwargs):
        """
        Pass in a wc unit, set up recordings, get ready to run.
        Args:
            sensory_unit (SensoryWCUnit): it should already have everything you want connected to it
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
        self.unit = sensory_unit

        trace_sources = {
            "FR": sensory_unit.r,
            "stim": sensory_unit.stim,
            "SFA": sensory_unit.a,
            # "u1_S": wc_unit.S
        }
        for k, v in trace_sources.items():
            self.add_new_trace(source=v, trace_name=k)

    def run(self):
        while self.t_i < self.ttot:
            # drive the stimulus forward
            # u1.currents["stim"].set_time(self.t_i)
            self.unit.currents
            for current in self.unit.currents.values():
                current.update()
                # if self.t_i % 100 == 0:
                #     print(current.value, current.name)
            # update response
            self.unit.update()
            # update traces
            for trace in self.traces.values():
                trace.update_trace()
            self.t_i += 1

    @staticmethod
    def main():
        pass


if __name__ == '__main__':
    tic = datetime.datetime.now()
    u1 = SensoryWCUnit(name="u1", tauA=5000, gSFA=0.8)
    stim = ABAStimulus(a_semitone=44, df=9)
    u1.add_stim_current(stim, weight=0.5)
    sim = SensoryTripletsSimulation(sensory_unit=u1, T=5)

    sim.run()
    toc = datetime.datetime.now()
    # let's try it with seaborn and a dataframe
    trace_dict = {}
    trace_dict.update((k, v.trace) for k, v in sim.traces.items())
    trace_dict['tax'] = sim.tax
    data = pd.DataFrame(trace_dict, index=sim.tax) \
        [['tax', 'FR', 'SFA', 'stim']]

    plot_sensory_traces(data=data, unit=u1)

    # data1 = data.add(pd.Series(np.ones(len(sim.tax)), index=sim.tax))
    # data2 = data.add(pd.Series(np.ones(len(sim.tax)) * 2, index=sim.tax))
    # data2["u1_r"] = data2["u1_r"].apply(lambda x: x * 2)
    # data2["u1_a"] = data2["u1_a"].apply(lambda x: x * 2)



    # df = data[['tax', 'u1_r', 'u1_a']].melt(
    #     'tax', var_name='trace', value_name='values'
    # )
    # sns.lineplot(x='tax', y='values', hue='trace', data=df)
    # ax2 = plt.twinx()
    # ax2.set_ylim([-1, 0])
    # data_n = data[['tax', 'stim']]
    # data_n['stim'] = data_n['stim'].apply(lambda x: x * -.1)
    #
    # sns.lineplot(x='tax', y='stim', data=data_n, ax=ax2, color='grey')
    # # df = data.melt('tax', var_name='trace', value_name='values')

    # g = sns.FacetGrid(df, col='trace', col_wrap=1)
    # g.map(plot_sensory_traces, 'tax', 'values')


    print (toc - tic).microseconds / 10e6
    # f1 = generic_plot(sim.tax, np.concatenate(traces))
    # plt.show()
    # x = np.array(u1.tuning_curve.keys()[:-1])
    # y = np.array(u1.tuning_curve.values()[:-1])
    # f2 = generic_plot(x, y)
    # plt.show()

