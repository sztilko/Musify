import librosa
import numpy as np


def detect_pitch(y, sr, t):
    """
     Pick the pitch at a certain frame 't' is simple. First getting the bin of the strongest frequency by looking at
     the magnitudes array, and then finding the pitch at pitches[index, t]

    :param y: audio time series
    :param sr: sampling rate
    :param t: time frame at which the pitch is required
    :return: The pitch at given timepoint
    """

    pitches, magnitudes = librosa.core.piptrack(y=y, sr=sr, fmin=75, fmax=1600)
    index = magnitudes[:, t].argmax()
    pitch = pitches[index, t]

    return pitch

# y, sr = librosa.load(filename, sr=40000)

# np.set_printoptions(threshold=np.nan)
# print pitches[np.nonzero(pitches)]

