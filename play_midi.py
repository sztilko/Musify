import time
import numpy as np
import pygame
from pygame import midi


class MIDIPlayer:
    def __init__(self):
        pygame.init()
        midi.init()
        self.device = midi.get_default_output_id()
        print("Default MIDI device found: " + str(midi.get_default_output_id()))

    @staticmethod
    def list_all_midi_devices():
        for x in range(0, pygame.midi.get_count()):
            print(pygame.midi.get_device_info(x))

    def play_midi_sequence(self, midi_input, duration, with_instrument=0):
        """
        Plays the given MIDI sequence

        :param midi_seq: list of midi notes to play
        :param duration: the duration of the recording in sec
        :param with_instrument: the number of the instrument
        :return: plays the midi notes on given instrument
        """

        output = midi.Output(self.device)
        output.set_instrument(with_instrument)
        scale_factor=duration/np.sum(midi_input[2][:])

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


