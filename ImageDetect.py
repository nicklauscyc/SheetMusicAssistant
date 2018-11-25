# test on how to read, display, and write images
import cv2
import numpy as np

def deduplicate(allPoints, bounds=10):
    # takes in allPoints list of tuples from locations(),
    # and returns a list of tuples that is deduplicated

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
    imgCenY = imgHeight//2
    
    # using openCV to match img on scoreImg, match coordinates are top
    # left corner of each img template
    result = cv2.matchTemplate(scoreImg, img, cv2.TM_CCOEFF_NORMED)
    location = np.where(result >= threshold)

    # converting numpy array to list of tuples of note coordinates
    # X coordinate is the left edge of img, Y coordinate is center of img
    allPoints = []
    for point in zip(*location[::-1]):
        allPoints.append((point[0], point[1]+imgCenY, musicType))
        
    deduped = deduplicate(allPoints)
    
    return deduped


def classifyStave():
    # group all notes into their respective staves
    pass

def classifyNote():
    # classify a note per stave
    pass

def convertStave2List():
    # convert a list of tuples from 1 stave to a list of lists
    # for playback purposes and further analysis
    
    pass


## Creating all list of tuples for each musical symbol


def resolveOverlap(symbol, overlap):
    # for resolving instances where 'falsePositive' show up.
    # example would be 'symbol' as minims and 'overlap' as dottedMinims.
    # both arguments are lists of 3-tuples eg. (1082, 700, ('n',1,4)) for
    # a quarter note or (1032, 321, ('end1')) for a single end bar line

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

    # dictionary of all possile music types
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
    
    dottedMinimLine = locations(template+'/dottedMinimLine.png', scoreFile,
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
    
    barLineFP= locations(template+'/barLine.png', scoreFile,
                         musicType=musicTypes['barLine'])
    singleEnd = locations(template+'/singleEnd.png', scoreFile,
                          musicType=musicTypes['singleEndS'])
    doubleEnd = locations(template+'/doubleEnd.png', scoreFile,
                          musicType=musicTypes['doubleEndS'])

    # removing false positives for barlineFP, essentially removing
    # last element
    barLine = barLineFP[:len(barLineFP)-1]

    ######################################################################
    ## Test Code for Visualization #######################################
    ######################################################################
    if test == True:
        # change location to list of tuples of music symbol
        location = trebleClef
        
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

createMusicTypes('./MusicScores/Sample1.png', test=True)
