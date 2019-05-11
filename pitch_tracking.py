import librosa
import numpy as np
import sounddevice as sd
import matplotlib
matplotlib.use("TKAgg")
import matplotlib.pyplot as plt
from play_midi import MIDIPlayer

fs = 41000

duration = 5  # seconds
signal = sd.rec(int(duration * fs), samplerate=fs, channels=1)
print("Record on...")
sd.wait()
sd.play(signal, fs)
print("Playback...")
sd.wait()

signal = np.squeeze(signal)
t = np.linspace(0, duration, len(signal))

strength = librosa.onset.onset_strength(signal, sr=fs)
onsets = librosa.onset.onset_detect(signal, sr=fs)

# plt.figure(figsize=(12, 6))
# plt.plot(signal, label="signal")
# plt.plot(strength, label="onset strength")
# for onset in onsets:
#     plt.axvline(onset)
# plt.legend(loc="best")
# plt.show()
#
# plt.figure(figsize=(12, 6))
# plt.plot(strength, label="onset strength")
# plt.legend()
# plt.show()

pitches, magnitudes = librosa.core.piptrack(y=signal, sr=fs, fmin=500, fmax=5000,)

print(pitches.shape, magnitudes.shape)

idxs = magnitudes.argmax(axis=0)
print(f"Shape of idxs: {idxs.shape}")

p = [pitches[idx, t] for t, idx in enumerate(idxs)]
p = librosa.core.hz_to_midi(p)

print(len(p))
plt.figure(figsize=(12, 6))
plt.plot(p, '.')
plt.show()

mp = MIDIPlayer()
mp.play_midi_sequency(p, duration)





