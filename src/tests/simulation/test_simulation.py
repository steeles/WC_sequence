import numpy as np
from src.simulation.simulation import Simulation
from src.simulation.traces import Trace, CurrentTrace
from src.a_wilson_cowan.currents import Current


class dCurrent(Current):
    def update(self):
        self.value=self.source[0]


def test_simulation_init():
    eps = .000001
    sim = Simulation()
    assert sim.ttot == 5/.001
    sim2 = Simulation(dt=.05,T=5000)
    tax = sim2.tax
    assert tax[-1]-tax[-2]-.05 < eps


def test_trace():
    sim = Simulation()
    src = [0]
    trc = Trace(sim, source=src, target=sim.traces, trace_name="foo")
    # print(trc.__dict__.get("source"))
    for ind in xrange(5):
        src[0] = ind
        trc.update_trace()
        trc.sim.step()
    #print(trc.__dict__)
    assert len(trc.trace) == trc.sim.ttot
    trc.trace[:5]
    assert all(trc.trace[:5] == np.array([0., 1., 2., 3., 4.]))


def test_current_trace():
    src = [0]
    curr = dCurrent(source=src, weight=0.5, target={}, name="foo")
    sim = Simulation()
    tar = {}
    trc = CurrentTrace(sim=sim, source=curr, target=tar, trace_name="foo")
    print(tar)
    assert isinstance(tar["foo"], CurrentTrace)
    for ind in xrange(5):
        src[0] = ind
        curr.update()
        trc.update_trace()
        trc.sim.step()
    trc.update_trace()
    # print trc.trace[:10]
    assert trc.trace[4] == src[0] * curr.weight
    # assert False


############## TODO NOOOOO
def test_nested_trace():
    # this seems very annoying... TODO: I HATE THIS
    sim = Simulation()
    sim.traces["foo"]=dict()
    src = [0]
    trc = Trace(sim, source=src, target=sim.traces["foo"], trace_name="bar")
    # print(trc.__dict__.get("source"))
    for ind in xrange(5):
        src[0] = ind
        trc.update_trace()
        trc.sim.step()
    print(sim.traces["foo"]["bar"].source)
    print(sim.traces["foo"]["bar"].trace)

    assert len(sim.traces["foo"]["bar"].trace)==sim.ttot
    assert sim.traces["foo"]["bar"].source[0] == 4
    assert sim.traces["foo"]["bar"].trace[4] == 4


    #assert False

