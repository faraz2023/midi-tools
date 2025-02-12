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
- <MIDI_channel> is 0 for melodic instruments.

- Do not include explanations, comments, or extra text. Only provide note events.

- Ensure ensure that in the note data you generate, no two notes of the same pitch and channel start at the same time. This is necessary for the midi export work.

Artistic and Stylistic Guidelines:
- {genre}
- Instrument: {instrument} (melodic, MIDI channel 0).

Below is an example format (do not copy this verbatim, it is for reference ONLY):

Example Chord Progression (1 bar) (DO NOT USE FOR ARTISTIC REFERENCE, JUST A TECHNICAL FORMAT EXAMPLE):
0 C4 1 80 0
0 E4 1 80 0
0 G4 1 80 0
1 F4 1 80 0
1 A4 1 80 0
1 C5 1 80 0
2 G4 1 80 0
2 B4 1 80 0
2 D5 1 80 0
3 C4 1 80 0
3 E4 1 80 0
3 G4 1 80 0

Currently requested loop type is: {output_type}
"""

def get_prompt(output_type, instrument, per_file_length, tempo, time_signature, key, genre, description):
    return f"""
We request you to create a {output_type} progression of {per_file_length} bars in length, intended for use in Ableton. 
Genre: {genre}
The instrument is {instrument}, played on MIDI channel 0.

Details:
- Tempo: {tempo} bpm
- Time Signature: {time_signature[0]}/{time_signature[1]}
- Key: {key}

Artistic and Stylistic Guidelines:
{description}

Do not include explanations or commentary. Only output the note data in the specified format.
"""

defaults = {
    "output_type": "chords",
    "instrument": "felt piano",
    "per_file_length": 4,
    "tempo": 80,
    "time_signature": (4, 4),
    "key": "Dminor",
    "genre": "The piece should be genre-appropriate, resembling the style of neo-classical composers such as Nils Frahm or Ólafur Arnalds.",
    "description": """
- The chord progression should be expressive and evolving, yet simple and minimalist.
- Utilize simple chord voicings that develop over time. Consider adding subtle inversions or extensions to create a more complex harmony.
- Vary velocities for natural dynamics and realism. Avoid constant velocities.
- Ensure that the harmonic content reflects the requested key and conveys the intended mood.
"""
} 