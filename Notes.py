# notes

notes = ['C4','E4','G4','C5','B4','A4','G4','F4','E4','F4','G4',
         'E4','D4','E4','F4','D4','C4']


'Octave/Eb4.wav'

def getNotes():
    new = []
    for note in notes:
        newNote = 'Octave/' + note + '.wav'
        new.append(newNote)
    return new
