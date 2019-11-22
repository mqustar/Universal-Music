

import sys
import time
import pyaudio
import aubio
from aubio import source, notes
import numpy as np

win_s = 512          # fft size
hop_s = win_s //  2     # hop size

# parse command line arguments


filename = 'test3.mp3'

samplerate = 0
if len( sys.argv ) > 2: samplerate = int(sys.argv[2])

# create aubio source
a_source = aubio.source(filename, samplerate, hop_s)
samplerate = a_source.samplerate

# create aubio tempo detection
a_tempo = aubio.tempo("default", win_s, hop_s, samplerate)
notes_o = aubio.notes("default", win_s, hop_s, samplerate)



# create a simple click sound
click = 0.7 * np.sin(2. * np.pi * np.arange(hop_s) / hop_s * samplerate / 3000.)

# pyaudio callback
def pyaudio_callback(_in_data, _frame_count, _time_info, _status):
    samples, read = a_source()
    is_beat = a_tempo(samples)
    new_note = notes_o(samples)
    if (new_note[0] != 0 and new_note[2] != 0):

        pass
    if is_beat:
       samples += click
    audiobuf = samples.tobytes()
    if read < hop_s:
        return (audiobuf, pyaudio.paComplete)
    return (audiobuf, pyaudio.paContinue)

# create pyaudio stream with frames_per_buffer=hop_s and format=paFloat32
p = pyaudio.PyAudio()
pyaudio_format = pyaudio.paFloat32
frames_per_buffer = hop_s
n_channels = 1
stream = p.open(format=pyaudio_format, channels=n_channels, rate=samplerate,
        output=True, frames_per_buffer=frames_per_buffer,
        stream_callback=pyaudio_callback)

# start pyaudio stream
stream.start_stream()

