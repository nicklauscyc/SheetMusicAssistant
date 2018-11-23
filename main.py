# main file

from Sounds import sounds
from tkinter import *
import threading
from threading import Thread
from image_util import *
# edited starter code from 112 website

import time

def init(data):
    # load data.xyz as appropriate
    
    data.whiteKeys = []
    data.blackKeys = []
    
    data.wKeyWidth = 50
    data.wKeyHeight = 100
    
    data.bKeyWidth = 30
    data.bKeyHeight = 50

    
    data.score = PhotoImage(file='semibreve.gif')
    data.sWidth = data.score.width()
    data.sHeight = data.score.height()

def generateKeys(data):

    # generate white keys
    startX = (data.width/2) - data.wKeyWidth*4
    keyMargin = 10
    startY = data.height - data.wKeyHeight - keyMargin
    for i in range(8):
        wkeyCorner = (startX + i*data.wKeyWidth, startY)
        
        data.whiteKeys.append(wkeyCorner)

def playNote(filename):
    start = time.time()
    

    # try to change it to play for shorter periods of time
    sounds.play('./'+ filename)




#playNote('Piano.mf.A4.wav')
#sounds.play('./Piano.mf.A4.wav')
#sounds.play('./backgroundMusic.wav')


'A4.wav'
'Ab4.wav'
'B4.wav'
'Bb4.wav'
'C4.wav'
'C5.wav'
'D4.wav'
'Db4.wav'
'E4.wav'
'Eb4.wav'
'F4.wav'
'G4.wav'
'Gb4.wav'

def pianoPressed(event, data):
    pass

    
def mousePressed(event, data):
    # use event.x and event.y
    pass

def keyPressed(event, data):
    # use event.char and event.keysym
    if event.keysym == 'a':
        Thread(target=playNote, args=('Octave/C4.wav',)).start()
    if event.keysym == 's':
        Thread(target=playNote, args=('Octave/D4.wav',)).start()
    if event.keysym == 'd':
        Thread(target=playNote, args=('Octave/E4.wav',)).start()
    if event.keysym == 'f':
        Thread(target=playNote, args=('Octave/F4.wav',)).start()
    if event.keysym == 'g':
        Thread(target=playNote, args=('Octave/G4.wav',)).start()
    if event.keysym == 'h':
        Thread(target=playNote, args=('Octave/A4.wav',)).start()
    if event.keysym == 'j':
        Thread(target=playNote, args=('Octave/B4.wav',)).start()
    if event.keysym == 'k':
        Thread(target=playNote, args=('Octave/C5.wav',)).start()
    if event.keysym == 'w':
        Thread(target=playNote, args=('Octave/Db4.wav',)).start()
    if event.keysym == 'e':
        Thread(target=playNote, args=('Octave/Eb4.wav',)).start()
    if event.keysym == 't':
        Thread(target=playNote, args=('Octave/Gb4.wav',)).start()
    if event.keysym == 'y':
        Thread(target=playNote, args=('Octave/Ab4.wav',)).start()
    if event.keysym == 'u':
        Thread(target=playNote, args=('Octave/Bb4.wav',)).start()
        
        
    

def timerFired(data):
    pass

def drawWhiteKeys(canvas, data):
    for key in data.whiteKeys:
        canvas.create_rectangle(key, key[0] + data.wKeyWidth,
                                key[1] + data.wKeyHeight, fill='white',)

def drawBlackKeys(canvas, data):
    pass
    
def drawKeyboard(canvas, data):
    
    pass
def redrawAll(canvas, data):
    # draw in canvas
    drawKeyboard(canvas, data)
    
    canvas.create_image(data.width/2, 10,
                        image=data.score,anchor='n')
    
    canvas.create_text(.5*data.width, .9*data.height, fill='white',
                       text='Press keys: a,s,d,f,g,h,j,k,w,e,t,y,u to play notes')

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
    data.width = width
    data.height = height
    data.timerDelay = 10 # milliseconds
    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(1000, 1000)
