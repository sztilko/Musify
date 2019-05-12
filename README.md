# Musify
Project scope:
The aim is to build a Python based application, that records input sound samples from the user and converts them to set of instrument sounds. For example the user records a pattern of snaps which then converts to snare drum sounds.
The user should be able to give monophonic melodic input such as whistle, which as well should be converted to a selected instrument sound eg. violin.
The application should record the inputs sequentially, building up a song layer by layer.
The first version should be able to process 3 types inputs:
- whistle
- snaps
- claps

The application should work in the following way:
1. The user starts recording a max. 1 minute long sample.
2. When the recording phase is over, the recorded sample is played back on a selected instrument.
3. The following recording sessions should go in parallel with the playback of the yet recorded samples.
4. The final samples should be exported in a common audio format.

## Required packages
- numpy
- SoundDevice (for audio recording)
- pyGame (for midi playback)
- librosa (for audio processing)

_Creating virtual environment for running (conda)_:

`conda create -n musify python=3.7` \
`conda activate musify` \
`conda install numpy` \
`pip install sounddevice` \
`pip install pygame` \
`conda install -c conda-forge librosa`