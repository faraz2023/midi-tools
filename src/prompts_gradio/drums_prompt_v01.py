def get_system_prompt(output_type, per_file_length, genre, instrument, tempo, time_signature, key):
    return f"""
Rules:

- Use absolute timing, where 1.0 represents a quarter note. The loop must be exactly {per_file_length} bars long.
- Tempo: {tempo} bpm, Time Signature: {time_signature[0]}/{time_signature[1]}.
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

- Output Format:
Each line must contain one note event in the following format:
    <start_time> <drum_name> <duration> <velocity> <MIDI_channel>
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
- <MIDI_channel> is 9 for drums.

- Do not include explanations, comments, or extra text. Only provide note events.

- Ensure ensure that in the note data you generate, no two notes of the same pitch and channel start at the same time. This is necessary for the midi export work.

Artistic and Stylistic Guidelines:
- {genre}
- Instrument: {instrument} (drums, MIDI channel 9).

Below are some example formats (do not copy these verbatim, they are for reference ONLY):

Example Drum Loop (1 bar) (DO NOT USE FOR ARTISTIC REFERENCE, JUST A TECHNICAL FORMAT EXAMPLE):
0 kick 0.5 100 9
1 snare 0.5 90 9
2 kick 0.5 100 9
3 snare 0.5 90 9
0 closed_hat 0.5 80 9
1 closed_hat 0.5 80 9
2 closed_hat 0.5 80 9
3 open_hat 0.5 80 9

Currently requested loop type is: {output_type}
"""

def get_prompt(output_type, instrument, per_file_length, tempo, time_signature, key, genre, description):
    return f"""
We request you to create a {output_type} of {per_file_length} bars in length, intended for use in Ableton. 
Genre: {genre}
The instrument is {instrument}, played on MIDI channel 9.

Details:
- Tempo: {tempo} bpm
- Time Signature: {time_signature[0]}/{time_signature[1]}

Artistic and Stylistic Guidelines:
{description}

Do not include explanations or commentary. Only output the note data in the specified format.
"""

defaults = {
    "output_type": "drums",
    "instrument": "drum kit",
    "per_file_length": 4,
    "tempo": 80,
    "time_signature": (4, 4),
    "key": "Dminor",  # Key is less relevant for drums but kept for consistency
    "genre": "The piece should be genre-appropriate, resembling the style of electronic or acoustic drum patterns.",
    "description": """
- The loop should be dynamic and rhythmically engaging, with a strong groove.
- Utilize a variety of drum sounds to create a rich texture.
- Vary velocities for natural dynamics and realism. Avoid constant velocities.
- Ensure that the rhythmic content reflects the requested tempo and conveys the intended mood.
"""
} 