from music21 import *
from bachchoral import *
import sys
import copy
sys.setrecursionlimit(10**6)


#music21
x = BachChoral(5) # Loads Choral 20 (Riemenschneider numbering)
x.num # Riemenschneider numbering
x.bwv # BWV numbering
x.choralinfo #further choral info as dict
k = x.key # most probable key
k
print(k)
x.keySharps # number of sharps (positive) or flats (negative) in the KeySignature

# get music21 object "stream.Score" of the Choral
x.chor
x.chor.show() #shows 4-staff score: S, A, T, B (already excludes other parts if they exist)
x.show() # same
x.show('xml') #shows on external musicxml capable app (MuseScore)

p = x.piano # piano imploded version
p.show()

# individual voices are stored in the respective object attributes
s = x.soprano
a = x.alto
t = x.tenor
b = x.bass
s.show()
b.show()

# search for D7 candidates [not fully functional yet!]: red color (7th is brigher)
x.searchD7()

# search for S65 (added 6th) candidates [not fully functional yet!]: orange
x.searchS65()

p.show() # see reduction with colored notes
x.noColors() # back to black and white
