output_type = 'chords'
instrument = "felt piano"
per_file_length = 4
tempo = 80
time_signature = (4, 4)
key = 'Dminor'
genre = "The piece should be genre-appropriate, resembling the style of neo-classical composers such as Nils Frahm or Ólafur Arnalds."
description = f"""
- The chord progression should be expressive and evolving, yet simple and minimalist.
- Utilize simple chord voicings that develop over time. Consider adding subtle inversions or extensions to create a more complex harmony.
- Vary velocities for natural dynamics and realism. Avoid constant velocities.
- Ensure that the harmonic content reflects the requested key of {key} and conveys the intended mood.
- The piece should be in the key of {key}.
"""

system_prompt = f"""
Rules:

- Use absolute timing, where 1.0 represents a quarter note. The loop must be exactly {per_file_length} bars long.
- Tempo: {tempo} bpm, Time Signature: {time_signature[0]}/{time_signature[1]}, Key: {key}.
- For melodic instruments (MIDI channel 0), use standard note names (e.g., C4, F#5).

- Output Format:
Each line must contain one note event in the following format:
    <start_time> <note_name> <duration> <velocity> <MIDI_channel>
- <start_time> is in bar-relative units, where 0.0 is the start of the loop.
- <duration> is the length of the note in quarter-note units.
- <velocity> is an integer velocity value.
- <MIDI_channel> is 0 for melodic instruments.

- Do not include explanations, comments, or extra text. Only provide note events.

- Ensure ensure that in the note data you generate, no two notes of the same pitch and channel start at the same time. This is necessary for the midi export work.


Artistic and Stylistic Guidelines:
- {genre}
- Instrument: {instrument} (melodic, MIDI channel 0).


Below is an example format (do not copy this verbatim, it is for reference ONLY):

Example Chord Progression (1 bar):
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

prompt = f"""
We request you to create a {output_type} progression of {per_file_length} bars in length, intended for use in Ableton. 
Genre: {genre}
The instrument is {instrument}, played on MIDI channel 0.

Details:
- Tempo: {tempo} bpm
- Time Signature: {time_signature[0]}/{time_signature[1]}
- Key: {key}

Artistic and Stylistic Guidelines:
- {description}

Do not include explanations or commentary. Only output the note data in the specified format.
""" 