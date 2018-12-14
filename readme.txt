SheetMusicAssistant

PROJECT DESCRIPTION:
SheetMusicAssistant is a python application that opens sheet music pdfs and runs optical music recognition with the openCV module. It is then able to play the sheet music pdf out loud via pyaudio, or listen to a user play an instrument while reading from the sheet music live via pyaudio and aubio. In both listening and playing modes, SheetMusicAssistant scrolls through the displayed sheet music, so you never have to flip a page again. Thus, SheetMusicAssistant performs both optical recognition and audio recognition. 

The current limitations are that it only reads music in common time, only reads in treble clef, only reads in c major, only reads notes that last 1 beat, 2 beats, 3 beats, and 4 beats, only reads rests that last for 1 beat, 2 beats, and 4 beats. Furthermore it only reads melodies, not two notes at a time.

HOW TO RUN:
Open main.py and run it with a python 3 interpreter

HOW TO INSTALL NEEDED LIBARIES:
The modules that need installation and are required to run SheetMusicAssistant are listed below, and the hyperlinks to install these modules are provided below each module name. Remember, SheetMusicAssistant runs in python 3 so be sure to install python 3 versions of each module:

openCV (for image recognition)
https://docs.opencv.org/master/df/d65/tutorial_table_of_content_introduction.html

wand (for converting pdf files to png for image recognition, gif for tkinter display)
http://docs.wand-py.org/en/0.4.5/

numpy (for both image recognition and audio recognition)
https://pypi.org/project/numpy/

pyaudio (for playing and recording audio)
https://people.csail.mit.edu/hubert/pyaudio/

aubio (for audio recognition)
https://aubio.org/manual/latest/python_module.html#python-install

SHORTCUT COMMANDS:
Currently there are no shortcut commands




