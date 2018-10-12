import numpy as np
from src.a_wilson_cowan.wc_unit \
    import WCUnit, Simulation, Current, StimCurrent


def test_wc_unit_init():
    wc = WCUnit()
    assert wc.tauNMDA == 100
    wc2 = WCUnit(tau=200, foo="bar")
    assert wc2.tau == 200
    assert wc2.foo == "bar"
    assert wc2.tauNMDA == 100


def test_simulation_init():
    eps = .000001
    sim = Simulation()
    assert sim.ttot == 5/.001
    sim2 = Simulation(dt=.05,T=5000)
    tax = sim2.tax
    assert tax[-1]-tax[-2]-.05 < eps


def test_stim_current_init():
    u3 = WCUnit(name="u3")
    stim = np.ones(10)
    curr = StimCurrent(stim, .5, u3)
    assert curr.target.name == "u3"


def test_wc_add_stim_current():
    u2 = WCUnit(name="u2")
    stim = np.ones(10)
    u2.add_stim_current(
        stimulus=stim, weight=.5)
    assert u2.currents["stim"].weight == .5
    u2.currents["stim"].update(0)
    assert u2.stim[0] == 0.5


