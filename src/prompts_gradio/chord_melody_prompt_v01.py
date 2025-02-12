def get_system_prompt(output_type, per_file_length, genre, instrument, tempo, time_signature, key):
    return f"""
Rules:

- Use absolute timing, where 1.0 represents a quarter note. The loop must be exactly {per_file_length} bars long.
- Tempo: {tempo} bpm, Time Signature: {time_signature[0]}/{time_signature[1]}, Key: {key}.
- For melodic instruments (MIDI channel 0), use standard note names (e.g., C4, F#5).

- Output Format:
Each line must contain one note event in the following format:
    <start_time> <note_name> <duration> <velocity> <MIDI_channel>
- <start_time> is in bar-relative units, where 0.0 is the start of the loop.
- <start_time> is in quarter-note units, where:
  - 0.0 = start of quarter note 1
  - 1.0 = start of quarter note 2
  - 2.0 = start of quarter note 3
  - 3.0 = start of quarter note 4
  - Subdivisions use decimals (0.5 = eighth note, 0.25 = sixteenth note)
- <duration> is the length of the note in quarter-note units:
  - 1.0 = quarter note
  - 0.5 = eighth note
  - 0.25 = sixteenth note
  - 0.125 = thirty-second note
- <velocity> is an integer velocity value.
- <MIDI_channel> is 0 for all notes (both melody and chords).
- <IMPORTANT> We must have {per_file_length} bars which with the above format results in {per_file_length*4} quarter notes.

- Do not include explanations, comments, or extra text. Only provide note events.
- Ensure that in the note data you generate, no two notes of the same pitch and channel start at the same time.
- The output should contain BOTH melody notes and chord notes, properly synchronized.
- Chords should support and enhance the melody, not overpower it.
- Melody notes should be in a higher register than chord notes for clarity.

Artistic and Stylistic Guidelines:
- {genre}
- Instrument: {instrument} (melodic, MIDI channel 0).

Below are some example formats (do not copy these verbatim, they are for reference ONLY):

Example Chord-Melody Combination with chord notes (lower register) and melody notes (higher register) (1 bar) (DO NOT USE FOR ARTISTIC REFERENCE, JUST A TECHNICAL FORMAT EXAMPLE):
0 C2 2 65 0
0 E2 2 60 0
0 G2 2 60 0
2 F2 2 65 0
2 A2 2 60 0
2 C3 2 60 0
0 E3 0.25 85 0
0.25 G3 0.125 75 0
0.375 A3 0.125 80 0
0.5 C4 0.5 90 0
1 B3 0.25 85 0
1.25 A3 0.25 80 0
1.5 G3 0.25 75 0
1.75 E3 0.25 70 0
2 F3 0.75 95 0
2.75 G3 0.25 85 0
3 A3 0.375 90 0
3.375 G3 0.125 80 0
3.5 E3 0.5 85 0



Currently requested loop type is: {output_type}
"""

def get_prompt(output_type, instrument, per_file_length, tempo, time_signature, key, genre, description):
    return f"""
We request you to create a {output_type} of {per_file_length} bars in length, intended for use in Ableton. 
The output should contain both a melody line and supporting chord progression that work together harmoniously.
Genre: {genre}
The instrument is {instrument}, played on MIDI channel 0.


IMPORTANT RULES:
- Use absolute timing, where 1.0 represents a quarter note. The loop must be exactly {per_file_length} bars long.
- Tempo: {tempo} bpm, Time Signature: {time_signature[0]}/{time_signature[1]}, Key: {key}.
- For melodic instruments (MIDI channel 0), use standard note names (e.g., C4, F#5).

- Output Format:
Each line must contain one note event in the following format:
    <start_time> <note_name> <duration> <velocity> <MIDI_channel>
- <start_time> is in bar-relative units, where 0.0 is the start of the loop.
- <start_time> is in quarter-note units, where:
  - 0.0 = start of quarter note 1
  - 1.0 = start of quarter note 2
  - 2.0 = start of quarter note 3
  - 3.0 = start of quarter note 4
  - Subdivisions use decimals (0.5 = eighth note, 0.25 = sixteenth note)
- <duration> is the length of the note in quarter-note units:
  - 1.0 = quarter note
  - 0.5 = eighth note
  - 0.25 = sixteenth note
  - 0.125 = thirty-second note
- <velocity> is an integer velocity value.
- <MIDI_channel> is 0 for all notes (both melody and chords).
- <IMPORTANT> We must have {per_file_length} bars which with the above format results in {per_file_length*4} quarter notes.

- Ensure that in the note data you generate, no two notes of the same pitch and channel start at the same time.
- The output should contain BOTH melody notes and chord notes, properly synchronized.
- Chords should support and enhance the melody, not overpower it.
- Melody notes should be in a higher register than chord notes for clarity.



Below are some example formats (do not copy these verbatim, they are for reference ONLY):
Example Chord-Melody Combination with chord notes (lower register) and melody notes (higher register) (1 bar) (DO NOT USE FOR ARTISTIC REFERENCE, JUST A TECHNICAL FORMAT EXAMPLE):
0 C2 2 65 0
0 E2 2 60 0
0 G2 2 60 0
2 F2 2 65 0
2 A2 2 60 0
2 C3 2 60 0
0 E3 0.25 85 0
0.25 G3 0.125 75 0
0.375 A3 0.125 80 0
0.5 C4 0.5 90 0
1 B3 0.25 85 0
1.25 A3 0.25 80 0
1.5 G3 0.25 75 0
1.75 E3 0.25 70 0
2 F3 0.75 95 0
2.75 G3 0.25 85 0
3 A3 0.375 90 0
3.375 G3 0.125 80 0
3.5 E3 0.5 85 0


Details:
- Tempo: {tempo} bpm
- Time Signature: {time_signature[0]}/{time_signature[1]}
- Key: {key}

Artistic and Stylistic Guidelines:
- {genre}
- Instrument: {instrument} (melodic, MIDI channel 0).

Do not include explanations or commentary. Only output the note data in the specified format.
"""

defaults = {
    "output_type": "chord-melody",
    "instrument": "felt piano",
    "per_file_length": 4,
    "tempo": 80,
    "time_signature": (4, 4),
    "key": "Dminor",
    "genre": "The piece should be genre-appropriate, resembling the style of neo-classical composers such as Nils Frahm or Ólafur Arnalds, with a focus on the interplay between melody and harmony.",
    "description": """
- Create a cohesive musical piece where melody and chords complement each other.
- The melody should be expressive and lyrical, while the chords provide harmonic support and movement.
- Melody notes should generally be in a higher register than chord notes for clarity.
- Use chord voicings that support but don't overpower the melody.
- Vary velocities naturally - typically melody notes slightly louder than chord notes.
- Ensure smooth voice leading in both melody and chord progressions.
- Consider using passing tones in the melody that create tension and resolution with the underlying chords.
- The harmonic rhythm (chord changes) should support the melodic phrases.
"""
} 