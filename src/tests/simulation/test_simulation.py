from src.simulation.simulation import Simulation



def test_simulation_init():
    eps = .000001
    sim = Simulation()
    assert sim.ttot == 5/.001
    sim2 = Simulation(dt=.05,T=5000)
    tax = sim2.tax
    assert tax[-1]-tax[-2]-.05 < eps

