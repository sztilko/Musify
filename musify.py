import numpy as np
import soundcard as sc
import matplotlib
matplotlib.use("TKAgg")
import matplotlib.pyplot as plt


speaker = sc.default_speaker()
mic = sc.default_microphone()

sample_rate = 41000
# give record time in seconds!
record_time = 4
t = np.linspace(0, 4, sample_rate*record_time)

# record data into a np.array
print('Record on!')
signal = mic.record(samplerate=sample_rate, numframes=sample_rate * record_time)
signal = np.delete(signal, 1, 1)  # delete redundant second channel of recording (mono recording)
signal = np.squeeze(signal)  # remove singleton dimension
# play sample
print('Record off!')
speaker.play(signal / np.max(signal), samplerate=sample_rate)
print("Playback Done!")


time = np.arange(0, sample_rate*record_time)/sample_rate
# extract onset peaks from signal
signal_power = np.convolve(np.abs(signal), np.hanning(1000))  # convolving abs.valued data with hanning filter to get a smooth (signal power calculated as integrating with apprx 25ms Hanning window)
signal_onsets = np.convolve(signal_power, 1000*[1, -1])

print("Now plot!")
plt.figure(figsize=(12, 6))
plt.subplot(211)
plt.title("Audio signal")
plt.xlabel("frame")
plt.plot(signal)

plt.subplot(212)
plt.plot(signal_power, label="Signal power")
plt.plot(np.where(signal_onsets > 0, signal_onsets, 0), label="Signal onset")
plt.xlabel("frame")
plt.grid()
plt.legend(loc="best")
plt.show()


