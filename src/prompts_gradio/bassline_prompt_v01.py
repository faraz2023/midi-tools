# src/prompts_gradio/bassline_prompt_v01.py
def get_system_prompt(output_type, per_file_length, genre, instrument, tempo, time_signature, key):
    return f"""
        Rules:

        - Use absolute timing, where 1.0 represents a quarter note. The loop must be exactly {per_file_length} bars long.
        - Tempo: {tempo} bpm, Time Signature: {time_signature[0]}/{time_signature[1]}, Key: {key}.
        - For melodic instruments (MIDI channel 0), use standard note names (e.g., C2, F#3).

        - Output Format:  
        Each line must contain one note event in the following format:
            <start_time> <note_name> <duration> <velocity> <MIDI_channel>
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

        - Ensure that in the note data you generate, no two notes of the same pitch and channel start at the same time. This is necessary for the MIDI export to work.

        Artistic and Stylistic Guidelines:
        - {genre}
        - Instrument: {instrument} (melodic, MIDI channel 0).

        Below are some example formats (do not copy these verbatim, they are for reference ONLY):

        Example Bassline (1 bar) (DO NOT USE FOR ARTISTIC REFERENCE, JUST A TECHNICAL FORMAT EXAMPLE):
        0 C2 0.5 100 0
        0.5 G2 0.25 90 0
        0.75 A2 0.25 85 0
        1 F2 0.5 95 0
        1.5 E2 0.5 90 0
        2 D2 0.75 100 0
        2.75 E2 0.25 85 0
        3 C2 1 100 0

        Currently requested loop type is: {output_type}
        """

def get_prompt(output_type, instrument, per_file_length, tempo, time_signature, key, genre, description):
    return f"""
        We request you to create a {output_type} of {per_file_length} bars in length, intended for use in Ableton.
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

# Default values for the UI
defaults = {
    "output_type": "bassline",
    "instrument": "analog synth",
    "per_file_length": 8,
    "tempo": 110,
    "time_signature": (4, 4),
    "key": "Aminor",
    "genre": "The bassline should be genre-appropriate for melodic techno, with a driving and energetic feel.",
    "description": """
- The bassline should be rhythmically driving and provide a strong foundation for the track.
- Utilize a mix of short, staccato notes and longer, sustained notes to create rhythmic interest.
- Vary velocities for dynamic expression. Emphasize important notes with higher velocities.
- Ensure that the bassline reflects the requested key and works well with the melodic and harmonic content of the track.
"""
}