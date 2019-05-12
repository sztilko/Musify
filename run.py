from src.rec import Recording
from src.drum import Drum
from src.synth import Synth

fs = 41000
dur = 5

rec = Recording(fs, dur)
rec.start()
rec.play_back_snaps()
rec.play_back_whistle()

drum = Drum(signal=rec.drum_signal, sampling_rate=fs, recording_time=dur)
synth = Synth(signal=rec.whistle_signal, sampling_rate=fs, recording_time=dur, with_instrument=32)

if __name__ == "__main__":
    drum.start()
    synth.start()

drum.join()
synth.join()
