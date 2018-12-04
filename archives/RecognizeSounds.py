# sound recognition
import aubio

import numpy as np
import wave

track = [[('E5', (201, 354)), (1, (201, 354)), ('C5', (373, 369)), (1, (373, 369))], [('D5', (566, 361)), (1, (566, 361)), ('B4', (743, 377)), (1, (743, 377))], [('C5', (942, 370)), ('B4', (1041, 379)), ('A4', (1143, 385)), ('B4', (1242, 378))], [('G4', (1364, 391)), (1, (1364, 391)), (1, (1364, 391)), ('G4', (1607, 392))], [('A4', (162, 654)), (1, (162, 654)), ('C5', (331, 638)), (1, (331, 638))], [('A4', (523, 654)), ('A5', (623, 601)), ('G5', (725, 608)), ('F5', (826, 616))], [('E5', (948, 624)), ('F5', (1047, 617)), ('G5', (1148, 608)), ('E5', (1247, 624))], [('D5', (1367, 630)), (1, (1367, 630)), (1, (1367, 630)), ('G4', (1608, 662))], [('E5', (162, 892)), (1, (162, 892)), ('C5', (337, 908)), (1, (337, 908))], [('D5', (536, 899)), (1, (536, 899)), ('B4', (718, 915)), (1, (718, 915))], [('C5', (922, 908)), ('B4', (1024, 916)), ('A4', (1128, 923)), ('B4', (1230, 916))], [('G4', (1354, 930)), (1, (1354, 930)), (1, (1354, 930)), ('G4', (1603, 931))], [('A4', (162, 1192)), (1, (162, 1192)), ('C5', (328, 1177)), (1, (328, 1177))], [('A4', (517, 1192)), ('A5', (615, 1140)), ('G5', (716, 1146)), ('F5', (815, 1155))], [('G5', (936, 1147)), ('A5', (1040, 1140)), ('B5', (1145, 1131)), ('C6', (1248, 1124))], [('D6', (1373, 1115)), (1, (1373, 1115)), (1, (1373, 1115)), ('D5', (1609, 1171))], [('C5', (161, 1446)), (1, (161, 1446)), (1, (161, 1446)), ('E5', (408, 1431))], [(0, (549, 1453)), (0, (549, 1453)), ('C5', (741, 1446)), (1, (741, 1446))], [('B4', (951, 1453)), (1, (951, 1453)), (1, (951, 1453)), ('D5', (1204, 1439))], [(0, (1349, 1453)), (0, (1349, 1453)), ('B4', (1542, 1453)), (1, (1542, 1453))], [('A4', (161, 1730)), (1, (161, 1730)), (1, (161, 1730)), ('C5', (395, 1716))], [(0, (530, 1722)), (0, (530, 1722)), ('A4', (711, 1731)), (1, (711, 1731))], [('B4', (911, 1724)), ('G4', (1010, 1739)), ('A4', (1111, 1731)), ('B4', (1210, 1724))], [('C5', (1331, 1716)), ('D5', (1430, 1709)), ('E5', (1531, 1700)), ('D5', (1630, 1709))], [('C5', (161, 1984)), (1, (161, 1984)), (1, (161, 1984)), ('E5', (408, 1969))], [(0, (549, 1992)), (0, (549, 1992)), ('C5', (741, 1985)), (1, (741, 1985))], [('B4', (951, 1991)), (1, (951, 1991)), (1, (951, 1991)), ('D5', (1204, 1978))], [(0, (1350, 1992)), (0, (1350, 1992)), ('B4', (1542, 1992)), (1, (1542, 1992))], [('A4', (161, 2269)), (1, (161, 2269)), (1, (161, 2269)), ('C5', (396, 2254))], [(0, (531, 2261)), (0, (531, 2261)), ('A4', (715, 2269)), (1, (715, 2269))], [('B4', (916, 2261)), (1, (916, 2261)), ('D5', (1084, 2247)), ('E5', (1189, 2240))], [('D5', (1314, 2247)), ('C5', (1415, 2254)), ('B4', (1515, 2262)), ('G4', (1616, 2277))]]

note = aubio.source('./Sounds/Notes/A5.wav')
note
fftSize = 4096
pitch = aubio.pitch('default',
                    fftSize,
                    note.hop_size,
                    note.samplerate)
pitch.set_unit('freq') # sets to hertz
pitch.set_tolerance(0.8)

#audioBuffer = note.read(note.hop_size)
audioBuffer = 1024

signal = np.fromstring(audioBuffer, dtype=np.float32)

pitchAct = pitch_o(signal)[0]
confidence = pitch_o.get_confidence()
#note = aubio.freq2note(pitch)
#print(pitch)
if 10 <= pitchAct <= 10000:
    note = aubio.freq2note(pitchAct)
    print(note)






# converts frequency to note, now need to detect frequency
freqDetect = 441.4
playedNote = aubio.freq2note(freqDetect)
print(playedNote)

sound.record('voice.wav') #just creates the voice file
#wf = wave.open(outputFile, 'wb')
a = wave.open('voice.wav', 'wb')

if a != None:
    a.read(1024)
    audiobuffer = a.read(buffer_size)
    print('audiobuffer is', audiobuffer)
    signal = np.fromstring(audiobuffer, dtype=np.float32)
    pitch = pitch_o(signal)[0]
    confidence = pitch_o.get_confidence()
    #note = aubio.freq2note(pitch)
    #print(pitch)
    if 10 <= pitch <= 10000:
        note = aubio.freq2note(pitch)
        print(note)
    

#aubio.source('voice.wav')
# setup pitch
tolerance = 0.8
buffer_size = 1024 # default value as set in sounds
win_s = 4096 # fft size
hop_s = buffer_size # hop size
pitch_o = aubio.pitch("default", win_s, hop_s, samplerate)
pitch_o.set_unit("freq")
pitch_o.set_tolerance(tolerance)

while True:
    try:
        audiobuffer = a.read(buffer_size)
        print(audiobuffer)
        signal = np.fromstring(audiobuffer, dtype=np.float32)
        pitch = pitch_o(signal)[0]
        confidence = pitch_o.get_confidence()
        #note = aubio.freq2note(pitch)
        #print(pitch)
        if 10 <= pitch <= 10000:
            note = aubio.freq2note(pitch)
            print(note)
        #print("{} / {}".format(pitch,confidence))

        if outputsink:
            outputsink(signal, len(signal))

        if record_duration:
            total_frames += len(signal)
            if record_duration * samplerate < total_frames:
                break
    except KeyboardInterrupt:
        print("*** Ctrl+C pressed, exiting")
        break
'''
