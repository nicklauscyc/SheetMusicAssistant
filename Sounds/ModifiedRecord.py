# sounds file that enables play back


#Code taken from CMU 112 website on pyaudio
#Code modified from https://people.csail.mit.edu/hubert/pyaudio/

###########################################################################
######################### Playing a WAV file ##############################
###########################################################################


"""PyAudio Example: Play a WAVE file."""

import pyaudio
import wave
from array import array
from struct import pack

import aubio
import numpy as np

def play(file):
    CHUNK = 1024 #measured in bytes

    wf = wave.open(file, 'rb')

    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    data = wf.readframes(CHUNK)

    while len(data) > 0:
        stream.write(data)
        data = wf.readframes(CHUNK)

    stream.stop_stream()
    stream.close()

    p.terminate()

###########################################################################
######################### Recording a WAV file ############################
###########################################################################
def detectNote():
    # modified version of record function taken from 112 website
    CHUNK = 1024 #measured in bytes looks like its the buffer size
    FORMAT = pyaudio.paFloat32
    CHANNELS = 1 #changed from og stereo
    RATE = 44100 #common sampling frequency
    RECORD_SECONDS = 0.1 # in seconds, human reaction time is .17s for audio

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    # setup pitch
    tolerance = 0.8
    hop_s = CHUNK # hop size
    win_s = 4096 # fft size
    pitchBase = aubio.pitch("default", win_s, hop_s, RATE)
    pitchBase.set_unit("freq")
    pitchBase.set_tolerance(tolerance)

    audiobuffer = stream.read(CHUNK)
    signal = np.fromstring(audiobuffer, dtype=np.float32)
    pitch = pitchBase(signal)[0]
    confidence = pitchBase.get_confidence()

    # ensures that only audible notes are counted as pitch
    if 10 <= pitch <= 10000:
        
        note = aubio.freq2note(pitch)
    else:
        note = ''
        
    stream.stop_stream()
    stream.close()
    p.terminate()

    print(note)
    return note


