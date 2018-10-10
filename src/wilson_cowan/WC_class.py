# basic bare bones WC unit
# this guy wants to know its parameters and how to update its value
# from numpy import exp
# print "exp loaded"
import numpy as np
import matplotlib.pyplot as plt
import pdb
import collections
import pandas as pd

Current = collections.namedtuple("Current", ['source', 'weight'])
'''if i need to make changes to the default parameters,
i should do it here'''

defaultPars = dict(
    ke=.1, the=.2,  # IO params
    kS=.1, thS=.5,
    r0=0., a0=0., S0=0., stim0=1.,  # time varying values
    gee=.57,
    gStim=1.,
    gSFA=0,
    tau=10., tauNMDA=100., tauA=200., G=.64)


# factor out the simulator
class WC_net_unit(object):
    _registry = []

    """ Creates a basic WC unit. To assign pars from a dictionary, 
    use WC_unit(**parsDict) """

    """adding capacity for units to form connections with other units"""

    def __init__(self, **kwargs):
        self.__dict__.update(defaultPars, **kwargs)
        # update the registry; this
        # print self

        self.params = self.__dict__.copy()
        self._registry.append(self)

        self.currents = dict()
        self.cxParams = dict()
        self.r = [self.r0]
        self.a = [self.a0]
        self.S = [self.S0]
        self.stim = [self.stim0]

        self.init_intrinsicCurrents()

    def init_intrinsicCurrents(self):
        if self.gee != 0:
            self.addNewCurrent(source=self.r, weight=self.gee, name="self_excitation")

        if self.gStim != 0:
            self.addNewCurrent(source=self.stim, weight=self.gStim, name="stim_current")

        if self.gSFA != 0:
            self.addNewCurrent(source=self.a, weight=-self.gSFA, name="SFA")

    def getCxParams(self):
        return self.cxParams

    def getParams(self):
        self.params.update(self.cxParams)
        return self.params

    # wanna be able to do with one or many
    def setCxParams(self, new_connections_dict):
        self.cxParams.update(new_connections_dict)

    # probably with this one too
    def addNewCurrent(self, source, weight, name):

        self.currents[name] = Current(source=source, weight=weight)
        self.cxParams[name] = weight

    def removeCurrent(self, name):
        if name in self.currents:
            del self.currents[name]

    # @profile
    def currentValues(self):
        # ind = self.currents.keys()
        cvals = np.zeros(len(self.currents))
        counter = 0
        for c in self.currents.itervalues():
            # print c.source
            val = c.source[0] * c.weight
            cvals[counter] = val
            counter += 1
        self.cvals = cvals

    def stimFeed(self, stimSource):

        self.stim[0] = stimSource

    def f_r(self, x):
        th = self.the
        k = self.ke

        return 1 / (1 + np.exp(-(x - th) / k)) - 1 / (1 + np.exp(th / k))

    def f_S(self, x):
        th = self.thS
        k = self.kS
        return 1 / (1 + np.exp(-(x - th) / k))

    def updateS(self, dt=1):
        dS = (-self.S[0] / self.tauNMDA + (1 - self.S[0]) * self.G * self.f_S(self.r[0])) * dt
        self.S[0] += dS

    def updateA(self, dt=1):
        da = dt / self.tauA * (-self.a[0] + self.r[0])
        self.a[0] += da

    def updateR(self, dt=1):
        self.currentValues()

        dr = dt / self.tau * (-self.r[0] + self.f_r(sum(self.cvals)))
        self.r[0] += dr

    # wanna do this in some sort of way that lets me record all the currents too
    @staticmethod
    def integrator(dt=1., T=500., stimSource=None, restart=True):

        tax = np.arange(dt, T + dt, dt)
        ttot = len(tax)

        for unit in WC_net_unit._registry:
            unit.rTrace = np.zeros(ttot)
            unit.aTrace = np.zeros(ttot)
            unit.Strace = np.zeros(ttot)

            if restart:
                unit.r[0] = unit.r0
                unit.a[0] = unit.a0
                unit.S[0] = unit.S0
                unit.stim[0] = unit.stim0

            unit.tax = tax
            unit.currentValues()
            unit.currentTrace = np.zeros((ttot, len(unit.currents)))

        for t in xrange(ttot):
            counter = 0
            for unit in WC_net_unit._registry:

                ''' lets me put vectorized stim in there (?)'''
                if stimSource is not None:
                    unit.stim[0] = stimSource[counter, t]

                unit.rTrace[t] = unit.r[0]
                unit.aTrace[t] = unit.a[0]
                unit.Strace[t] = unit.S[0]

                unit.currentTrace[t, :] = unit.cvals
                unit.updateR(dt)
                unit.updateA(dt)
                unit.updateS(dt)
                counter += 1
        for unit in WC_net_unit._registry:
            df2 = pd.DataFrame(unit.currentTrace,
                               index=unit.tax, columns=unit.currents.keys())
            unit.currentTrace = df2  # slap some labels on those currents!

            # this concatenation apparently takes forever
            unit.records = df2.copy()
            unit.records.insert(0, 'FR', pd.Series(unit.rTrace, index=df2.index))

            unit.records = unit.records.drop(
                unit.records.tail(1).index)

    '''one issue with this one is it doesn't let me do isolated plots.
    I also want to do fixed line types '''

    @staticmethod
    def plot_timecourses(netnames=None):
        nUnits = len(WC_net_unit._registry)
        fig, axes = plt.subplots(nrows=nUnits, figsize=(12., 9.))
        fixedNames = ['FR', 'stim_current', 'self_excitation', 'SFA']

        # line pars for each entry in the list of fixedNames
        fixedPars = [dict(color='b', linewidth=1.5),  # FR
                     dict(color='k'),  # stim_current
                     dict(color='g'),  # self_excitation
                     dict(color='r')]

        nLeftoverColors = 7
        cm = plt.get_cmap('gnuplot')
        palette = [cm(1. * i / nLeftoverColors) for i in range(nLeftoverColors)]

        # plt.rc('axes', color_cycle=) #hopefully cycle through

        for ind in xrange(nUnits):
            unit = WC_net_unit._registry[ind]

            ax = axes[ind]
            df = unit.records
            cols = df.columns
            leftovers = [x for x in cols if x not in fixedNames]
            # pdb.set_trace()
            # first plot the fixed guys as they show up
            for nInd in xrange(len(fixedNames)):
                name = fixedNames[nInd]
                if name in cols:
                    ax.plot(df.index, df[name], label=name, **fixedPars[nInd])

            for nInd in xrange(len(leftovers)):
                name = leftovers[nInd]
                if name in cols:
                    ax.plot(df.index, df[name], label=name, color=palette[nInd + 2])

            #			unit.records.plot(ax=ax)
            if netnames is not None:
                ax.set_title(netnames[ind])

            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.legend(loc='right', prop={'size': 11})
            ax.set_ylim([-1.1, 1.1])
            ax.set_ylabel('FR, current')

        axes[-1].set_xlabel('time (ms)', fontsize=16)
        fig.tight_layout()
        plt.show(block=False)

    def plot_derivatives(self, iapp=0):
        # possible values of E:
        # vectorize all currents... and combinations of currents...

        E_ax = np.arange(-0.2, 1.2, .01)
        # column vector it up
        xax = E_ax[np.newaxis].T

        if 'self_excitation' in self.currentTrace.columns:
            x = self.currentTrace.drop('self_excitation', 1)
        else:
            x = self.currentTrace

        # plot dR for all R's with each current at its most extreme value
        if iapp == "each":
            extremeCvals = np.where(np.max(abs(x), 0) == abs(np.min(x, 0)), \
                                    np.min(x, 0), np.max(x, 0))
            iapp = np.tile(extremeCvals, (len(E_ax), 1))
            E_ax = np.tile(xax, (1, len(extremeCvals)))

        dE = (-E_ax + self.f_r(iapp + self.gee * E_ax))

        dEdf = pd.DataFrame(dE, columns=x.columns, index=xax)
        # pdb.set_trace()
        # zline = np.zeros(len(xax))
        # plt.figure()
        # plot(xax,dE(xax,minInp),'b')
        # ax = plt.gca()
        # plt.figure()
        tmp = dEdf.plot()
        # pdb.set_trace()
        tmp.hlines(0, tmp.get_xlim()[0], tmp.get_xlim()[1])
        plt.title("extreme values")
        # print "plotted zline"
        # plt.title("extreme values")

        plt.show(block=False)


if __name__ == "__main__":
    foo = WC_net_unit(gSFA=.7, gee=0, r0=0.5, the=0., gStim=0.6)
    bar = WC_net_unit(gSFA=.7, gee=0, the=0., gStim=0.6)

    foo.addNewCurrent(bar.r, -1, "bar_inh_foo")

    bar.addNewCurrent(foo.r, -1, "foo_inh_bar")

    netnames = ["foo", "bar"]

    WC_net_unit.integrator(T=5000)

    WC_net_unit.plot_timecourses(netnames)

# return tax,E,a,Isyn,stim




