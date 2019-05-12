from src.rec import Recording
from src.drum import Drum

fs = 41000
dur = 5

rec = Recording(fs, dur)
rec.start()
rec.play_back_snaps()
rec.play_back_whistle()

drum = Drum(rec.drum_signal, fs, dur)

if __name__ == "__main__":
    drum.start()
