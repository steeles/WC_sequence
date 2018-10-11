
from src.wilson_cowan.wc_unit import WCUnit, Simulation, Synapse


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

def test_synapse_init():
    syn = Synapse(foobar=42)
    assert syn.k == 0.1
    assert syn.theta == .2