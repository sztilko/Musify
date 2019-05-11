import pygame
from pygame import midi
import time
pygame.init()
midi.init()

# list all midi devices
for x in range(0, pygame.midi.get_count()):
    print(pygame.midi.get_device_info(x))


device = midi.get_default_output_id()
print(midi.get_default_output_id())
output = midi.Output(device)
output.set_instrument(device)
output.note_on(64, 127)
time.sleep(2)
#output.note_off(64)
output.close()

# pygame.mixer.music.load("gf.mid")
# pygame.mixer.music.play()

