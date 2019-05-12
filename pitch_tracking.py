import librosa
import numpy as np
import sounddevice as sd
import matplotlib
matplotlib.use("TKAgg")
import matplotlib.pyplot as plt
import math
import pygame
from play_midi import MIDIPlayer
import time

duration = 8   # seconds

sample_rate = 41000
sd.default.samplerate = sample_rate
sd.default.channels = 1
pygame.mixer.init(buffer=1024)  # initialize pygame mixer
beep = pygame.mixer.Sound("Sounds/record_beep.wav")  # set beep sound

for i in range(4):
    print("Record starts in..." + str(4-i))
    beep.play()
    time.sleep(1)  # 3*times the length of the beep sound to prevent overlap with recording
print("Record on...")
signal = sd.rec( int( duration * sample_rate ), blocking=True )
# print("Playback...")
# sd.play(signal, blocking=True)
signal = np.squeeze(signal)
t = np.linspace(0, duration, len(signal))
plt.subplot(311)
plt.plot(t, signal)

# signal processing part

signal_filt = signal**2
window = 200
avg_mask = np.ones(window) / window
signal_filt = np.convolve(signal_filt, avg_mask, 'same')  # moving_avg signal for thresholding

plt.subplot(312)
plt.plot(t, signal_filt)
th_filt = signal_filt > np.amax(signal_filt)*0.005
plt.subplot(313)
plt.plot(t, th_filt)
#plt.show()

pitches, magnitudes = librosa.core.piptrack( y=signal, sr=sample_rate, fmin=500, fmax=5000 )

idxs = magnitudes.argmax(axis=0)
p = [pitches[idx, t] for t, idx in enumerate(idxs)]
p = np.array(p)
np.place(p, p == 0, 1)  # handle zeros in frequency array (log problem)
p = librosa.core.hz_to_midi(p)


scale_factor = math.ceil(th_filt.shape[0]/p.shape[0])
small_th = th_filt[0:-1:scale_factor]   # small size binary threshold data
filtered_midi = small_th*p  # thresholded midi data
filtered_midi[np.isnan(filtered_midi)] = 0  # replace nans with 0s
plt.figure(figsize=(12, 6))
plt.plot(filtered_midi)
plt.title('Thresholded and rounded MIDI notes')
#plt.show()

diff_mask = np.array([1, 1, -1, -1])
note_change = np.convolve(filtered_midi, diff_mask, 'same')  # detect note changes with diff filter
note_on = np.amax(note_change)*0.8 < note_change
note_off = np.min(note_change)*0.8 < note_change
event_map = note_on.astype(int)-(note_off-1)
events = np.where(event_map == 1)[0]
sleep_times = np.append(events, len(event_map)-1)-np.insert(events, 0, 0)
events = np.insert(events, 0, 0)  # treat start as an event

midi_input = np.asarray([filtered_midi[events].astype(int), small_th[events].astype(int)*127, sleep_times])  # create the input for MIDIPlayer
#midi input format :[MIDI notes, velocities, time of play]
print(midi_input)
mp = MIDIPlayer()
mp.play_midi_sequence(midi_input, duration, 32)

