
################################################################################
########################## SheetMusicAssistant #################################

# Nicklaus Choo
'''
main file is modified from starter animation
code taken from CMU 112 website
'''

############################################################
# All Imports
############################################################

####################################
# Imports from Python modules
####################################

# use stop threading

# core animation
from tkinter import *
from threading import Thread
# used in ImageDetect.py
import cv2
import numpy as np
# used in PDF Convert
import os
from wand.image import Image
from wand.color import Color

####################################
# Imports from Custom Directories
####################################

# Image Recognition
from ImageRecognition import ImageDetect
from ImageRecognition import PDFConvert
# Sound capabilities
from Sounds import sound

####################################
# Application UI Objects
####################################


def color(red, green, blue):
    # adapted from 112 website
    return "#%02x%02x%02x" % (red, green, blue)
   
class Screen(object):
    # the main interface screen with all the stylistic attributes of
    # the application

    def __init__(self):
        pass
        

    def __repr__(self):

        return ('A Screen Object')
    
    @ staticmethod
    def drawMenuBar(canvas, data):
        stdColor = color(80,80,80)
        mseColor = color(200,200,200)
        highlight = color(0,0,0)

        # draw buttons first, all from data, the exact same buttons

        data.openPDFBtn.draw(canvas)
        data.listenBtn.draw(canvas)
        data.playBtn.draw(canvas)
        intervals = data.width/3
        canvas.create_rectangle(0,100, data.width, 110,
                                fill=highlight, width=0)
        
class FileNavigation(Screen):
    # the interface screen when looking for pdf to convert

    def drawScoreOptions(self, canvas, data):
        

        # dictionary containing file name as key, 4-tuple as coordinates
        data.fileList = {} # always clears the dictionary
        pdfNum = 1
        canvas.create_rectangle(0, 110,
                              data.width/3,data.height,
                              fill=color(0,0,0),
                              width=0)
                
        canvas.create_rectangle(0, 110, data.width/3, data.height,
                                fill=color(0,0,0),
                                width=0)
        canvas.create_text(0 + 10, 110 + 40,
                           anchor='w',
                           text='MusicScores Folder',
                           font='Calibri 15',
                           fill=color(200,200,200))

        for item in range(len(data.dirItems)):
            fileName = data.dirItems[item]

            if fileName[-4:]=='.pdf':
                data.fileList[fileName] = (0, 110 + pdfNum*80,
                                           data.width/3, 110 + (pdfNum+1)*80)
                
                canvas.create_rectangle(data.fileList[fileName],
                                        fill=color(0,0,0),
                                        activefill=color(80,80,80),
                                        width=0)
                canvas.create_text(0 + 10, 110 + pdfNum*80 + 40,
                                   anchor='w',
                                   text=fileName,
                                   font='Calibri 11',
                                   fill=color(200,200,200))
                pdfNum += 1
                                                        
    def scoreSelected(self, event, data):
        # don't think this is going to draw anything in the end.
        if data.activeScreen == 'openPDF':
            for file in data.fileList:
                
                # list of all file coordinates
                x1, y1, x2, y2 = data.fileList[file]

                if x1 < event.x < x2 and y1 < event.y < y2:
                    # score is selected
                
                    # fire up loading screen
                    data.loading = True
                    print('data.loading set to True')
                    data.file2Load = file
                    

                    
##                    ###################
##                    
##                    PDFConvert.toGIF('./MusicScores/' + file)
##                    PDFConvert.toPNG('./MusicScores/' + file)
##                    data.activeScreen = 'main'
##
##            
##                    
##                    data.track = []
##                    data.scoreFile = file
##                    data.score = PhotoImage(file='./MusicScores/'+ \
##                                            file[:-4]+'.gif')
##                    tupData = ImageDetect.convert2playable('./MusicScores/'+\
##                                                      data.scoreFile[:-4]+\
##                                                              '.png')
##                    data.track, data.staves = tupData
##                    
##                    
##                        
##                    initForPlayBack(data) # initialize other variables for play
##
##                    
##                    initForListening(data) # initialize variables for listening
##                    data.loading = False
                    
class MusicDisplay(Screen):
    # the interface screen when listening to music

    def drawScore(self, canvas, data):
        # draws the score on the screen
        
    
        pass

class Button(object):

    def __init__(self, location, width=100, height=100,
                 text='button', baseColor=(80,80,80),
                 highlight=(0,0,0)):
        # location is the top left corner, a tuple
        self.location = location
        self.width = width
        self.height = height
        self.text = text
        self.font= 'Calibri 20'
        self.fontColor = color(200,200,200)
        self.baseColor = color(baseColor[0],baseColor[1],baseColor[2])
        self.highlight = color(highlight[0], highlight[1], highlight[2])
                 
        
    def draw(self, canvas):
        # draws the button on screen
        canvas.create_rectangle(self.location,
                                self.location[0]+self.width,
                                self.location[1]+self.height,
                                fill=self.baseColor, width=0,
                                activefill=self.highlight)
        canvas.create_text(self.location[0]+self.width/2,
                           self.location[1]+self.height/2,
                            text=self.text,
                            font=self.font,
                            fill=self.fontColor)

    def isClick(self, event, data):
        # check if button is clicked
        if self.location[0] < event.x < self.location[0] + self.width and \
           self.location[1] < event.y < self.location[1] + self.height:
            return True
        
####################################
# Core Animation Code
####################################

# Global Variables for Threading
loading = False


def initMenuBar(data):
    stdColor = color(80,80,80)
    mseColor = color(200,200,200)
    highlight = color(0,0,0)

    # draw buttons first
    intervals = data.width/3
    buttonText = ['Open PDF', 'Listen', 'Play']
    for i in range(3):
        
        if i == 0: 
            data.openPDFBtn = Button((i*intervals,0),width=intervals,
                                  height=100, text=buttonText[i])
        if i == 1:
            data.listenBtn = Button((i*intervals,0),width=intervals,
                                  height=100, text=buttonText[i])
        if i == 2:
            data.playBtn = Button((i*intervals,0),width=intervals,
                                  height=100, text=buttonText[i])
def initForFileNavigation(data):
    # when you first start, cwd should be the parent folder of main.py

    data.fileNav = FileNavigation()
    data.dirItems = os.listdir('./MusicScores')
    data.fileList = {}
       
def initForPlayBack(data):
    # initializes all required items for score playBack
    data.lastBar = len(data.track) - 1
    data.bar = 0
    data.lastNote = len(data.track[0]) - 1
    data.note = 0

    data.trackPosition = (data.bar, data.note)

    data.time = 0
    data.tempo = 300
    data.end = False
    data.Xposn = 0

    # how to tell if score is in scrolling state
    data.scrolling = False

    # initialize the score specific variables    
    data.numStaves = len(data.staves)
    
    data.scrollDist = []
    
    for stave in range(1,len(data.staves)):
        data.scrollDist.append(data.staves[stave][1]-\
                               data.staves[stave-1][1])
        
    data.scrollIndex = -1

    data.greenDotY = []
    for stave in data.staves:
        staveYcoordinate = stave[1]
        data.greenDotY.append(staveYcoordinate)
        
    data.greenDots = [] # list of tuples of circle centers
    data.greenDotYPosn = 0

    
def init(data):
    startDir = os.getcwd()

    initMenuBar(data)
    initForFileNavigation(data)

    # init for scoreDisplay
    data.score = ''
    data.scoreFile = '' # filename, .pdf
    data.track = []
    data.scrollScore = 0
    data.scoreTop = 110


    ''' all screens are 'main','openPDF','listen','play' '''
    data.activeScreen = 'main'

    # for load screen
    data.loading = False
        
def drawLoadScreen(canvas, data):
    # shows a loading screen for the duration that the image takes to
    # load
    loadWidth = 900
    loadHeight = 100
    
    canvas.create_rectangle(data.width/3*2 - loadWidth/2,
                            data.height/2 - loadHeight/2,
                            data.width/3*2 + loadWidth/2,
                            data.height/2 + loadHeight/2,
                            fill=color(80, 80, 80),
                            width=0)
    loadText = 'Loading all sheet music elements, approximately 20 s'
    canvas.create_text(data.width/3*2,
                       data.height/2,
                       text=loadText,
                       font='Calibri 11',
                       fill=color(200,200,200))

    print('load elements drawn')
    
def mousePressed(event, data):
    # use event.x and event y
    if data.openPDFBtn.isClick(event, data):
        print('pdf clicked')
        # changes screen
        if data.activeScreen != 'openPDF':
            # a pdf options opened first time clicked
            data.activeScreen = 'openPDF'
            
            
        else:
            data.activeScreen = 'main'
        
    elif data.listenBtn.isClick(event, data):
        print('listen clicked')
        # changes screen
        data.activeScreen = 'listen'
        
    elif data.playBtn.isClick(event, data):
        print('play clicked')
        # changes screen
        data.activeScreen = 'play'
        
    data.fileNav.scoreSelected(event,data) # checks for file nav

def keyPressed(event, data):
    # use event.char and event.keysym
    pass

def playNote(filename):
    # wrapper function from pyaudio's play function
    sound.play('./'+ filename)
    return None

def playBack(data):
    if data.end == False:
        data.time += data.timerDelay
            
        if data.time % data.tempo == 0 and data.time > 0:

            # going to have same time for all
            bar, note = data.trackPosition

            if data.track[bar][note][1][0] < data.Xposn:
                # time to scroll
                #data.scrollScore += 100
                # don't think I need
                pass
            data.Xposn = data.track[bar][note][1][0]
            data.Yposn = data.track[bar][note][1][1]
            musicNote = data.track[bar][note][0]
            currStave = data.greenDotYPosn
    
            
            
            noteName = './Sounds/Notes/' +\
                       str(musicNote) +\
                       '.wav'
            if type(musicNote) == str:
                # plays a note if it is a note
                Thread(target=playNote, args=(noteName,)).start()

                # append green dot centers tuples for drawing
                data.greenDots.append((data.Xposn,
                                      data.greenDotY[currStave]))
            
            # checking for bar ends
            if bar != data.lastBar:
                # last bar of the whole piece is data.lastBar
                if note != data.lastNote:
                    data.note += 1
                    data.trackPosition = (bar, data.note)

                else: # last note of the bar
                    oldBar = data.bar
                    data.bar += 1
                    nextBar = data.bar + 1
                    oldNote = data.note
                    data.note = 0
                    data.trackPosition = (data.bar, data.note)
                    data.lastNote = len(data.track[data.bar]) - 1

                    if bar + 1 != data.lastBar: 
                    # if next bar has first note x posn less than current
                    # bar bar x posn, data.scrolling = true
                    # currX is actually the immediately next note's x posn
                        currX = data.track[data.bar][data.note][1][0]
                        nextBarX = data.track[nextBar][data.note][1][0]

                        # the Ys are slightly different
                        oldX = data.track[oldBar][oldNote][1][0]

                        if oldX > currX:
                            # draw dots below
                            data.greenDotYPosn += 1

                        if currX > nextBarX:
                            data.scrolling = True
                            data.scrollIndex += 1

                        else:
                            data.scrolling = False

                        # checking to increase Y position for greendots
                    
                        
            else:
                if note != data.lastNote:
                    data.note += 1
                    data.trackPosition = (bar, data.note)

                else: # last note, last bar
                    data.end = True
                    data.activeScreen = 'main'
                    print('end')
                    
                    

def resetGreenDots(data):
    # resets all the green dots
    data.greenDots = []
    data.greenDotYPosn = 0

###########################################################################
######################## LISTENING CODE ###################################
###########################################################################
    
def initForListening(data):
    # initializes all required items for listening to score
    # data.track is already there whenever you want the app to
    # listen to you
    # initForListening is called when you press the listen button
    data.lastBar = len(data.track) - 1
    data.bar = 0
    data.lastNote = len(data.track[0]) - 1
    data.note = 0

    # starting track position
    data.trackPosition = (data.bar, data.note)

    data.time = 0

    # data.tempo is actually unnecessary 
    data.tempo = 300
    data.end = False
    data.Xposn = 0

    # how to tell if score is in scrolling state
    data.scrolling = False

    # initialize the score specific variables    
    data.numStaves = len(data.staves)
    
    data.scrollDist = []
    
    for stave in range(1,len(data.staves)):
        data.scrollDist.append(data.staves[stave][1]-\
                               data.staves[stave-1][1])
        
    data.scrollIndex = -1

    data.greenDotY = []
    for stave in data.staves:
        staveYcoordinate = stave[1]
        data.greenDotY.append(staveYcoordinate)
        
    data.greenDots = [] # list of tuples of circle centers
    data.greenDotYPosn = 0
                    
def listening(data):
    if data.end == False:
        data.time += data.timerDelay
            
        if data.time % data.tempo == 0 and data.time > 0:

            # going to have same time for all
            bar, note = data.trackPosition

            data.Xposn = data.track[bar][note][1][0]
            data.Yposn = data.track[bar][note][1][1]
            musicNote = data.track[bar][note][0]
            currStave = data.greenDotYPosn
    
            
            
            noteName = './Sounds/Notes/' +\
                       str(musicNote) +\
                       '.wav'
            if type(musicNote) == str:
                # plays a note if it is a note
                Thread(target=playNote, args=(noteName,)).start()

                # append green dot centers tuples for drawing
                data.greenDots.append((data.Xposn,
                                      data.greenDotY[currStave]))
            
            # checking for bar ends
            if bar != data.lastBar:
                # last bar of the whole piece is data.lastBar
                if note != data.lastNote:
                    data.note += 1
                    data.trackPosition = (bar, data.note)

                else: # last note of the bar
                    oldBar = data.bar
                    data.bar += 1
                    nextBar = data.bar + 1
                    oldNote = data.note
                    data.note = 0
                    data.trackPosition = (data.bar, data.note)
                    data.lastNote = len(data.track[data.bar]) - 1

                    if bar + 1 != data.lastBar: 
                    # if next bar has first note x posn less than current
                    # bar bar x posn, data.scrolling = true
                    # currX is actually the immediately next note's x posn
                        currX = data.track[data.bar][data.note][1][0]
                        nextBarX = data.track[nextBar][data.note][1][0]

                        # the Ys are slightly different
                        oldX = data.track[oldBar][oldNote][1][0]

                        if oldX > currX:
                            # draw dots below
                            data.greenDotYPosn += 1

                        if currX > nextBarX:
                            data.scrolling = True
                            data.scrollIndex += 1

                        else:
                            data.scrolling = False

                        # checking to increase Y position for greendots
                    
                        
            else:
                if note != data.lastNote:
                    data.note += 1
                    data.trackPosition = (bar, data.note)

                else: # last note, last bar
                    data.end = True
                    data.activeScreen = 'main'
                    print('end')

def loadScore(data):
    ###################
    file = data.file2Load         
    PDFConvert.toGIF('./MusicScores/' + file)
    PDFConvert.toPNG('./MusicScores/' + file)
    data.activeScreen = 'main'


    
    data.track = []
    data.scoreFile = file
    data.score = PhotoImage(file='./MusicScores/'+ \
                            file[:-4]+'.gif')
    tupData = ImageDetect.convert2playable('./MusicScores/'+\
                                      data.scoreFile[:-4]+\
                                              '.png')
    data.track, data.staves = tupData
    
    
        
    initForPlayBack(data) # initialize other variables for play

    
    initForListening(data) # initialize variables for listening
    data.loading = False

def timerFired(data):
    if data.activeScreen == 'play' and data.track != []:
        # keep calling playback until it ends
        playBack(data)
                # try to check for number of lines
        if data.scrolling == True:
            # scroll a specific amount as per each pair of stave dist
            scrollIncrement = data.scrollDist[data.scrollIndex]/\
                              (4*data.tempo/data.timerDelay)
            
            data.scrollScore += scrollIncrement
            
        if data.end == True:
            initForPlayBack(data)
            data.scrollScore = 0
            resetGreenDots(data)
            data.scrollIndex = -1
            
    elif data.activeScreen == 'listen' and data.track != []:
        # listen to whatever is going on
        
        listening(data)

        if data.end == True:
            initForListening(data)
            data.scrollScore = 0
            resetGreenDots(data)
            data.scrollIndex = -1

    elif data.activeScreen == 'openPDF':

        if data.loading == True:
            ###################
            loadScore(data)
            # loads the actual score after 100 millisecond of clicking

       
def drawGreenDots(canvas, data):
    # draws the green dots
    greenDots = data.greenDots
    
    for center in range(len(data.greenDots)):
        r = 10
        X, Y = greenDots[center]
        staveOffset = 290/3
        xOffset = 10

        canvas.create_oval(X - r + xOffset,
                           Y - r - data.scrollScore + staveOffset + \
                           data.scoreTop,
                           X + r + xOffset,
                           Y + r - data.scrollScore + staveOffset + \
                           data.scoreTop,
                           fill=color(0,255,0),
                           width=0)
        
def redrawAll(canvas, data):
    # draw in canvas
    print(data.activeScreen)

    if data.activeScreen == 'main':
        if data.score != '': # score is found
            canvas.create_image(data.width/2, data.scoreTop,
                                image=data.score,anchor='n')
        Screen.drawMenuBar(canvas, data)
        
    elif data.activeScreen == 'openPDF':
        if data.score != '': # score is found
            canvas.create_image(data.width/2, data.scoreTop,
                                image=data.score,anchor='n')
            
        data.fileNav.drawMenuBar(canvas, data)
        data.fileNav.drawScoreOptions(canvas, data)
        
    elif data.activeScreen == 'listen':
        # these two have to change because of scrolling
        if data.score != '': # score is found
            canvas.create_image(data.width/2, data.scoreTop - data.scrollScore,
                                image=data.score,anchor='n')
            drawGreenDots(canvas, data)
        MusicDisplay.drawMenuBar(canvas, data)
    elif data.activeScreen == 'play':
        if data.score != '': # score is found
            canvas.create_image(data.width/2, data.scoreTop - data.scrollScore,
                                image=data.score,anchor='n')
            drawGreenDots(canvas, data)
        MusicDisplay.drawMenuBar(canvas, data)
                                   
    
    if data.loading == True:
        drawLoadScreen(canvas, data)
        print('drawLoadScreen was fired in redrawAll')

####################################
# run function 
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
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
    data.timerDelay = 100 # milliseconds
    root = Tk()
    root.title("Sheet Music Assistant")
    root.resizable(width=False, height=False) # prevents resizing window
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events, after every mouse pressed or keypressed, canvas
    # is redrawn
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

#playBackList = ImageDetect.convert2playable('./MusicScores/Sample1.png', test=False)
run(1900, 1000)
