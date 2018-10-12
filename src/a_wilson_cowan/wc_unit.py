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
        r0=0., a0=0., S0=0., stim0=1.,  # time varying values
        gee=.57,
        gStim=1.,
        gSFA=0,
        tau=10., tauNMDA=100., tauA=200., G=.64)

    def __init__(self, name="u1", tau=10., **kwargs):
        """ set up the vars, make sure there's a name """
        KWPars.__init__(self, **kwargs)
        self.r = [self.r0]
        self.a = [self.a0]
        self.S = [self.S0]
        self.stim = [self.stim0]
        self.name = name
        self.tau = tau
        self.currents = dict()
        self.f_r = f_activation_builder(self.ke, self.the)

    def add_stim_current(self, weight, stimulus, name="stim"):
        """
        add a new current for stimulus
        Args:
            weight (float):
            stimulus (numpy.array):
            name (str): to add to self.currents[name
        """
        stim_current = StimCurrent(stimulus=stimulus, target=self, weight=weight, name=name)
        self.currents[name] = stim_current

    def update(self):
        pass


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
            name (str): what to call it in target.current[name]
        """
        self.source = source
        self.weight = weight
        self.target = target
        self.value = 0.

        if not name:
            name = target.name + str(weight)
        self.name = name


class StimCurrent(Current):
    """ stimulus is an array and has to know what time it is
    it's the only one without a variable source...
    """

    def __init__(self, stimulus, weight, target, name=None):
        """
        create a stimulus current
        Args:
            stimulus (numpy.array):
            weight (float): strength of current on target
            target (WCUnit): unit the current is added to; that unit will update its connections
                and add this current to the summed inputs to its firing rate function
            name (str): what to call it in target.current[name]
        """
        Current.__init__(self, weight=weight, target=target, name=name, source=None)
        self.stimulus = stimulus
        self.value = stimulus[0] * weight

    def update(self, t):
        """ stimulus is the only one that updates a variable directly """
        self.target.stim[0] = self.stimulus[t] * self.weight
        self.value = self.stimulus[t] * self.weight


if __name__ == "__main__":
    STIM = aba_triplet()
    u1 = WCUnit(name="u1")
    u1.addStimCurrent(STIM, weight=0.5)
