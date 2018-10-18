""" module for currents for WC units """


# import numpy as np

class Current(object):
    """ generic class for a current """

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
            stimulus (numpy.array): the stimulus
            weight (float): strength of current on target
            target (WCUnit): unit the current is added to; that unit will update its connections
                and add this current to the summed inputs to its firing rate function
            name (str): what to call it in target.current[name]
        """
        Current.__init__(self, weight=weight, target=target, name=name, source=None)
        self.stimulus = stimulus
        self.value = stimulus[0] * weight
        self.t = 0

    def set_time(self, t):
        """
        feed in a time
        Args:
            t:
        """
        self.t = t

    def update(self):
        """ stimulus is the only one that updates a variable directly """
        stim = self.stimulus[self.t]
        self.value = stim * self.weight
        self.target.stim[0] = self.stimulus  # WE CAN PROBABLY GET RID OF THIS


class SFACurrent(Current):
    """ current from SFA ; onto itself """
    def __init__(self, source, weight, target, tau_A=200, name=None):
        """
        create a new current, it will go into target's connections
        and take from's variable value[0]
        Args:
            source (list): should connect to a unit's firing rate, u.r; length = 1, access like source[0] # = u.r[0]
            weight (float): strength of current on target
            target (WCUnit): here it will be the same unit whose firing rate is its source
            tau_A (float): adaptation time constant (in time steps)
            name (str): what to call it in target.current[name]
        """
        if not name: name = target.name + str(weight) + "_SFA"
        Current.__init__(self, source, weight, target, name)
        self.tau_A = tau_A

    def update(self):
        da = 1. / self.tau_A * (-self.target.a[0] + self.source[0])
        self.target.a[0] += da
        self.value = self.weight * self.target.a[0]
