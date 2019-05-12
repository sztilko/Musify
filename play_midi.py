import pygame
from pygame import midi
import time


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

    def play_midi_sequence(self, midi_seq, duration, with_instrument=0):
        """
        Plays the given MIDI sequence

        :param midi_seq: list of midi notes to play
        :param duration: the duration of the recording in sec
        :param with_instrument: the number of the instrument
        :return: plays the midi notes on given instrument
        """

        n = len(midi_seq)
        step = duration/n   # duration of a note

        output = midi.Output( self.device )
        output.set_instrument(with_instrument)

        for idx, note in enumerate(midi_seq):
            output.note_on(int(note), 123)
            time.sleep(step)
        output.close()


