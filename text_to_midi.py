from midiutil import MIDIFile
import re
import os
import math

EXPORT_PATH = os.path.join('.', 'MIDI_files')
os.makedirs(EXPORT_PATH, exist_ok=True)

# Ableton Live default drum mapping
ABLETON_DRUM_MAP = {
    'kick': 36, 'snare': 38, 'clap': 39, 'closed_hat': 42, 'open_hat': 46,
    'low_tom': 41, 'mid_tom': 47, 'high_tom': 50, 'crash': 49, 'ride': 51
}

NOTE_NAMES = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}

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

    current_time = 0
    for line in input_text.split('\n'):
        try:
            note_data, current_time = parse_note_line(line, current_time)
            if note_data:
                time, pitch, duration, velocity, channel = note_data
                midi.addNote(0, channel, pitch, time, duration, velocity)
        except ValueError as e:
            print(f"Error parsing line: {line}")
            print(f"Error message: {str(e)}")

    with open(output_file, "wb") as output_file:
        midi.writeFile(output_file)

# Example usage
def create_midi_from_text(input_text, filename, tempo=120, time_signature=(4, 4)):
    output_file = os.path.join(EXPORT_PATH, filename)
    text_to_midi(input_text, output_file, tempo, time_signature)
    print(f"MIDI file '{filename}' has been created.")


if __name__ == "__main__":
    # Example 1: Simple melody
    text_input = """
0 A3 2.0 40 0
2 C4 1.0 45 0
3 E4 2.0 50 0
5 A3 0.5 55 0
5.5 C4 0.5 50 0
6 E4 1.0 55 0
7 G4 1.0 60 0
8 A4 2.0 65 0
10 E4 0.75 60 0
10.75 G4 0.25 65 0
11 A4 1.0 70 0
12 C5 1.5 75 0
13.5 B4 0.25 70 0
13.75 A4 0.25 65 0
14 G4 1.0 60 0
15 E4 1.0 55 0
16 A3 1.5 50 0
17.5 C4 0.25 55 0
17.75 E4 0.25 60 0
18 A4 2.0 65 0
20 G4 0.5 60 0
20.5 E4 0.5 55 0
21 C4 1.0 50 0
22 D4 1.0 55 0
23 E4 1.5 60 0
24.5 G4 0.75 65 0
25.25 A4 0.75 70 0
26 C5 1.0 75 0
27 B4 0.5 70 0
27.5 A4 0.5 65 0
28 G4 1.0 60 0
29 E4 1.0 55 0
30 A3 1.5 50 0
31.5 B3 0.25 55 0
31.75 C4 0.25 60 0
32 E4 2.0 65 0
34 A4 0.75 70 0
34.75 G4 0.25 65 0
35 E4 1.0 60 0
36 C4 1.0 55 0
37 D4 1.5 60 0
38.5 E4 0.75 65 0
39.25 G4 0.75 70 0
40 A4 2.0 75 0
42 C5 0.5 80 0
42.5 B4 0.5 75 0
43 A4 1.0 70 0
44 G4 1.0 65 0
45 E4 1.5 60 0
46.5 C4 0.25 55 0
46.75 D4 0.25 60 0
47 E4 1.0 65 0
48 A4 2.0 70 0
50 G4 0.75 65 0
50.75 E4 0.25 60 0
51 C4 1.0 55 0
52 D4 1.0 60 0
53 E4 1.5 65 0
54.5 G4 0.75 70 0
55.25 A4 0.75 75 0
56 C5 1.0 80 0
57 E5 0.5 85 0
57.5 D5 0.5 80 0
58 B4 1.0 75 0
59 G4 1.0 70 0
60 A4 3.0 65 0
63 G4 0.5 60 0
63.5 E4 0.5 55 0
    """
    create_midi_from_text(text_input, "V_waves_melody_1.mid", tempo=90)



