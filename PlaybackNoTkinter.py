# Playback the given score
# triggered from keypressed in main
# code modified from CMU 112 website
from tkinter import *
from threading import Thread
from Sounds import sounds

def init(data):
    # initialize all necessary data for playing back

    data.track = [[1,1,1,1], [1,1,1,1], [1,0,1,0], [1,0,1,0],
                  [1,1,1,1], [1,1,1,1], [0,1,0,1], [0,1,0,1]]
    data.lastBar = len(data.track) - 1
    data.bar = 0
    data.lastNote = len(data.track[0]) - 1
    data.note = 0

    data.trackPosition = (data.bar, data.note)

    data.time = 0
    data.tempo = 500
    data.end = False

def playNote(filename):
    # try to change it to play for shorter periods of time
    sounds.play('./'+ filename)
    
def timerFired(data):
    if data.end == False:
        data.time += data.timerDelay
            
        if data.time % data.tempo == 0 and data.time > 0:
            print (data.trackPosition)
            bar, note = data.trackPosition
            if data.track[bar][note] == 1:
                Thread(target=playNote, args=('Octave/C4.wav',)).start()

            # checking for bar ends
            if bar != data.lastBar:
                if note != data.lastNote:
                    data.note += 1
                    data.trackPosition = (bar, data.note)

                else:
                    data.bar += 1
                    data.note = 0
                    data.trackPosition = (data.bar, data.note)
                    data.lastNote = len(data.track[data.bar]) - 1
            else:
                if note != data.lastNote:
                    data.note += 1
                    data.trackPosition = (bar, data.note)

                else: # last note, last bar
                    data.end = True
                    # find a way to terminate

import time
def run():
    # Set up data and call init
    class Struct(object): pass
    data = Struct()

    # adding properties to data
    data.timerDelay = 100 # milliseconds
    init(data) # allows for the rest of data properties to be initialized 
    # create the root and the canvas

    start = time.time()*1000 # in milliseconds

    while data.end == False:
        present = time.time()*1000
        if (present - start) % data.timerDelay == 0:
            timerFired(data)

    # and launch the app
    # root.mainloop()  # blocks until window is closed
    
    print("bye!")

run()
