# test on how to read, display, and write images
import cv2
import numpy as np
import Notes
from Sounds import sounds
import time
import threading
from threading import Thread

# cv2.imread('imageName.png',flag) flag can be 1(color), 0(grayscale)
# or -1(unchanged)

qtrNote = cv2.imread('./MusicNotesTemplate/quarter.png',0)
score = cv2.imread('./MusicScores/basicScoretest3.png',0)

print(score.shape)
result = cv2.matchTemplate(score,qtrNote,cv2.TM_CCOEFF_NORMED)

threshold = 0.74 # empirically tested threshold
location = np.where(result >= threshold)

# find notes
counter = 0
#print(location)

for point in zip(*location[::-1]):
    # counter += 1
    
    r = 10
    cv2.circle(score, (point[0] + r, point[1] +r), r, (0,0,255), 2)
#print(counter)   

# show image
# the string is just the window name
cv2.imshow('score display',score)

endBar = cv2.imread('./MusicScores/endScore.png',0)
r2 = cv2.matchTemplate(score,endBar,cv2.TM_CCOEFF_NORMED)

loc2 = np.where(result >= threshold)

for point in zip(*location[::-1]):
    r = 20
    cv2.circle(score, (point[0] + r, point[1] +r), r, (0,0,255), 2)
    
def playNote(filename):
    print('play')
    start = time.time()
    # try to change it to play for shorter periods of time
    sounds.play('./'+ filename)

##[[C, D, E, F], [F,G,A,B]]

##def play():
##    # dummy playing for now
##    notes = Notes.getNotes()
##    counter = 0
##    for note in notes:
##        counter += 1
##        once = 0
##        while once == 0:
##            if time.time() % 1 == 0:
##                once += 1
##                if once == 1:
##                    Thread(target=playNote, args=(note,)).start()
##                    break
##        
##Thread(target=play).start()

cv2.waitKey(0) # 0 is passed, so it waits indefinitely for a keystroke
# and then continues
cv2.destroyAllWindows() # destroys all windows unless a specific window name
# is keyed in as argument
