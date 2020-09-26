# music21_evidence-based_harmony

Here are some exploratory tools I'm developing/adapting, using python and music21 to teach “evidence-based harmony”.

The "BachChoral" class loads a J.S.Bach Choral from music21 corpus. It has methods that make it easier:
to get the choral info, the most probable key / keySignature,
to implode the 4-staff choral to piano and individual voices,
to seach for specifice chords.

By now there are two methods that can be used to search things:

- searchD7, searches Dominant 7 candidates: colors notes red (the seventh is brighter)
- searchS65, searches added 6th candidates: colors notes orange.
