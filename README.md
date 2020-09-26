# evidence-based harmony tools

Here are some exploratory tools I'm developing/adapting, using python and music21 to teach "evidence-based harmony": that is, the inference of stylistic principles of tonal harmony based on the analysis of the repertoire.

This approach is strongly influenced Diether de la Motte's pedagogical approach in "The Study of Harmony: An Historical Perspective" [Harmonielehre]. The application, therefore, is less focused on automated analysis and more on the search for chords, voice-leading strategies, patterns and structures to identify, for example: frequency of use, context, etc.


The "BachChoral" class loads a J.S.Bach Choral from music21 corpus. It has attributes and methods that make it easier:
- to get the choral info, the most probable key / keySignature,
- to implode the 4-staff choral to piano and individual voices,
- to seach for specifice chords
- etc

By now there are two methods that can be used to search things:

- searchD7, searches Dominant 7 candidates: colors notes red (the seventh is brighter)
- searchS65, searches added 6th candidates: colors notes orange.

Warning: these methods are not fully functional and return some false positives!
