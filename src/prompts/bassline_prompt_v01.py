output_type = 'bassline'
instrument = "analog synth"
per_file_length = 8
tempo = 110
time_signature = (4, 4)
key = 'Aminor'
genre = "The bassline should be genre-appropriate for melodic techno, with a driving and energetic feel."

description = f"""
- The bassline should be rhythmically driving and provide a strong foundation for the track.
- Utilize a mix of short, staccato notes and longer, sustained notes to create rhythmic interest.
- Vary velocities for dynamic expression. Emphasize important notes with higher velocities.
- Ensure that the bassline reflects the requested key of {key} and works well with the melodic and harmonic content of the track.
- The bassline should be in the key of {key}.
"""

system_prompt = f"""
Rules:

- Use absolute timing, where 1.0 represents a quarter note. The loop must be exactly {per_file_length} bars long.
- Tempo: {tempo} bpm, Time Signature: {time_signature[0]}/{time_signature[1]}, Key: {key}.
- For melodic instruments (MIDI channel 0), use standard note names (e.g., C2, F#3).

- Output Format:  
Each line must contain one note event in the following format:
    <start_time> <note_name> <duration> <velocity> <MIDI_channel>
- <start_time> is in bar-relative units, where 0.0 is the start of the loop.
- <duration> is the length of the note in quarter-note units.
- <velocity> is an integer velocity value.
- <MIDI_channel> is 0 for melodic instruments.

- Do not include explanations, comments, or extra text. Only provide note events.

- Ensure that in the note data you generate, no two notes of the same pitch and channel start at the same time. This is necessary for the MIDI export to work.

Artistic and Stylistic Guidelines:
- {genre}
- Instrument: {instrument} (melodic, MIDI channel 0).

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

Do not include explanations or commentary. Only output the note data in the specified format.
""" 