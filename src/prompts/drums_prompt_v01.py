output_type = 'drums'
instrument = "drum kit"
per_file_length = 4
tempo = 80
time_signature = (4, 4)
key = 'Dminor'  # Key is less relevant for drums but kept for consistency
genre = "The piece should be genre-appropriate, resembling the style of electronic or acoustic drum patterns."

description = f"""
- The loop should be dynamic and rhythmically engaging, with a strong groove.
- Utilize a variety of drum sounds to create a rich texture.
- Vary velocities for natural dynamics and realism. Avoid constant velocities.
- Ensure that the rhythmic content reflects the requested tempo and conveys the intended mood.
"""

system_prompt = f"""
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
- <duration> is the length of the note in quarter-note units.
- <velocity> is an integer velocity value.
- <MIDI_channel> is 9 for drums.

- Do not include explanations, comments, or extra text. Only provide note events.

- Ensure ensure that in the note data you generate, no two notes of the same pitch and channel start at the same time. This is necessary for the midi export work.


Artistic and Stylistic Guidelines:
- {genre}
- Instrument: {instrument} (drums, MIDI channel 9).


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

Currently requested loop type is: {output_type}
"""

prompt = f"""
We request you to create a {output_type} of {per_file_length} bars in length, intended for use in Ableton. 
Genre: {genre}
The instrument is {instrument}, played on MIDI channel 9.

Details:
- Tempo: {tempo} bpm
- Time Signature: {time_signature[0]}/{time_signature[1]}

Artistic and Stylistic Guidelines:
- {description}

Do not include explanations or commentary. Only output the note data in the specified format.
"""