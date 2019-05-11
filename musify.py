import numpy as np
import sounddevice as sd
import matplotlib
matplotlib.use("TKAgg")
import matplotlib.pyplot as plt
import librosa
import pygame
import time

#set initial parameters
sample_rate = 41000  # sampling rate in Hz
record_time = 5  # record time in seconds
sd.default.samplerate = sample_rate
sd.default.channels = 1
pygame.mixer.init(buffer=1024)  # initialize pygame mixer
beep = pygame.mixer.Sound("Sounds/record_beep.wav")  # set beep sound

t = np.linspace(0, record_time, sample_rate*record_time)  # create time vector

# record data into a np.array
print('Record on!')
beep.play()
time.sleep(beep.get_length()*3)  #3*times the length of the beep sound to prevent overlap with recording
signal = sd.rec(sample_rate * record_time)
time.sleep(record_time)
print('Record off!')
beep.play()
time.sleep(beep.get_length())
signal = np.squeeze(signal)  # remove singleton dimension

# extract onset peaks from signal
onsets = librosa.onset.onset_detect(signal, sample_rate, units='time')

plt.figure(figsize=(12, 6))
plt.plot(t, signal)
plt.title("Audio signal")
plt.xlabel("frame")
for onset_t in onsets:
    plt.axvline(onset_t, color='r')
# plt.show()

# play snares at times of snaps
snare = pygame.mixer.Sound("Sounds/snare.wav")  # set snare sound
print('Time instances of snaps: ' + str(onsets))

delays = np.array(onsets[0])
for counter, value in enumerate(onsets):
    if counter > 0:
        delays = np.append(delays, value-onsets[counter-1])
    if counter == len(onsets)-1:
        delays = np.append(delays, record_time - onsets[counter])
print('Delay times: ' + str(delays))

for interval in delays:
    if interval == delays[-1]:
        break
    time.sleep(interval)
    snare.play()
time.sleep(snare.get_length())  # last sleep is needed to keep the program running so it is not shut down until sound is playing
