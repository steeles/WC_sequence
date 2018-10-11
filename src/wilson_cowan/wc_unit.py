# TODO: import WC_class
import numpy as np
from src.stim.stim_maker import aba_triplet

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
    func = lambda x: 1/(1+np.exp(-(x-theta)/k)) - 1/(1+np.exp(theta/k))
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


class Simulation(object):

    def __init__(self, T=5, dt=.001, **kwargs):
        self.T = T
        self.dt = dt
        self.tax = np.arange(dt, T+dt, dt)
        self.ttot = len(self.tax)


class WCUnit(KWPars):
    pars = dict(
        ke=.1, the=.2,  # IO params
        kS=.1, thS=.5,
        r0=0., a0=0., S0=0., stim0=1.,  # time varying values
        gee=.57, name="u1",
        gStim=1.,
        gSFA=0,
        tau=10., tauNMDA=100., tauA=200., G=.64)

    def __init__(self, **kwargs):
        """ set up the vars, make sure there's a name """
        KWPars.__init__(self, **kwargs)
        self.r = [self.r0]
        self.a = [self.a0]
        self.S = [self.S0]
        self.stim = [self.stim0]
        self.name = self.name
        self.currents = dict()

#     def __init__(self, **kwargs):
#         KWPars.__init__(self, **kwargs)
#         self.f_activation = f_activation_builder(self.k, self.theta)


class Current(object):
    # generic class for a current
    def __init__(self, source, weight, target, name=None):
        """
        create a new current, it will go into target's connections
        and take from's variable value[0]
        Args:
            source (list): variable from which current comes; will be either length 0 as from
                a mutable attribute, or an nd.array from a stimulus.
            weight (float): strength of current on target
            target (WCUnit): unit the current is added to; that unit will update its connections
                and add this current to the summed inputs to its firing rate function
            name (str): what to call it
        """
        self.source = source
        self.weight = weight
        self.target = target
        if not name:
            name = target.name + str(weight)
        self.name = name


class StimCurrent(Current):

    def __init__(self, **kwargs):
        Current.__init__(self, **kwargs)
        self.stim = stim

    def update_current(self, t):




if __name__ == "__main__":
    STIM = aba_triplet()

    u1 = WCUnit(name="u1")
    u1.addStimCurrent(STIM)
