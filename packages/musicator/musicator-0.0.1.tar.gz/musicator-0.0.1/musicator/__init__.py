import musicator.tone as _tone
import numpy as np

__all__ = ['Composer']


class Composer:
    __tones__ = []
    def __init__(self):
        pass
    def tone(self, *_, hz, duration):
        self.__tones__.append((hz, duration))
    def save(self, fout, rate=44100):
        res = []
        for tone in self.__tones__:
            res += list(_tone.generate(*tone, rate))
        _tone.wavwrite(fout, rate, np.array(res, dtype='float64'))
