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
    u2.add_SFA_current(weight=.8)
    u2.r[0] = 1
    u2.currents['SFA'].update()
    assert u2.a[0] > 0
    assert u2.currents['SFA'].weight < 0
    assert u2.currents['SFA'].value < 0
    u2.update()
    assert u2.r[0] < 1

def test_wc_update():
    u2 = WCUnit(name="u2")
    stim = np.ones(10)
    u2.add_stim_current(
        stimulus=stim, weight=.5)
    assert u2.currents["stim"].weight == .5
    u2.currents["stim"].t = 1
    u2.currents["stim"].update()
    u2.update()
    assert u2.r[0] > 0.08
    assert u2.r[0] < 0.085


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

def test_update_all():
    eps = .00001
    u1 = WCUnit(name="u1", tauA=300, gSFA=0.8)
    stim = np.ones(10)
    u1.add_stim_current(stimulus=stim, weight=.9)
    for ind in xrange(10):
        u1.update_all()
    assert u1.a[0] > 0



def test_add_intrinsic_currents_SFA():
    """
    i could wind up changing the defaults; i should just check that
    the logical relationships follow
    """
    eps = .00001
    u1 = WCUnit(name="u1", tauA=300, gSFA=0.8)
    stim = np.ones(10)
    u1.add_stim_current(stimulus=stim, weight=.9)
    for ind in xrange(10):
        u1.update_all()
    assert u1.a[0] > 0
    assert u1.currents["SFA"].value > 0
    # assert abs(u1.currents["SFA"].value) < u1.a[0]

    u2 = WCUnit(tauA=30, gSFA=0.8)
    stim = np.ones(10)
    u2.add_stim_current(stimulus=stim, weight=.9)
    for ind in xrange(10):
        u2.update_all()
    # tauA is shorter so there should be more
    assert u2.a[0] > u1.a[0]
    # assert abs((u2.a[0]/ u1.a[0]) - (u2.currents["SFA"].value / u1.currents["SFA"].value)) < eps

    u3 = WCUnit(tauA=30, gSFA=0.5)
    stim = np.ones(10)
    u3.add_stim_current(stimulus=stim, weight=.9)
    for ind in xrange(10):
        u3.update_all()
    assert abs(u3.currents["SFA"].value -\
           u2.currents["SFA"].value) < eps
    assert abs(u3.a[0] - u2.a[0]) < eps
    print u3.currents["SFA"].weight
    print u2.r
    assert u1.r[0] - u2.r[0] > eps
    assert u3.r[0] - u2.r[0] > eps
    # assert u3.a[0] < u2.a[0]
