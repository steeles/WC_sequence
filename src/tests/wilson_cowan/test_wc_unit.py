import numpy as np
from src.a_wilson_cowan.wc_unit \
    import WCUnit, StimCurrent


def test_wc_unit_init():
    wc = WCUnit()
    assert wc.tauNMDA == 100
    wc2 = WCUnit(tau=200, foo="bar")
    assert wc2.tau == 200
    assert wc2.foo == "bar"
    assert wc2.tauNMDA == 100


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
    u2.currents["stim"].update()
    assert u2.stim[0] == 0.5

def test_add_SFA_current():
    u2 = WCUnit(name="u2")
    u2.add_SFA_current(.8)
    u2.r[0] = 1
    u2.currents['SFA'].update()
    assert u2.a[0] > 0

def test_wc_update():
    u2 = WCUnit(name="u2")
    stim = np.ones(10)
    u2.add_stim_current(
        stimulus=stim, weight=.5)
    assert u2.currents["stim"].weight == .5
    u2.currents["stim"].t = 1
    u2.currents["stim"].update()
    u2.update()
    assert u2.r[0] > 0.05
    assert u2.r[0] < 0.055

def test_wc_higher_weight_update():
    u2 = WCUnit(name="u2")
    stim = np.ones(10)
    u2.add_stim_current(
        stimulus=stim, weight=.9)
    assert u2.currents["stim"].weight == .9
    u2.currents["stim"].t = 1
    u2.currents["stim"].update()
    u2.update()
    assert u2.r[0] > 0.085
    assert u2.r[0] < 0.09

def test_lower_weights_drive_less():
    pass


def test_add_intrinsic_currents():
    u1 = WCUnit(name="u1", tauA=300, gSFA=0.8)
    stim = np.ones(10)
    u1.add_stim_current(stimulus=stim, weight=.9)
    for ind in xrange(10):
        u1.update_all()
    print(u1.a)
    print(u1.currents["SFA"].value)

    u2 = WCUnit(tauA=30, gSFA=0.8)
    stim = np.ones(10)
    u2.add_stim_current(stimulus=stim, weight=.9)
    for ind in xrange(10):
        u2.update_all()
    print(u2.a)
    print(u2.currents["SFA"].value)

    u3 = WCUnit(tauA=30, gSFA=0.5)
    stim = np.ones(10)
    u3.add_stim_current(stimulus=stim, weight=.9)
    for ind in xrange(10):
        u3.update_all()
    print(u3.a)
    print(u3.currents["SFA"].value)
    assert False

