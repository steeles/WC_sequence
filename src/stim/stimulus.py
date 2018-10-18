import numpy as np
from src.simulation.simulation import TimeAxis
from src.a_wilson_cowan.currents import Current


class ToneCurrent(Current):
    """ class to use with SensoryNeurons and ABAStimulus; leverages sn.tuning curve to map current to cell
    """
    def __init__(self, stimulus, weight, target, name=None):
        """
        create a tone stimulus current
        Args:
            stimulus (src.stim.stimulus.ABAStimulus): ABA stimulus in sequence of tones; parent TimeAxis
            weight (float): strength of current on target
            target (src.a_wilson_cowan.sensory_neuron.SensoryUnit): a SensoryUnit with a self.tuning_curve
            name (str): what to call it in target.current[name]
        """
        Current.__init__(self, weight=weight, target=target, name=name)
        self.stimulus = stimulus
        self.value = self.map_tone_to_current()

    def map_tone_to_current(self):
        """
        semitone -> weight x tuning curve -> current
        looks up the semitone value of the stimulus right now and maps it to a current with tuning curve and weight
        """
        value = self.target.tuning_curve[self.stimulus.value] * self.weight
        return value

    def update(self):
        """ update the stim (incr t_i by +1) and map it to the target as a current """
        self.stimulus.update()
        self.value = self.map_tone_to_current()


class ABAStimulus(TimeAxis):
    """ master stimulus class; subclass of TimeAxis, with time granularity functions """
    def __init__(self, df=3, iti=.05, a_semitone=49, b_semitone=None, tone_length=0.03, T=5, dt=.001, **kwargs):
        """
        create a new ABAStimulus object
        Args:
            df Optional(int): difference in frequency for ABA triplet. Preferred.
            iti (float): inter-tone-interval
            a_semitone (int): default 49 <as in key of a piano>, A 440; you can get frequency in Hz with
                music.key_to_frequency(a_semitone)
            b_semitone Optional(int):
            tone_length (float):
            T (float): total time in seconds
            dt (float): timescale of simulation in seconds (also integration time step)
            **kwargs:
        """
        TimeAxis.__init__(self, T, dt, **kwargs)
        self.df = df
        self.iti = iti
        self.a_semitone = a_semitone
        if df:
            self.b_semitone = a_semitone + df
        elif b_semitone:
            self.b_semitone = b_semitone
        else:
            print('need a b tone')
        self.tone_length = tone_length
        # can it use its own method to create an attribute on init?
        self.trt = int(self.iti / self.dt)
        self.period = 4 * self.trt
        self.tone_time = int(self.tone_length / self.dt)
        self.tones = self.repeating_tones()
        self.value = self.tones[self.t_i]
        # we also have ttot, tax, t_i

    def generate_triplet_tones(self):
        """ returns 1d numpy.array with the tones in a single triplet """
        triplet = np.zeros(self.period)
        triplet[:self.tone_time] = self.a_semitone
        triplet[self.trt:self.trt + self.tone_time] = self.b_semitone
        triplet[2 * self.trt:2 * self.trt + self.tone_time] = self.a_semitone
        return triplet

    def repeating_tones(self):
        """
        create sequence of tones (unit: melopy.key, semitone) on a time grid of dt
        Returns:
            numpy.array: 1D array of tones
        """
        triplet = self.generate_triplet_tones()
        tones = np.zeros(self.ttot)
        n_cycles = int(np.ceil(self.ttot/self.period))
        tmp = np.tile(triplet, [1, n_cycles])
        tones[:tmp.shape[1]] = tmp
        return tones

    def update(self):
        self.t_i += 1
        self.value = self.tones[self.t_i]

"""pars from micheyl 20015: Each sequence was comprised of 20 triplets.
Each tone was 125 ms in duration, including 20 ms raised-cosine
ramps. In the basic test condition, there was no silent gap between
the tones within a triplet, and the silent gap between consecutive
triplets was also 125 ms long, resulting in a total sequence duration
of 10 s. The A and B tone frequencies were kept constant within a
sequence. The A tone frequency was selected randomly for each
listener among four possible frequencies (500, 1000, 2000, and
4000 Hz). The B tone frequency was varied parametrically across
sequences, and depending on the condition being tested, it was 1,
3, 6, or 9 semitones above the A tone frequency (for instance, at
the 1000 Hz A tone frequency, the frequency of the B tones was
1059, 1189, 1414, or 1682 Hz). These four frequency separations
(Fs) were selected, based on published data (Carlyon et al., 2001)
and preliminary results, to yield different build-up rates and asymptotic
levels of perceived stream segregation. Another series of test
conditions was produced by inserting 50 ms silent gaps between
the tones within a triplet and increasing the intertriplet gap duration
to 175 ms, resulting in a slower tone-repetition rate """