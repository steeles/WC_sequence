from src.a_wilson_cowan.currents import Current, StimCurrent, SFACurrent
from src.a_wilson_cowan.wc_unit import WCUnit


class Target():
    a = [0]


def test_SFA_update():
    r = [0]
    u1 = Target
    sfa = SFACurrent(source=r, weight=.8, target=u1, name="test")
    r[0]=.9
    sfa.update()
    sfa_value_1 = sfa.value
    assert sfa_value_1 > 0
    for ind in range(100):
        sfa.update()
    assert u1.a[0] == sfa.value
    assert sfa.value > sfa_value_1