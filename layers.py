import sounddevice as sd
import matplotlib.pyplot as plt
import numpy as np
import time
import pygame

duration = 8
fs = 44100
sd.default.samplerate = fs
sd.default.channels = 1
sd.default.latency=('low')
pygame.mixer.init(buffer=1024)  # initialize pygame mixer
beep = pygame.mixer.Sound("Sounds/record_beep.wav")  # set beep sound
print(beep.get_length())
print("REC1")
t = np.linspace(0, duration, fs*duration)
for _ in range(4):
    beep.play()
    time.sleep(1)  # 3*times the length of the beep sound to prevent overlap with recording
layer = sd.rec(fs * duration, blocking=True)
# plt.plot(myrecording)
# plt.show()
i = 1
fig=plt.figure(figsize=(15, 5))
while True:
    i += 1
    plt.plot(t, layer)
    print("REC" + str(i) + 'starts in 4...')
    for i in range(4):
        beep.play()
        time.sleep(1)  # 3*times the length of the beep sound to prevent overlap with recording
    new_layer = sd.playrec(layer,blocking=True)
    #new_layer = sd.rec(fs * duration, blocking=True)
    layer = layer + np.roll(new_layer, -11000)  # experimental value to make recording overlap with playback
    plt.plot(t, new_layer)
    plt.plot(t, layer/10)
    break
sd.play(layer, blocking=True)

