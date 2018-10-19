# TODO: import WC_class
import numpy as np

from src.a_wilson_cowan.currents import Current, StimCurrent, SFACurrent
from src.simulation.simulation import Simulation

# does creation of sensory unit update registry for WC overall?


def f_activation_builder(k, theta):
    """
     returns an activation function with specified k and theta
    Args:
        k: slope
        theta: threshold
    Returns:
        function
    """
    func = lambda x: 1 / (1 + np.exp(-(x - theta) / k)) - 1 / (1 + np.exp(theta / k))
    return func


class KWPars(object):
    """ superclass for objects with a pars dict. The entries in pars will be updated by kwargs, mapped to attributes"""

    pars = {"foo": "bar"}

    def __init__(self, **kwargs):
        """ basic pattern:
        object gets initialized with an attribute called "pars" containing a dict
        user can supply keywords that get added to the pars dict and mapped to attributes.
        Example:
            kw = KWPars(answer=42, question=None)
            kw.
        """
        self.pars.update(kwargs)
        for k, v in self.pars.items():
            self.__setattr__(k, v)


class WCUnit(KWPars):
    pars = dict(
        ke=.1, the=.2,  # IO params
        kS=.1, thS=.5,
        r0=0., a0=0., S0=0., stim0=0.,  # time varying values
        gee=.57,
        gStim=1.,
        gSFA=0,
        tau=10., tauNMDA=100., tauA=200., G=.64)

    def __init__(self, name="u1", tau=10., **kwargs):
        """
        set up the vars, make sure there's a name
        Args:
            name (str): what to call the unit for reference, dicts, plotting, etc
            tau: membrane timescale in time step units (dt)
            **kwargs:
        """
        KWPars.__init__(self, **kwargs)
        #Simulation.__init__(self, **kwargs)
        self.r = [self.r0]
        self.a = [self.a0] # I probably only need r... actually, maybe to record I need a container...
        self.S = [self.S0] # yeah set_trace needs a container.
        self.stim = [self.stim0]
        self.name = name
        self.tau = tau
        self.currents = dict()
        # add intrinsic currents
        if self.tauA and self.gSFA:
            self.add_SFA_current(weight=self.gSFA)
        self.f_r = f_activation_builder(self.ke, self.the)

    def add_stim_current(self, stimulus, weight, name="stim"):
        """
        add a new current for stimulus
        Args:
            stimulus (numpy.array): length ttot
            weight (float): strength of current on target
            name (str): to add to self.currents[name]
        """
        stim_current = StimCurrent(stimulus=stimulus, weight=weight, name=name, target=self)
        self.currents[name] = stim_current

    def add_SFA_current(self, weight, name="SFA"):
        """
        add a new current for spike frequency adaptation; unit adapts (slowly) in response to its own firing rate.
        Args:
            weight (float): strength of current on target
            tau_A (float): adaptation time constant (in time steps)
            name (str): what to call it in target.current[name]; default target.name + str(weight) + "_SFA"
        Result: self.currents.update{name: SFACurrent}
        """
        if weight > 0: weight = -weight
        sfa_current = SFACurrent(source=self.r, weight=weight, tau_A=self.tauA, target=self, name=name)
        self.currents[name] = sfa_current

    def update(self):
        cvals = [c.value * c.weight for c in self.currents.itervalues()]
        dr = 1/self.tau * (-self.r[0] + self.f_r(sum(cvals)))
        self.r[0] += dr

    def update_all(self, n=1):
        for ind in xrange(n):
            for current in self.currents.values():
                current.update()
            self.update()
