# Musify
Project scope:
The aim is to build a Python based application, that records input sound samples from the user and converts them to set of instrument sounds. For example the user records a pattern of snaps which then converts to snare drum sounds.
The user should be able to give monophonic melodic input such as whistle, which as well should be converted to a selected instrument sound eg. violin.
The first version can handle 2 types of inputs:
- whistle for melodies
- snaps or claps for drums

The application works in the following way:
1. The user starts recording a snap pattern to use later as a rhythm base.
2. When the recording phase is over, the recorded sample is played back so the user can whistle a melody to it.
3. The raw recordings are converted to the selected insturments and played back.

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
