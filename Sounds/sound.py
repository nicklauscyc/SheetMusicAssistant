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

# for note detection
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
############################# Detect Note #################################
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
    fftSize = 4096 # fft size
    pitchBase = aubio.pitch("default", fftSize, hop_s, RATE)
    pitchBase.set_unit("freq")
    pitchBase.set_tolerance(tolerance)

    audioBuffer = stream.read(CHUNK)
    signal = np.fromstring(audioBuffer, dtype=np.float32)
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

    return note

###########################################################################
######################### Recording a WAV file ############################
###########################################################################
def record(outputFile):
    CHUNK = 1024 #measured in bytes looks like its the buffer size
    FORMAT = pyaudio.paFloat32
    CHANNELS = 2 #stereo
    RATE = 44100 #common sampling frequency
    RECORD_SECONDS = 1 #change this record for longer or shorter!

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* recording")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(outputFile, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()


def listen():
    for i in range(10000):
        detectNote()
