import numpy as np

from src.a_wilson_cowan.wc_unit import KWPars

class Trace(KWPars):
    pars0 = {"variety": "variablw"}
    """ copy a variable into an array """
    def __init__(self, sim, source, target=None, trace_name=None, **kwargs):
        """
        recording for a variable in a simulation
        Args:
            sim (Simulation): t_i and ttot
            source (list len 0, soon: x.value):
            target (OrderedDict): where the trace gets stored
            trace_name (str): name to get stored
            **kwargs
        """
        # TODO: add type?
#        print(str(target) + " TARGET")

        self.sim = sim
        # dictionary update
        target.update([(trace_name, self)])

        if not target:
            target = self.sim.traces
        self.source = source
        self.trace = np.zeros(self.sim.ttot)
#        print(str(target))
        self.target = target

    def update_trace(self):
        self.trace[self.sim.t_i] = self.source[0]

#
# class CurrentTrace(Trace):
#
#     # i will wind up with a bunch of current traces and the regular response trace


class CurrentTrace(Trace):
    """ same as a trace, but instead of recording a raw variable it records weighted current-values
    #     is it voltage times conductance gives current? all the inputs are PSPs...
    #     """
    #
    pars0 = {"variety": "current"}
    """ copy a current into an array """
    def __init__(self, sim, source, target=None, trace_name=None, unit=None, **kwargs):
        """
        recording for a CURRENT in a simulation
        Args:
            sim (Simulation): has attributes t_i and ttot
            source (Current): has attributes .value and .weight
            target (OrderedDict): where the trace gets stored
            trace_name (str): name to get stored
            unit (WCUnit): the unit the current is attached to
            **kwargs
        """
        Trace.__init__(self, sim, source, target, trace_name, **kwargs)
        self.unit = unit

    def update_trace(self):
        self.trace[self.sim.t_i] = self.source.value * self.source.weight

