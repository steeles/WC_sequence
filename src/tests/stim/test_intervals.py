import numpy as np

from src.stim.intervals import ABInterval, BAInterval, Intervals


def test_intervals():
    out = Intervals()
    ab = out.generate_ab_interval()
    ba = out.generate_ba_interval()
    # a is higher than b
    assert ab[0] > ba[0]
    # out inits with ab
    assert out.tones[0] == ab[0]
    out.set_ba()
    assert out.tones[0] == ba[0]