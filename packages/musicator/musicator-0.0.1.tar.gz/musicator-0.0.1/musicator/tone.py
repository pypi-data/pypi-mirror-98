from scipy.io.wavfile import write as wavwrite
import numpy as np

__all__ = ('wavwrite', 'generate')


def generate(hz, duration, rate):
    x = np.linspace(0, duration, rate * duration, endpoint=False)
    frequencies = x * hz
    y = np.sin((2 * np.pi) * frequencies)
    return y
