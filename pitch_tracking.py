import librosa
import numpy as np
import sounddevice as sd
import matplotlib
matplotlib.use("TKAgg")
import matplotlib.pyplot as plt
import math
from play_midi import MIDIPlayer

sample_rate = 41000
sd.default.samplerate = sample_rate
sd.default.channels = 1
duration = 5  # seconds
print("Record on...")
signal = sd.rec( int( duration * sample_rate ), blocking=True )
# print("Playback...")
# sd.play(signal, blocking=True)
signal = np.squeeze(signal)
t = np.linspace(0, duration, len(signal))
plt.subplot(311)
plt.plot(t, signal)

signal_filt = signal**2
window = 200
avg_mask = np.ones(window) / window
signal_filt = np.convolve(signal_filt, avg_mask, 'same')

plt.subplot(312)
plt.plot(t, signal_filt)
th_filt = signal_filt > np.amax(signal_filt)*0.01
plt.subplot(313)
plt.plot(t, th_filt)
#plt.show()

pitches, magnitudes = librosa.core.piptrack( y=signal, sr=sample_rate, fmin=500, fmax=5000 )

idxs = magnitudes.argmax(axis=0)
p = [pitches[idx, t] for t, idx in enumerate(idxs)]
p = np.array(p)
np.place(p, p == 0, 1)  # handle zeros in frequency array (log problem)
p = librosa.core.hz_to_midi(p)

plt.figure(figsize=(12, 6))
scale_factor = math.ceil(th_filt.shape[0]/p.shape[0])
small_th = th_filt[0:-1:scale_factor]
filtered_midi = small_th*p
plt.plot(filtered_midi)
plt.title('Thresholded and rounded MIDI notes')
#plt.show()

mp = MIDIPlayer()
mp.play_midi_sequence(p, duration)

