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




if __name__ == "__main__":
    # Example 1: Simple melody
    text_input = """
0 kick 0.25 110 9
1 clap 0.25 90 9
2 kick 0.25 100 9
2.5 closed_hat 0.25 80 9
3 clap 0.25 85 9
3.5 closed_hat 0.25 75 9
4 kick 0.25 105 9
5 clap 0.25 88 9
6 kick 0.25 98 9
6.5 closed_hat 0.25 78 9
7 clap 0.25 82 9
7.5 open_hat 0.25 70 9
8 kick 0.25 108 9
9 clap 0.25 92 9
10 kick 0.25 102 9
10.5 closed_hat 0.25 82 9
11 clap 0.25 87 9
11.5 closed_hat 0.25 77 9
12 kick 0.25 107 9
13 clap 0.25 91 9
14 kick 0.25 101 9
14.5 closed_hat 0.25 81 9
15 clap 0.25 86 9
15.5 open_hat 0.25 72 9
16 kick 0.25 112 9
17 clap 0.25 94 9
18 kick 0.25 104 9
18.5 closed_hat 0.25 84 9
19 clap 0.25 89 9
19.5 closed_hat 0.25 79 9
20 kick 0.25 109 9
21 clap 0.25 93 9
22 kick 0.25 103 9
22.5 closed_hat 0.25 83 9
23 clap 0.25 88 9
23.5 open_hat 0.25 74 9
24 kick 0.25 111 9
25 clap 0.25 95 9
26 kick 0.25 105 9
26.5 closed_hat 0.25 85 9
27 clap 0.25 90 9
27.5 closed_hat 0.25 80 9
28 kick 0.25 110 9
29 clap 0.25 96 9
30 kick 0.25 106 9
30.5 closed_hat 0.25 86 9
31 clap 0.25 91 9
31.5 open_hat 0.25 76 9
    """
    create_midi_from_text(text_input, "V_waves_drums_c01_1.mid", tempo=80)
