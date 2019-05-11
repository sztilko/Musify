import librosa
import numpy as np
import sounddevice as sd
import matplotlib
matplotlib.use("TKAgg")
import matplotlib.pyplot as plt


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

pitches, magnitudes = librosa.core.piptrack(y=signal, sr=fs, fmin=500, fmax=5000)

print(pitches.shape, magnitudes.shape)

idxs = magnitudes.argmax(axis=0)
print(f"Shape of idxs: {idxs.shape}")

p = [pitches[idx, t] for t, idx in enumerate(idxs)]
p = librosa.core.hz_to_note(p)
p = librosa.core.note_to_midi(p)

print(len(p))
plt.figure(figsize=(12, 6))
plt.plot(p, '.')
plt.show()



