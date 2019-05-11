import pygame
from pygame import midi
import time


class MIDIPlayer:
    def __init__(self):
        pygame.init()
        midi.init()
        device = midi.get_default_output_id()
        self.player = midi.Output(device)
        print("Default MIDI device found: " + str(midi.get_default_output_id()))

    def __del__(self):
        self.player.close()
        del self.player
        pygame.midi.quit()

    @staticmethod
    def list_all_midi_devices():
        for x in range(0, pygame.midi.get_count()):
            print(pygame.midi.get_device_info(x))

    def play_midi_sequency(self, midi_seq, duration, with_instrument=0):
        """
        Plays the given MIDI sequence

        :param midi_seq: list of midi notes to play
        :param duration: the duration of the recording in sec
        :param with_instrument: the number of the instrument
        :return: plays the midi notes on given instrument
        """

        n = len(midi_seq)
        step = duration/n   # duration of a note

        self.player.set_instrument(with_instrument)

        for idx, note in enumerate(midi_seq):
            self.player.note_on(note, 127)
            time.sleep(step)

            if idx+1 < n:
                if midi_seq[idx+1] == note:
                    pass  # If the next note is the same, keep holding it down
                else:
                    self.player.note_off(note, 127)
            else:
                self.player.note_off(note, 127)


# pygame.mixer.music.load("gf.mid")
# pygame.mixer.music.play()

