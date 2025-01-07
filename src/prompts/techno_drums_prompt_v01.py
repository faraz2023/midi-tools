output_type = 'drums'
instrument = "Ableton Drum Rack with techno drum samples"  
per_file_length = 8
tempo = 110
time_signature = (4, 4)
genre = "The drum pattern should be genre-appropriate for techno, with a steady four-on-the-floor kick and energetic percussion."

description = f"""
- The drum loop should have a strong, driving rhythm with a consistent kick on every downbeat.
- Include hi-hats, snares, claps, and other percussion to create a rich, layered groove. 
- Vary velocities and use subtle swing to humanize the pattern and add interest.
- Ensure the overall rhythm and energy level matches the intended tempo of {tempo} bpm.
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

- Ensure that in the note data you generate, no two notes of the same pitch and channel start at the same time. This is necessary for the MIDI export to work.

Artistic and Stylistic Guidelines:
- {genre}
- Instrument: {instrument} (drums, MIDI channel 9).

Currently requested loop type is: {output_type}  
"""

prompt = f"""
We request you to create a {output_type} pattern of {per_file_length} bars in length, intended for use in Ableton.
Genre: {genre}
The instrument is {instrument}, played on MIDI channel 9.

Details: 
- Tempo: {tempo} bpm
- Time Signature: {time_signature[0]}/{time_signature[1]}

Artistic and Stylistic Guidelines:
- {description}

Do not include explanations or commentary. Only output the note data in the specified format.
""" 