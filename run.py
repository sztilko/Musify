from src.rec import Recording

rec = Recording(41000, 5)
rec.start()
rec.play_back_snaps()
rec.play_back_whistle()