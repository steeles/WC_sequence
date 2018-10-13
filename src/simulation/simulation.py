

import numpy as np

class TimeAxis(object):
    def __init__(self, T=5, dt=.001, **kwargs):
        """
        Initialize the simulation. Creates the time axis at specified dt
        Args:
            T (float): T in seconds
            dt (float): integration timestep
            **kwargs:
        Derived attributes:
            self.tax (numpy.array): time axis
        """
        self.T = T
        self.dt = dt
        self.tax = np.arange(dt, T + dt, dt)


class Simulation(TimeAxis):
    """ master class to set up and record simulations """

    def __init__(self, T=5, dt=.001, **kwargs):
        """
        Initialize the simulation. Creates the time axis, calculates the number of
        time steps, and sets t_i to zero.
        Args:
            T (float): T in seconds
            dt (float): integration timestep
            **kwargs:
        Derived attributes:
            self.tax (numpy.array): time axis
            self.ttot (int): total number of time steps
            self.t_i (int): the current time step
            self.traces (dict): traces
        """
        TimeAxis.__init__(self, T, dt, **kwargs)
        self.ttot = len(self.tax)
        self.t_i = 0
        self.traces = dict()
        self.sources = dict()

    def step(self):
        """ increase time step self.t_i by one """
        if self.t_i < self.T:
            self.t_i += 1

    def add_new_trace(self, source, trace_name=None):
        """
        Set up a new recording to a variable
        Note: you don't need to record the stimulus, you pre-generated it
        Args:
            source (list): list length one. variable to record, ie. u1.r, which has a mutable value you can
                access like u1.r[0]
            trace_name (str): name of the trace
        Returns:  None; adds a new trace to self.traces (dict)
        """
        if not trace_name:
            trace_name = source
        blank_trace = np.zeros(self.ttot)
        self.traces[trace_name] = blank_trace
        self.sources[trace_name] = source

    def update_trace(self, trace_name):
        """
        recorder- takes data coming in and marks it on the trace at time self.t_i
        Args:
            trace_name (str): the name of the trace
            value (float): the value to set at time self.t_i on the trace
        """
        value = self.sources[trace_name][0]
        self.traces[trace_name][self.t_i] = value

