import mido
import os

def midi_note_to_name(midi_note):
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    octave = (midi_note // 12) - 1
    note = notes[midi_note % 12]
    return f"{note}{octave}"

def midi_to_text(midi_file_path):
    midi = mido.MidiFile(midi_file_path)
    
    # Extract tempo and time signature
    tempo = 120  # Default tempo
    time_signature = (4, 4)  # Default time signature
    ticks_per_beat = midi.ticks_per_beat
    
    for track in midi.tracks:
        for msg in track:
            if msg.type == 'set_tempo':
                tempo = mido.tempo2bpm(msg.tempo)
            elif msg.type == 'time_signature':
                time_signature = (msg.numerator, msg.denominator)

    # Process note events
    notes = []
    
    for track in midi.tracks:
        track_time = 0
        for msg in track:
            track_time += msg.time
            if msg.type == 'note_on' and msg.velocity > 0:
                # Note start
                start_time = track_time / ticks_per_beat
                notes.append([start_time, msg.note, None, msg.velocity, msg.channel])
            elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
                # Note end
                end_time = track_time / ticks_per_beat
                for note in reversed(notes):
                    if note[1] == msg.note and note[2] is None:
                        note[2] = end_time - note[0]
                        break

    # Sort notes by start time
    notes.sort(key=lambda x: x[0])

    # Generate output text
    output_text = f"# Tempo: {tempo:.2f}\n"
    output_text += f"# Time Signature: {time_signature[0]}/{time_signature[1]}\n\n"
    
    for note in notes:
        start_time, pitch, duration, velocity, channel = note
        if duration is not None:
            note_name = midi_note_to_name(pitch)
            output_text += f"{start_time:.2f} {note_name} {duration:.2f} {velocity} {channel}\n"

    return output_text

def midi_file_to_text(midi_file_path, output_file_path=None):
    text_content = midi_to_text(midi_file_path)
    
    if output_file_path:
        with open(output_file_path, 'w') as f:
            f.write(text_content)
        print(f"Text representation saved to {output_file_path}")
    else:
        print(text_content)

# Example usage
if __name__ == "__main__":
    midi_file_path = os.path.join('.', 'MIDI_files', 'E_Melody_felt_full.mid')
    output_file_path = os.path.join('.', 'TEXT_files', 'E_Melody_felt_full.txt')
    
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    
    midi_file_to_text(midi_file_path, output_file_path)