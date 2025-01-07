output_type = 'melody'
instrument = "felt piano"
per_file_length = 4
tempo = 80
time_signature = (4, 4)
key = 'Dminor'
genre = """
The piece should be genre-appropriate, resembling the style of neo-classical composers such as Nils Frahm or Ólafur Arnalds.
The peace should be slow moving and remind us of the movement of the ocean.
"""
description = f"""
- The loop should feel evolving and expressive, yet simple and minimalist, with a strong, yet slow rhythmic pulse.
- Utilize simple motifs that develop over time. Consider adding subtle arpeggiations to create a more complex texture.
- Vary velocities for natural dynamics and realism. Avoid constant velocities.
- Ensure that the harmonic and melodic content reflects the requested key of {key} and conveys the intended mood.
- The piece should be in the key of {key}.
"""

system_prompt = f"""
Rules:

- Use absolute timing, where 1.0 represents a quarter note. The loop must be exactly {per_file_length} bars long.
- Tempo: {tempo} bpm, Time Signature: {time_signature[0]}/{time_signature[1]}, Key: {key}.
- For drums (MIDI channel 9), use only these Ableton default drum names and their mappings:
- kick: 36
- snare: 38
- clap: 39
- closed_hat: 42
- open_hat: 46
- low_tom: 41
- mid_tom: 47
- high_tom: 50
- crash: 49
- ride: 51

- For melodic instruments (MIDI channel 0), use standard note names (e.g., C4, F#5).

- Ensure ensure that in the note data you generate, no two notes of the same pitch and channel start at the same time. This is necessary for the midi export work.

- Output Format:
Each line must contain one note event in the following format:
    <start_time> <note_name or drum_name> <duration> <velocity> <MIDI_channel>
- <start_time> is in bar-relative units, where 0.0 is the start of the loop.
- <duration> is the length of the note in quarter-note units.
- <velocity> is an integer velocity value.
- <MIDI_channel> is 9 for drums and 0 for melodic instruments.

- Do not include explanations, comments, or extra text. Only provide note events.

Artistic and Stylistic Guidelines:
- {genre}
- Instrument: {instrument} (melodic, MIDI channel 0).


Below are some example formats (do not copy these verbatim, they are for reference ONLY):

Example Drum Loop (1 bar):
0 kick 0.25 100 9
0.5 snare 0.25 90 9
1 kick 0.25 100 9
1.5 snare 0.25 90 9
0 closed_hat 0.25 80 9
0.5 closed_hat 0.25 80 9
1 closed_hat 0.25 80 9
1.5 open_hat 0.25 80 9

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

Example Melody (1 bar):
0 C4 0.5 100 0
0.5 E4 0.5 100 0
1 G4 0.5 100 0
1.5 C5 0.5 100 0
2 G4 1 100 0
3 E4 1 100 0


Currently requested loop type is: {output_type}
"""

prompt = f"""
We request you to create a {output_type} of {per_file_length} bars in length, intended for use in Ableton. 
Genre: {genre}
The instrument is {instrument}, played on MIDI channel 0.

Details:
- Tempo: {tempo} bpm
- Time Signature: {time_signature[0]}/{time_signature[1]}
- Key: {key}

Artistic and Stylistic Guidelines:
- {description}


- IMPORTANT: - Ensure ensure that in the note data you generate, no two notes of the same pitch and channel start at the same time. This is necessary for the midi export work.

Do not include explanations or commentary. Only output the note data in the specified format.
"""