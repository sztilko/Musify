import pygame
import pygame.sndarray
import numpy
import scipy.signal
import librosa
import sounddevice as sd


np = numpy
fs = sample_rate = 44100
#pygame.init()
pygame.mixer.init(44100, -16, 1, 2048)


def play_for(sample_wave, ms):
    """Play the given NumPy array, as a sound, for ms milliseconds."""
    sound = pygame.sndarray.make_sound(sample_wave)
    sound.play(-1)
    pygame.time.delay(ms)
    sound.stop()


def sine_wave(hz, peak, n_samples=sample_rate):
    """Compute N samples of a sine wave with given frequency and peak amplitude.
       Defaults to one second.
    """
    length = sample_rate / float(hz)
    omega = numpy.pi * 2 / length
    xvalues = numpy.arange(int(length)) * omega
    onecycle = peak * numpy.sin(xvalues)
    return numpy.resize(onecycle, (n_samples,)).astype(numpy.int16)


def square_wave(hz, peak, duty_cycle=.5, n_samples=sample_rate):
    """Compute N samples of a sine wave with given frequency and peak amplitude.
       Defaults to one second.
    """
    t = numpy.linspace(0, 1, 500 * 440/hz, endpoint=False)
    wave = scipy.signal.square(2 * numpy.pi * 5 * t, duty=duty_cycle)
    wave = numpy.resize(wave, (n_samples,))
    return (peak / 2 * wave).astype(numpy.int16)


# Play A (440Hz) for 1 second as a sine wave:
play_for(sine_wave(440, 4096), 2000)

# Play A-440 for 1 second as a square wave:
play_for(sum([sine_wave(440, 4096), sine_wave(880, 4096)]), 2000)

duration = 5  # seconds
signal = sd.rec(int(duration * fs), samplerate=fs, channels=1)
print("Record on...")
sd.wait()
sd.play(signal, fs)
print("Playback...")
sd.wait()

signal = np.squeeze(signal)
t = np.linspace(0, duration, len(signal))

pitches, magnitudes = librosa.core.piptrack(y=signal, sr=fs, fmin=500, fmax=5000)

n = pitches.shape[1]
tt = np.linspace(0, duration, n)
dn = duration/n

print(pitches.shape, magnitudes.shape)

idxs = magnitudes.argmax(axis=0)
print(f"Shape of idxs: {idxs.shape}")

p = [pitches[idx, t] for t, idx in enumerate(idxs)]

for item in p:
    # Play A (440Hz) for 1 second as a sine wave:
    play_for(sine_wave(item, 4096), int(round(dn*1000)))
