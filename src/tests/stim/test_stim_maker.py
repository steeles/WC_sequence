from collections import OrderedDict

import numpy as np
from scipy.stats import norm
import melopy.utility as music
from src.stim.stim_maker import fq_tuning_curve


def test_fq_tuning_curve():
    actual = fq_tuning_curve()
    assert actual[49] == 1
    assert music.key_to_frequency(49) == 440


def test_fq_tuning_actual_normal():
    actual = fq_tuning_curve(6, 'A', 2.5)
    equivalent_xax = np.linspace(-3,2,len(actual))
    yvals = norm.pdf(equivalent_xax, 0, 2.5)
    assert list(yvals/np.max(yvals)) == actual.values()


