from midiutil import MIDIFile
import re
import os
import math


ABLETON_DRUM_MAP = {
    'kick': 36, 'snare': 38, 'clap': 39, 'closed_hat': 42, 'open_hat': 46,
    'low_tom': 41, 'mid_tom': 47, 'high_tom': 50, 'crash': 49, 'ride': 51
}

NOTE_NAMES = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}

def create_midi_from_text(input_text, filepath, tempo=120, time_signature=(4, 4)):
    output_file = os.path.join(filepath)
    text_to_midi(input_text, output_file, tempo, time_signature)
    print(f"MIDI file '{filepath}' has been created.")


def note_to_midi(note):
    """Convert note name (e.g., 'C4', 'F#5') to MIDI note number."""
    if note.lower() in ABLETON_DRUM_MAP:
        return ABLETON_DRUM_MAP[note.lower()]
    
    match = re.match(r'([A-G])(#|b)?(-?\d+)', note, re.IGNORECASE)
    if not match:
        raise ValueError(f"Invalid note format: {note}")
    
    note, accidental, octave = match.groups()
    midi_note = NOTE_NAMES[note.upper()]
    if accidental == '#':
        midi_note += 1
    elif accidental == 'b':
        midi_note -= 1
    
    return midi_note + (int(octave) + 1) * 12

def parse_note_line(line, current_time=0):
    """Parse a single line of note data, supporting both absolute and relative timing."""
    line = line.strip()
    if line.startswith('#') or not line:
        return None, current_time
    
    parts = line.split()
    if len(parts) < 3 or len(parts) > 5:
        raise ValueError(f"Invalid line format: {line}")
    
    if parts[0] == '+':
        time = current_time + float(parts[1])
        parts = parts[1:]
    else:
        time = float(parts[0])
    
    note = note_to_midi(parts[1])
    duration = float(parts[2])
    velocity = int(parts[3]) if len(parts) > 3 else 100
    channel = int(parts[4]) if len(parts) > 4 else 0
    
    return [time, note, duration, velocity, channel], time

def text_to_midi(input_text, output_file, tempo=120, time_signature=(4, 4)):
    """Convert text-based note sequence to a single MIDI file."""
    midi = MIDIFile(1)  # One track
    midi.addTempo(0, 0, tempo)
    midi.addTimeSignature(0, 0, time_signature[0], int(math.log2(time_signature[1])), 24, 8)


    beats_per_bar = time_signature[0]
    current_time = 0
    print("--------------------------------")
    print(input_text)
    print("--------------------------------")
    for line in input_text.split('\n'):
        try:
            note_data, current_time = parse_note_line(line, current_time)
            if note_data:
                print("!!!! note data: ", note_data)
                time, pitch, duration, velocity, channel = note_data

                #fix time stuff
                time = time/2
                duration = duration/2
                midi.addNote(0, channel, pitch, time, duration, velocity)
        except ValueError as e:
            print(f"Error parsing line: {line}")
            print(f"Error message: {str(e)}")


    print("From text to midi: ", midi.__dict__)
    # recurservily print all the midi parmters in __dict__ and inner __dict__
    for key, value in midi.__dict__.items():
        print(f"{key}: {value}")
        if isinstance(value, dict):
            for inner_key, inner_value in value.items():
                print(f"  {inner_key}: {inner_value}")
    with open(output_file, "wb") as output_file:
        midi.writeFile(output_file)