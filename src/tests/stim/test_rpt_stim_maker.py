from src.stim.rpt_stim_maker import ABAStimulus


def test_tones():
    stim = ABAStimulus()
    print(stim.__dict__)
    assert False