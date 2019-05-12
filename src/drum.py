import numpy as np
import librosa
import pygame
import time
from threading import Thread


class Drum(Thread):
    def __init__(self, signal, sampling_rate, recording_time):
        Thread.__init__(self)
        print()
        print("------------------------")
        print("Initializing Drum class!")

        self.signal = np.squeeze(signal)
        self.fs = sampling_rate
        self.dur = recording_time
        self.delays = None                                   # calculates self.__process_signal() method

        # play snares at times of snaps
        self.snare = pygame.mixer.Sound("Sounds/snare.wav")  # set snare sound

        self.__process_signal()

    def __process_signal(self):
        # extract onset peaks from signal
        onsets = librosa.onset.onset_detect(self.signal, self.fs, units='time')

        delays = np.array(onsets[0])
        for counter, value in enumerate(onsets):
            if counter > 0:
                delays = np.append(delays, value - onsets[counter - 1])
            if counter == len(onsets) - 1:
                delays = np.append(delays, self.dur - onsets[counter])

        self.delays = delays

    def run(self):
        for interval in self.delays:
            if interval == self.delays[-1]:
                break
            time.sleep(interval)
            self.snare.play()
        time.sleep(self.snare.get_length())
