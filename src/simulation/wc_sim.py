from src.a_wilson_cowan.wc_unit import WCUnit
from src.stim.stim_maker import aba_triplet

from simulation import Simulation


class WCTripletsSimulation(Simulation):

    def __init__(self, T=5, dt=.001, **kwargs):
        Simulation.__init__(T=T, dt=dt, **kwargs)


if __name__ == '__main__':
    u1 = WCUnit()
    triplet = aba_triplet()
