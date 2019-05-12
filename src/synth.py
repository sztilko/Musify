import librosa
import numpy as np
import math
import pygame
from pygame import midi
import time
from threading import Thread


class Synth(Thread):
    def __init__(self, signal, sampling_rate, recording_time, with_instrument=0):
        """
        Synthesizer class
        Transforms the whistle audio signal into MIDI format, and plays back in chosen instrument

        :param signal: whistle audio signal
        :param sampling_rate: the sampling rate of the recording in Hz
        :param recording_time: recording duration
        :param with_instrument: number of the musical instrument (between 0 and 127)
        """
        Thread.__init__(self)
        print()
        print("------------------------")
        print("Initializing Synth class!")

        self.signal = np.squeeze(signal)
        self.fs = sampling_rate
        self.dur = recording_time
        self.instrument_num = with_instrument

        # threshold filter
        self.th_filt = None
        self.__calc_th_filt()

        # pitch tracking
        self.pitches = None
        self.__pitch_tracking()

        # filtered MIDI
        self.filtered_midi = None
        self.small_th = None
        self.__filter_and_round()

        # MIDI data for MIDI player
        self.midi_input = None
        self.__create_midi_data()

        # For playing midi synth
        pygame.init()
        midi.init()
        self.device = midi.get_default_output_id()
        print("Default MIDI device found: " + str(midi.get_default_output_id()))

    def __create_midi_data(self):
        diff_mask = np.array([1, 1, -1, -1])
        note_change = np.convolve(self.filtered_midi, diff_mask, 'same')  # detect note changes with diff filter
        note_on = np.amax(note_change) * 0.8 < note_change
        note_off = np.min(note_change) * 0.8 < note_change
        event_map = note_on.astype(int) - (note_off - 1)
        events = np.where(event_map == 1)[0]
        sleep_times = np.append(events, len(event_map) - 1) - np.insert(events, 0, 0)
        events = np.insert(events, 0, 0)  # treat start as an event

        # create the input for MIDIPlayer
        # midi input format :[MIDI notes, velocities, time of play]
        self.midi_input = np.asarray([self.filtered_midi[events].astype(int), self.small_th[events].astype(int) * 127,
                                      sleep_times])

    def __filter_and_round(self):
        scale_factor = math.ceil(self.th_filt.shape[0] / self.pitches.shape[0])
        small_th = self.th_filt[0:-1:scale_factor]  # small size binary threshold data
        filtered_midi = small_th * self.pitches  # thresholded midi data
        filtered_midi[np.isnan(filtered_midi)] = 0  # replace nans with 0s
        self.filtered_midi = filtered_midi.round()  # round to integers
        self.small_th = small_th

    def __calc_th_filt(self):
        signal_filt = self.signal ** 2
        window = 200
        avg_mask = np.ones(window) / window
        signal_filt = np.convolve(signal_filt, avg_mask, 'same')  # moving_avg signal for thresholding
        self.th_filt = signal_filt > np.amax(signal_filt) * 0.005

    def __pitch_tracking(self):
        pitches, magnitudes = librosa.core.piptrack(y=self.signal, sr=self.fs, fmin=500, fmax=5000)

        idxs = magnitudes.argmax(axis=0)
        p = [pitches[idx, t] for t, idx in enumerate(idxs)]
        p = np.array(p)
        np.place(p, p == 0, 1)  # handle zeros in frequency array (log problem)
        self.pitches = librosa.core.hz_to_midi(p)

    def __play_midi(self, midi_input, duration, with_instrument=0):
        """
        Plays the given MIDI sequence

        :param midi_input: list of midi notes to play
        :param duration: the duration of the recording in sec
        :param with_instrument: the number of the instrument
        :return: plays the midi notes on given instrument
        """

        output = midi.Output(self.device)
        output.set_instrument(with_instrument)
        scale_factor = duration/np.sum(midi_input[2][:])

        for step in range(midi_input.shape[1]):
            note = midi_input[0][step]
            velocity = midi_input[1][step]
            sleep_time = midi_input[2][step]
            if note == 0:
                output.note_on(note, 0)
                time.sleep(sleep_time * scale_factor)
            else:
                output.note_on(note, velocity)
                time.sleep(sleep_time*scale_factor)
                output.note_off(note)
        output.close()

    def run(self):
        print("Playing Synth...")
        self.__play_midi(self.midi_input, self.dur, self.instrument_num)
        print("Synth finished!")

