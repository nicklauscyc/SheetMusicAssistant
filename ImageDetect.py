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
    # takes in scoreImage for now
    

    # using openCV to match img on scoreImg, match coordinates are top
    # left corner of each img template
    result = cv2.matchTemplate(scoreImg, img, cv2.TM_CCOEFF_NORMED)
    location = np.where(result >= threshold)

    # converting numpy array to list of tuples of note coordinates
    allPoints = []
    for point in zip(*location[::-1]):
        allPoints.append((point[0], point[1], musicType))
        
    deduped = deduplicate(allPoints)
    
    return deduped


## Test Code for Visualization ##
location = locations('./MusicNotesTemplate/doubleEnd.png',
                     './MusicScores/Sample1.png')

scoreImg = cv2.imread('./MusicScores/Sample1.png', 1)
print(location)
for point in location:
    r = 10
    cv2.circle(scoreImg, (point[0], point[1]), r,
               (0,0,255), 2)
    
print(len(location))

cv2.imshow('score display',scoreImg)

# waits for any keystroke to continue to destroy all windows
cv2.waitKey(0) 
cv2.destroyAllWindows() 
    
################################


