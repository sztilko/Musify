import sounddevice as sd
import numpy as np
import time
import pygame


class Recording:
    def __init__(self, fs, duration):
        """
        This class is responsible for the recording.

        :param fs: sampling rate in Hz
        :param duration: the duration of the recording in seconds
        """
        self.dur = duration
        self.fs = fs
        self.t = np.linspace(0, duration, fs*duration)
        self.drum_signal = None
        self.whistle_signal = None

        # Set up recording device
        sd.default.samplerate = fs
        sd.default.channels = 1
        sd.default.latency = ('low')
        pygame.mixer.init(buffer=1024)  # initialize pygame mixer

        # Set up beep sound
        self.beep = pygame.mixer.Sound("Sounds/record_beep.wav")  # set beep sound

    def start(self):
        """
        Starts the recording session. First snaps then whistle

        :return: Creates audio signal for whistle and drum
        """
        self.__rec_drum()
        self.__rec_whistle_on_drum()

    def play_back_snaps(self):
        print("\nPlaying back the original audio signal of snaps...")
        sd.play(self.drum_signal, blocking=True)
        print("Done")

    def play_back_whistle(self):
        print("\nPlaying back the original audio signal of snaps...")
        sd.play(self.whistle_signal, blocking=True)
        print("Done")

    def __start_beep(self):
        input("Press ENTER to start recording!")
        for i in range(4):
            print(f"REC starts in {3-i} sec")
            self.beep.play()
            time.sleep(1)
        print("Recording...")

    def __end_beep(self):
        print("Recording finished!")
        self.beep.play()
        time.sleep(1)

    def __shift_signal(self):
        # shift whistle to overlap with snaps
        n = self.whistle_signal.size
        delay = -11000
        self.whistle_signal = np.roll(self.whistle_signal, delay)
        for x in range(n + delay, n):
            self.whistle_signal[x] = 0.

    def __rec_drum(self):
        print("First the snaps will be recorded!")
        self.__start_beep()
        self.drum_signal = sd.rec(self.fs * self.dur, blocking=True)
        self.__end_beep()

    def __rec_whistle_on_drum(self):
        print()
        print("-----------------------------------")
        print("Now we can record whistle on snaps!")
        self.__start_beep()
        self.whistle_signal = sd.playrec(self.drum_signal, blocking=True)
        self.__end_beep()

        self.__shift_signal()

