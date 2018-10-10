from collections import OrderedDict

import numpy as np
from scipy.stats import norm
import melopy.utility as music
from src.stim.stim_maker import fq_tuning_curve, aba_triplet

def test_fq_tuning_curve():
    actual = fq_tuning_curve()
    assert actual[49] == 1
    assert music.key_to_frequency(49) == 440


def test_fq_tuning_actual_normal():
    actual = fq_tuning_curve(6, 'A', 2.5)
    equivalent_xax = np.linspace(-3, 2, len(actual))
    yvals = norm.pdf(equivalent_xax, 0, 2.5)
    assert list(yvals / np.max(yvals)) == actual.values()


def test_triplets():
    tc = OrderedDict(
        [
            (43.0, 0.1353352832366127), (44.0, 0.24935220877729614), (45.0, 0.41111229050718745),
            (46.0, 0.6065306597126333), (47.0, 0.8007374029168081), (48.0, 0.9459594689067655), (49.0, 1.0),
            (50.0, 0.9459594689067655), (51.0, 0.8007374029168081), (52.0, 0.6065306597126333),
            (53.0, 0.41111229050718745),
            (54.0, 0.24935220877729614)
        ]
    )
    actual = aba_triplet(tc, 3)
    # they're all the same
    assert all(actual[0] == actual[1])
    assert all(actual[1] == actual[2])

    # the middle is smaller than the edge
    assert actual[1, int(actual.shape[1]/3)] < actual[0, 1]

    # the end is silent
    assert actual[2, -1] == 0

    # gap?

