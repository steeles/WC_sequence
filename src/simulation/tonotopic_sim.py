" Feed stim to a WC Unit "
import datetime
import matplotlib.pyplot as plt
import numpy as np

from src.a_wilson_cowan.sensory_neuron import SensoryWCUnit
from src.stim.stimulus import ABAStimulus
from src.sim_plots.make_figures import generic_plot
from src.stim.stimulus import ABAStimulus
from src.simulation.simulation import Simulation


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

    def __init__(self, sensory_unit=None, T=5, dt=.001, **kwargs):
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
        self.unit = sensory_unit
        # or units.currents...
        trace_sources = {
            "u1_r": sensory_unit.r,
            "stim": sensory_unit.stim,
            "u1_a": sensory_unit.a,
            # "u1_S": wc_unit.S
        }
        for k, v in trace_sources.items():
            self.add_new_trace(source=v, trace_name=k)

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
    u1 = SensoryWCUnit(name="u1", tauA=5000)
    stim = ABAStimulus(a_semitone=44, df=9)
    u1.add_stim_current(stim, weight=0.5)
    u1.add_SFA_current(weight=.5)
    sim = TonotopicTripletsSimulation(sensory_unit=u1, T=5)

    sim.run()
    f1 = generic_plot(sim.tax, np.array(sim.traces.values()))
    toc = datetime.datetime.now()
    print (toc - tic).microseconds / 10e6
    #plt.show()
    x = np.array(u1.tuning_curve.keys()[:-1])
    y = np.array(u1.tuning_curve.values()[:-1])
    f2 = generic_plot(x, y)
    plt.show()

