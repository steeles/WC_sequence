import numpy as np
from src.simulation.simulation import Simulation, Trace



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


def test_nested_trace():
    sim = Simulation()
    sim.traces["foo"]=dict()
    src = [0]
    trc = Trace(sim, source=src, target=sim.traces["foo"], trace_name="bar")
    # print(trc.__dict__.get("source"))
    for ind in xrange(5):
        src[0] = ind
        trc.update_trace()
        trc.sim.step()

    assert sim.traces["foo"]["bar"]
    assert False

