from music21 import *
import copy
import sys
sys.setrecursionlimit(10**6)

class BachChoral:
    bcl = corpus.chorales.ChoraleListRKBWV()
    # bcl = corpus.chorales.ChoraleList()
    bci = corpus.chorales.Iterator()
    domColor = '#C71E1D'
    n7Color = '#FF1E1D'
    subdomColor = '#DB6D1D'

    # Constructor method with instance variables name and age
    def __init__(self, num):
        self.num = num
        self.rawimp = None
        self.piano = None
        self.nummeasures = None
        # self.soprano = stream.Stream()
        # self.alto = stream.Stream()
        # self.tenor = stream.Stream()
        # self.bass = stream.Stream()
        self.impChorUstaff = None
        self.impChorDstaff = None
        self.chfy = None
        self.chords = None
        self.chordsOffsets = []
        self.numchords = None
        self.choralinfo = self.bcl.byRiemenschneider[num]
        self.bwv = str(self.choralinfo['bwv'])
        self.key = None
        self.keySharps = None
        self.timeSignature = None
        self.bachscore = corpus.parse('bach/bwv' + self.bwv)
        #self.bachscore = self.bci[num]
        self.parts = self.bachscore.getElementsByClass('Part')
        # aluns corais têm partes instrumentais associadas na base de
        # dados do music21 além de nomes de partes inconsistentes...
        # por hora é mais fácil ir até a ultima parte instrumental
        self.numparts = len(self.parts)
        self.chor = stream.Score()

        self.soprano = copy.copy(self.parts[self.numparts-4])
        self.alto = copy.copy(self.parts[self.numparts-3])
        self.tenor = copy.copy(self.parts[self.numparts-2])
        self.bass = copy.copy(self.parts[self.numparts-1])


        self.justchor()

        self.pianocoral()
        # self.cleanpart()
        self.getchords()



    def justchor(self):
        """Cria redução inicial contendo apenas soprano, contralto e baixo"""
        self.chor.append(self.soprano)
        self.chor.append(self.alto)
        self.chor.append(self.tenor)
        self.chor.append(self.bass)
        self.rawimp = self.chor.implode()
        self.piano = self.rawimp

    def pianocoral(self):
        self.impChorUstaff = self.piano[0]
        self.impChorDstaff = self.piano[1]
        saC = clef.TrebleClef()
        tbC = clef.BassClef()
        self.impChorUstaff[0].clef = saC
        self.impChorDstaff[0].clef = tbC
        umeasures = self.impChorUstaff.getElementsByClass(stream.Measure)
        dmeasures = self.impChorDstaff.getElementsByClass(stream.Measure)
        self.nummeasures = len(umeasures)
        for i in range(0,self.nummeasures):
            saM = umeasures[i]
            tbM = dmeasures[i]
            # saClef = saM.getElementsByClass(clef.Clef)
            # tbClef = tbM.getElementsByClass(clef.Clef)
            sop = saM.getElementsByClass(stream.Voice)[0]
            alt = saM.getElementsByClass(stream.Voice)[1]
            ten = tbM.getElementsByClass(stream.Voice)[0]
            bas = tbM.getElementsByClass(stream.Voice)[1]
            sopN = sop.getElementsByClass(note.Note)
            altN = alt.getElementsByClass(note.Note)
            tenN = ten.getElementsByClass(note.Note)
            basN = bas.getElementsByClass(note.Note)
            for sN in sopN:
                sN.lyrics = ""
            for aN in altN:
                aN.expressions = ""
                aN.lyrics = ""
            for tN in tenN:
                tN.expressions = ""
                tN.lyrics = ""
            for bN in basN:
                #bN.expressions = ""
                bN.lyrics = ""
        self.key = self.piano.analyze('key')
        self.keySharps = self.key.sharps
        # print(tbClef.flat[0])

    # def cleanpart(self):
    #     p1measures = self.piano[0].getElementsByClass(stream.Measure)
    #     p2measures = self.piano[1].getElementsByClass(stream.Measure)
    #
    #     self.soprano.insert(0, key.KeySignature(self.keySharps))
    #     self.alto.insert(0, key.KeySignature(self.keySharps))
    #     self.tenor.insert(0, key.KeySignature(self.keySharps))
    #     self.bass.insert(0, key.KeySignature(self.keySharps))
    #
    #     for msa in p1measures:
    #         svoice = msa.getElementsByClass(stream.Voice)[0]
    #         avoice = msa.getElementsByClass(stream.Voice)[1]
    #         self.soprano.append(svoice.getElementsByClass(note.Note))
    #         self.alto.append(avoice.getElementsByClass(note.Note))
    #     for mtb in p2measures:
    #         tvoice = mtb.getElementsByClass(stream.Voice)[0]
    #         bvoice = mtb.getElementsByClass(stream.Voice)[1]
    #         self.tenor.append(tvoice.getElementsByClass(note.Note))
    #         self.bass.append(bvoice.getElementsByClass(note.Note))
    #     self.soprano = self.soprano.flat
    #     self.alto = self.alto.flat
    #     self.tenor = self.tenor.flat
    #     self.bass = self.bass.flat

    def getchords(self):
        self.chfy = self.piano.chordify()
        self.chords = self.chfy.flat.getElementsByClass("Chord")
        self.numchords = len(self.chords)

    def searchD7(self):
        for i in range(0, self.numchords):
            chord = self.chords[i]
            coffset = chord.offset
            floffset = (coffset%1)
            croot = chord.root().name
            cbass = chord.bass().name
            cthird = chord.getChordStep(3)
            cfifth = chord.getChordStep(5)

            self.chordsOffsets.append(coffset)
            notes = self.piano.flat.getElementsByOffset(coffset).getElementsByClass(note.Note)
            if chord.containsTriad():
                canBeDominant = chord.canBeDominantV()
                has7 = chord.containsSeventh()
                if (canBeDominant and has7):
                    c7 = chord.getChordStep(7)

                    for n in notes:
                        # print(c7,n.pitch)
                        if (c7 == n.pitch):#marcar a sétima!
                            n.style.color = self.n7Color
                        else:
                            n.style.color = self.domColor
                    if (floffset != 0):
                        notes2 = self.piano.flat.getElementsByOffset(coffset - floffset,coffset).getElementsByClass(note.Note)
                        c1 = chord.getChordStep(1)
                        c3 = chord.getChordStep(3)
                        c5 = chord.getChordStep(5)
                        c7 = chord.getChordStep(7)
                        for n in notes2:
                            # print(c7,n.pitch)
                            if (c7 == n.pitch):#marcar a sétima!
                                n.style.color = self.n7Color
                            else:#if ((c1 == n.pitch) or (c3 == n.pitch) or (c5 == n.pitch)):
                                n.style.color = self.domColor

    def searchS65(self):
        for i in range(0, self.numchords):
            chord = self.chords[i]
            coffset = chord.offset
            floffset = (coffset%1)
            croot = chord.root().name
            cbass = chord.bass().name
            cthird = chord.getChordStep(3)
            cfifth = chord.getChordStep(5)

            self.chordsOffsets.append(coffset)
            notes = self.piano.flat.getElementsByOffset(coffset).getElementsByClass(note.Note)

            if chord.containsTriad():
                canBeDominant = chord.canBeDominantV()
                has7 = chord.containsSeventh()
                isInv1 = (chord.inversion() == 1)
                # is65 = (chord.inversionName() == 65)
                if ( (not canBeDominant) and has7 and isInv1):
                    for n in notes:
                        n.style.color = self.subdomColor
                    if (floffset != 0):
                        notes2 = self.piano.flat.getElementsByOffset(coffset - floffset).getElementsByClass(note.Note)
                        for n in notes2:
                            n.style.color = self.subdomColor

    def noColors(self):
        for i in range(0, self.numchords):
            chord = self.chords[i]
            coffset = chord.offset
            notes = self.piano.flat.getElementsByOffset(coffset).getElementsByClass(note.Note)
            for n in notes:
                n.style.color = '#000000'

    # Method with instance variable followers
    def show(self):
        self.chor.show()
