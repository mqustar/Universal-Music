import sys
from aubio import source, notes



filename = 'test.mp3'

downsample = 1
samplerate = 44100 // downsample
if len( sys.argv ) > 2: samplerate = int(sys.argv[2])

win_s = 512 // downsample # fft size
hop_s = 256 // downsample # hop size

s = source(filename, samplerate, hop_s)
samplerate = s.samplerate

tolerance = 0.
lol = 0
length = 0
notes_o = notes("default", win_s, hop_s, samplerate)

print("%8s" % "time","[ start","vel","last ]")

# total number of frames read
total_frames = 0
while True:
    samples, read = s()
    new_note = notes_o(samples)
    if (new_note[0] != 0):
        lol += 1
        length += new_note[2]
    total_frames += read
    if read < hop_s: break
print((length/lol)*(4/3))
