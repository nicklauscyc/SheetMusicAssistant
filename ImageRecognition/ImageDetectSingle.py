# test on how to read, display, and write images
import cv2
import numpy as np

def deduplicate(allPoints, bounds=10):
    # takes in allPoints list of tuples from locations(),
    # and returns a list of tuples that is deduplicated

    if allPoints == []: # object not found
        return []
    
    # sort the tuples based on x and y coordinates in
    # ascending order via a lambda function
    sortedPoints = sorted(allPoints,
                          key = lambda point: (point[0], point[1]))

    # dedupe sorted tuples in sortedPoints list
    deduped = [] # deduped list of tuples

    # add first tuple, because it's definitely not a duplicate
    deduped.append(sortedPoints[0]) 

    setY = set([])
    # add first element's range of y values into a set
    # to check for subsequent duplicates
    for i in range((2*bounds+1)+1):
        setY.add(sortedPoints[0][1] - bounds + i)

    # going through sortedPoints list to deduplicate tuples, fuzzily
    for i in range(1,len(sortedPoints)):

        point = sortedPoints[i]
        prev = sortedPoints[i-1]
        
        x, y = point[0], point[1]
        prevX, prevY = prev[0], prev[1]

        if not (prevX-bounds <= x <= prevX+bounds):
            deduped.append(point)
            setY = set([]) # reset set of y-value ranges
                
        else: # x is within the range of +- bounds
            # deciding whether to add the whole coordinate or not
            if y not in setY:
                deduped.append(point)
                
        for j in range((2*bounds+1)+1):
            # add the +- 2 range of values into the set
            fuzzY = y - bounds + j
            setY.add(fuzzY)
        
    return deduped


def locations(imageFile, scoreFile, musicType=('n',1,4),
              color=1, threshold=0.885):
    # returns the locations of the png 'imageFile' in the png 'score'
    # color=1 (color), color=0 (grayscale), color=-1 (unchanged)
    # threshold of 0.885 match has been empirically tested

    img = cv2.imread(imageFile, color)
    scoreImg = cv2.imread(scoreFile, color)

    # getting vertical center of img
    imgHeight = img.shape[0]
    imgCenY = imgHeight/2
    
    # using openCV to match img on scoreImg, match coordinates are top
    # left corner of each img template
    result = cv2.matchTemplate(scoreImg, img, cv2.TM_CCOEFF_NORMED)
    location = np.where(result >= threshold)

    # converting numpy array to list of tuples of note coordinates
    # X coordinate is the left edge of img, Y coordinate is center of img
    allPoints = []
    for point in zip(*location[::-1]):
        allPoints.append((point[0], int(point[1]+imgCenY), musicType))

    deduped = deduplicate(allPoints)
    
    return deduped # returns [] if nothing found

## Creating all list of tuples for each musical symbol


def resolveOverlap(symbol, overlap):
    # for resolving instances where 'falsePositive' show up.
    # example would be 'symbol' as minims and 'overlap' as dottedMinims.
    # both arguments are lists of 3-tuples eg. (1082, 700, ('n',1,4)) for
    # a quarter note or (1032, 321, ('end1')) for a single end bar line

    if symbol == []:
        return []

    if overlap == []: # no overlap
        return symbol
    
    # returns list of tuples that has false positives removed
    symbolType = symbol[0][2]
    allSymbols = overlap + symbol

    deduped = deduplicate(allSymbols)

    corrected = [] 
    for newSymbol in deduped:
        if newSymbol[2] == symbolType:
            corrected.append(newSymbol)
    return corrected


def createMusicTypes(scoreFile, template='./MusicNotesTemplate', test=False):
    # for each music symbol type, identify the locations on scoreFile
    # takes 13 seconds to run 

    # dictionary of all possible music types
    # singleEndS is for single stave music types
    musicTypes = {'quarter':('n',1,4),
                 'minim':('n',2,4),
                 'dottedMinim':('n',3,4),
                 'semibreve':('n',4,4),
                 'quarterRest':('r',1,4), 
                 'minimRest':('r',2,4),
                 'dottedMinimRest':('r',3,4),
                 'semibreveRest':('r',4,4),
                 'barLine':('barline',),
                 'singleEndS':('endS1',),
                 'doubleEndS':('endS2',),
                 'trebleClef':('treble',)
                 }
    
    ########################################################
    ## identifying all notes ###############################
    quarter = locations(template+'/quarter.png', scoreFile,
                        musicType=musicTypes['quarter'])
    
    minimLineFP = locations(template+'/minimLine.png', scoreFile,
                          musicType=musicTypes['minim'])
    minimSpace = locations(template+'/minimSpace.png', scoreFile,
                           musicType=musicTypes['minim'])
    
    dottedMinimLine = locations(template+'/dottedMinimLine3.png', scoreFile,
                                musicType=musicTypes['dottedMinim'])
    dottedMinimSpace = locations(template+'/dottedMinimSpace.png', scoreFile,
                                 musicType=musicTypes['dottedMinim'])
    
    semibreveLine = locations(template+'/semibreveLine.png', scoreFile,
                              musicType=musicTypes['semibreve'])
    semibreveSpace = locations(template+'/semibreveSpace.png', scoreFile,
                               musicType=musicTypes['semibreve'])

    # removing false positives for minimLineFP
    minimLine = resolveOverlap(minimLineFP, dottedMinimLine)
    # combining lines and space notes together
    minim = minimLine + minimSpace
    dottedMinim = dottedMinimLine + dottedMinimSpace
    semibreve = semibreveLine + semibreveSpace
    
    
    ########################################################
    ## identifying rests ###################################
    quarterRest = locations(template+'/quarterRest.png', scoreFile,
                            musicType=musicTypes['quarterRest'])
    minimRest = locations(template+'/minimRest.png', scoreFile,
                          musicType=musicTypes['minimRest'])
    semibreveRest = locations(template+'/semibreveRest.png', scoreFile,
                              musicType=musicTypes['semibreveRest'])


    ########################################################
    # identifying clefs and staves #########################
    trebleClef = locations(template+'/trebleClef.png', scoreFile,
                           musicType=musicTypes['trebleClef'])
    
    barLineFP = locations(template+'/barLine.png', scoreFile,
                         musicType=musicTypes['barLine'])
    singleEnd = locations(template+'/singleEnd.png', scoreFile,
                          musicType=musicTypes['singleEndS'])
    doubleEnd = locations(template+'/doubleEnd.png', scoreFile,
                          musicType=musicTypes['doubleEndS'])

    # barlines do overlap with singleEnds
    barLine1 = resolveOverlap(barLineFP, singleEnd)

    # removing false positives for barlineFP, essentially removing
    # last element
    barLine = barLineFP[:len(barLine1)-1]

    ######################################################################
    ## Test Code for Visualization #######################################
    ######################################################################
    if test == True:
        # change location to list of tuples of music symbol
        location = barLine
        
        scoreImg = cv2.imread(scoreFile, 1)
        print('entire list of tuples:')
        print(location)
        print('number of', location[0][2], 'identified:' + str(len(location)))
        for point in location:
            r = 10
            cv2.circle(scoreImg, (point[0], point[1]), r,
                       (0,0,255), 2)

        cv2.imshow('score display',scoreImg)

        # waits for any keystroke to continue to destroy all windows
        cv2.waitKey(0) 
        cv2.destroyAllWindows() 


    ######################################################################

    return (quarter, minim, dottedMinim, semibreve,
            quarterRest, minimRest, semibreveRest,
            barLine, singleEnd, doubleEnd,
            trebleClef)
    

def identifyPitch(scoreFile, template='./MusicNotesTemplate', test=False):
    # identifies the pitch

    allTypes = createMusicTypes(scoreFile, template=template, test=test)

    quarter, minim, dottedMinim, semibreve = allTypes[0], allTypes[1],\
                                             allTypes[2], allTypes[3]

    quarterRest, minimRest, semibreveRest = allTypes[4], allTypes[5],\
                                            allTypes[6]

    barLine, singleEnd, doubleEnd = allTypes[7], allTypes[8], allTypes[9]

    trebleClef = allTypes[10]
    
    # classifying staves, using lists
    allStaves = singleEnd + doubleEnd


    ########################################################
    ## Get dimensions of each stave type, only 2 ###########
    
    # dimensions of each stave that's not double barred ending
    stave = cv2.imread(template+'/singleEnd.png',1)
    staveHeight = stave.shape[0]
    numNotesInStave = 8
    noteSep = staveHeight/numNotesInStave

    # dimensions of each stave that has a double barred ending
    stave2 = cv2.imread(template+'/doubleEnd.png',1)
    staveHeight2 = stave2.shape[0]
    noteSep2 = staveHeight2/numNotesInStave

    numLines = len(allStaves) # number of lines
    # allStaves is the coordinates of all staves in music
    
    dividers = []

    for line in range(len(allStaves)):
        if line != len(allStaves)-1:
            adjustY = (allStaves[line][1] + allStaves[line+1][1])//2

        else: # it's the double bar ending
            adjustY = allStaves[line][1] + 1.5*staveHeight2 

        dividers.append((allStaves[line][0], adjustY, ('dvd',)))    

    
    # add dividers into list of all music objects
    allNotesRestsBarsP = quarter + minim + dottedMinim + semibreve +\
                        quarterRest + minimRest + semibreveRest +\
                        barLine + singleEnd + doubleEnd + \
                        trebleClef +\
                        dividers

    allNotesRestsBars = []

    # checks for empty elements
    for item in allNotesRestsBarsP:
        if item != []: allNotesRestsBars.append(item)
            
    # sort based on Y coordinate, then X coordinate
    allNotesRestsBars = sorted(allNotesRestsBars,
                               key = lambda elem: (elem[1], elem[0]))

    ########################################################
    # create list of pitches ###############################
    pitches = []
    notesTreble = ['D6','C6','B5','A5','G5','F5','E5','D5','C5','B4',
                   'A4','G4','F4','E4','D4','C4','B3','A3','G3']
    
    for line in range(len(allStaves)):
        pitchDict = {}
        numNotes = 19
        noteLines = []
        if line < len(allStaves) - 1:
            for i in range(numNotes):
                pitchDict[int(allStaves[line][1]-noteSep*(numNotes-1)/2 +\
                          noteSep*i)] = notesTreble[i]
        else:
            for i in range(numNotes):
                pitchDict[int(allStaves[line][1]-noteSep2*(numNotes-1)/2 +\
                          noteSep2*i)] = notesTreble[i]

        pitches.append(pitchDict)
    
    lineNum = 0
    # classify the pitches, but create list of dictionaries of pitches first
    playBackList = []
    playBackLine = []
    
    for elem in allNotesRestsBars:
        xPosn = elem[0]
        yPosn = elem[1]
        if elem[2] == ('dvd',):
            # toggle a switch in lineNum
            lineNum += 1

            # sort the playBackLine based on x Coordinate, ie item[1]
            playBackLine = sorted(playBackLine,
                                  key = lambda item: item[1])
            playBackList.append(playBackLine)
            playBackLine = []
                                  
        # find closes note line
        minDiff = staveHeight
        linePitch = -1
        
        if elem[2][0] == 'n':
            for key in pitches[lineNum]:
        
                # finding the pitch
                if abs(elem[1]-key) < minDiff:
                    minDiff = abs(elem[1]-key)
                    linePitch = key

            playBackLine.append((pitches[lineNum][linePitch],
                                 (xPosn,yPosn),elem[2]))

        elif elem[2][0] == 'r':
            playBackLine.append((0,(xPosn,yPosn),elem[2]))

        elif elem[2][0] == 'barline':
            playBackLine.append(('|',(xPosn,yPosn),elem[2]))

    return (playBackList, allStaves)
    
def convert2playable(scoreFile, template='./MusicNotesTemplate', test=False):
    # group all notes into their respective staves to enable playback in
    # Tkinter, returns list of list of playable notes

    playBackList, allStaves = identifyPitch(scoreFile,
                                            template=template, test=test)

    for i in playBackList:
        
        #print(i)
        pass
        
    finalPlayBack = []
    presentBar = []
    
    for line in playBackList:
        # goes through each line of music, the whole stave  
        for i in range(len(line)):

            playInfo = line[i][0]
            posn = line[i][1]
            musicType = line[i][2] # this is a tuple

            if playInfo == '|':
                finalPlayBack.append(presentBar)
                presentBar = []
                
            elif type(playInfo) == str:
                presentBar.append((playInfo,posn))
                for beat in range(1,musicType[1]):
                    presentBar.append((1,posn))
                    
            elif playInfo == 0:
                for beat in range(musicType[1]):
                    presentBar.append((playInfo,posn))

            if i == len(line) - 1:
                # whole line is done
                finalPlayBack.append(presentBar)
                presentBar = []
    #print(finalPlayBack)
    return (finalPlayBack, allStaves)
                    
###test code
##playBackList = convert2playable('./MusicScores/Goldenrod_Theme.png',
##                                test=True)
####print(playBackList)

##playBackList = convert2playable('./MusicScores/Sample1.png', test=True)
##print(playBackList)
