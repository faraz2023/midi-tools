def get_system_prompt(output_type, per_file_length, genre, instrument, tempo, time_signature, key):
    return f"""
Rules:

- IMPORTANT: The loop MUST be EXACTLY {per_file_length} bars long, no more and no less.
- Use absolute timing, where 1.0 represents a quarter note. The loop must be exactly {per_file_length} bars long.
- In {time_signature[0]}/{time_signature[1]} time, each bar is {time_signature[0]}.0 beats long.
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
- <IMPORTANT> We must have {per_file_length} bars which with the above format results in {per_file_length*4} quarter notes.

- Do not include explanations, comments, or extra text. Only provide note events.
- Ensure ensure that in the note data you generate, no two notes of the same pitch and channel start at the same time.

Artistic and Stylistic Guidelines:
- {genre}
- Instrument: {instrument} (melodic, MIDI channel 0).

Below are some example formats (do not copy these verbatim, they are for reference ONLY):

Example Melody (1 bar in 4/4)(DO NOT USE FOR ARTISTIC REFERENCE, JUST A TECHNICAL FORMAT EXAMPLE):
0 C4 0.5 100 0
0.5 E4 0.5 100 0
1 G4 0.5 100 0
1.5 C5 0.5 100 0
2 G4 1 100 0
3 E4 1 100 0

Currently requested loop type is: {output_type}
"""

def get_prompt(output_type, instrument, per_file_length, tempo, time_signature, key, genre, description):
    return f"""
We request you to create a {output_type} of EXACTLY {per_file_length} bars in length, intended for use in Ableton. 

IMPORTANT RULES:
- IMPORTANT: The loop MUST be EXACTLY {per_file_length} bars long, no more and no less.
- Use absolute timing, where 1.0 represents a quarter note. The loop must be exactly {per_file_length} bars long.
- In {time_signature[0]}/{time_signature[1]} time, each bar is {time_signature[0]}.0 beats long.
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
- <IMPORTANT> We must have {per_file_length} bars which with the above format results in {per_file_length*4} quarter notes.

- Do not include explanations, comments, or extra text. Only provide note events.
- Ensure ensure that in the note data you generate, no two notes of the same pitch and channel start at the same time.


Below are some example formats (do not copy these verbatim, they are for reference ONLY):

Example Melody (1 bar in 4/4)(DO NOT USE FOR ARTISTIC REFERENCE, JUST A TECHNICAL FORMAT EXAMPLE):
0 C4 0.5 100 0
0.5 E4 0.5 100 0
1 G4 0.5 100 0
1.5 C5 0.5 100 0
2 G4 1 100 0
3 E4 1 100 0



Genre: {genre}
The instrument is {instrument}, played on MIDI channel 0.

Details:
- Tempo: {tempo} bpm
- Time Signature: {time_signature[0]}/{time_signature[1]}
- Key: {key}
- Expected Length: EXACTLY {per_file_length} bars.

Artistic and Stylistic Guidelines:
- Genre: {genre}
- Description: {description}
- Instrument: {instrument} (melodic, MIDI channel 0).

Do not include explanations or commentary. Only output the note data in the specified format.
"""

defaults = {
    "output_type": "melody",
    "instrument": "felt piano",
    "per_file_length": 4,
    "tempo": 80,
    "time_signature": (4, 4),
    "key": "Dminor",
    "genre": """
The piece should be genre-appropriate, resembling the style of neo-classical composers such as Nils Frahm or Ólafur Arnalds.
The peace should be slow moving and remind us of the movement of the ocean.
""",
    "description": """
- The loop should feel evolving and expressive, yet simple and minimalist, with a strong, yet slow rhythmic pulse.
- Utilize simple motifs that develop over time. Consider adding subtle arpeggiations to create a more complex texture.
- Vary velocities for natural dynamics and realism. Avoid constant velocities.
- Ensure that the harmonic and melodic content reflects the requested key and conveys the intended mood.
"""
} 