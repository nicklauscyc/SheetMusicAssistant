# Playback the given score
# triggered from keypressed in main
# code modified from CMU 112 website
from tkinter import *
from threading import Thread
from Sounds import sounds

# Updated Animation Starter Code from 112 website


####################################
# customize these functions
####################################
def init(data):
    # load data.xyz as appropriate

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

def mousePressed(event, data):
    # use event.x and event.y
    pass

def playNote(filename):
    # try to change it to play for shorter periods of time
    sounds.play('./'+ filename)
    
def keyPressed(event, data):
    pass
        
def playBack(data):
    data.playTime += data.timerDelay
    
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
            
def redrawAll(canvas, data):
    pass

####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='black', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()

    # adding properties to data
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window
    
    init(data) # allows for the rest of data properties to be initialized 
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events

    # the click of a mouse lambda function
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    
    print("bye!")

run(1900, 1000)
