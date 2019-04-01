import numpy as np
import soundcard as sc
import matplotlib.pyplot as plt

speaker = sc.default_speaker()
mic = sc.default_microphone()

sample_rate = 41000
# give record time in seconds!
record_time = 4

# record data into a np.array
print('Record on!')
signal = mic.record(samplerate=sample_rate, numframes=sample_rate * record_time)
signal = np.delete(signal, 1, 1)  # delete redundant second channel of recording (mono recording)
signal = np.squeeze(signal)  # remove singleton dimension
# play sample
speaker.play(signal / np.max(signal), samplerate=sample_rate)

time = np.arange(0, sample_rate*record_time)/sample_rate
# extract onset peaks from signal
signal_power = np.convolve(np.abs(signal), np.hanning(1000))  # convolving abs.valued data with hanning filter to get a smooth
signal_onsets = np.convolve(signal_power, 1000*[1,-1])

plt.figure()
plt.plot(signal)
plt.plot(signal_power)
plt.plot(np.where(signal_onsets > 0, signal_onsets, 0))
plt.show()


