import numpy as np
import soundcard as sc
import matplotlib
matplotlib.use("TKAgg")
import matplotlib.pyplot as plt
import librosa

speaker = sc.default_speaker()
mic = sc.default_microphone()

sample_rate = 41000
# give record time in seconds!
record_time = 3
t = np.linspace(0, record_time, sample_rate*record_time)

# record data into a np.array
print('Record on!')
signal = mic.record(samplerate=sample_rate, numframes=sample_rate * record_time)
print('Record off!')
signal = np.delete(signal, 1, 1)  # delete redundant second channel of recording (mono recording)
signal = np.squeeze(signal)  # remove singleton dimension

# play sample
speaker.play(signal / np.max(signal), samplerate=sample_rate)
print("Playback Done!")

# extract onset peaks from signal
onsets=librosa.onset.onset_detect(signal,sample_rate,units='time')

plt.figure(figsize=(12, 6))
plt.plot(t,signal)
plt.title("Audio signal")
plt.xlabel("frame")
for onset_t in onsets:
    plt.axvline(onset_t,color='r')
plt.show()