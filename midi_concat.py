import os
import sys
from mido import MidiFile, MidiTrack, Message, MetaMessage

def concatenate_midis(folder_path):
    # List all .mid files in the folder
    midi_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.mid')]
    
    # Exclude final.mid if it exists
    midi_files = [f for f in midi_files if f.lower() != 'final.mid']
    
    # If no MIDI files found, exit
    if not midi_files:
        print("No MIDI files found in the specified folder.")
        return
    
    # Sort the files numerically by their prefix before ".mid"
    # Assuming files are named like "1.mid", "2.mid", etc.
    # We'll try to parse the leading number. If it fails, use the string sort.
    def numeric_key(x):
        try:
            return int(os.path.splitext(x)[0])
        except ValueError:
            return x
    
    midi_files.sort(key=numeric_key)
    
    # Read the first MIDI file to extract initial tempo and time signature
    first_midi_path = os.path.join(folder_path, midi_files[0])
    first_midi = MidiFile(first_midi_path)
    
    initial_tempo = None
    initial_time_signature = None
    
    # Extract initial tempo and time signature from the first track of the first file
    for msg in first_midi.tracks[0]:
        if msg.type == 'set_tempo' and initial_tempo is None:
            initial_tempo = msg.tempo
        if msg.type == 'time_signature' and initial_time_signature is None:
            initial_time_signature = (msg.numerator, msg.denominator, msg.clocks_per_click, msg.notated_32nd_notes_per_beat)
        # If we found both already, we can break early
        if initial_tempo is not None and initial_time_signature is not None:
            break
    
    # Create a new MidiFile for the final output
    final_midi = MidiFile(type=first_midi.type)
    final_track = MidiTrack()
    final_midi.tracks.append(final_track)
    
    # Insert the initial tempo and time signature into the final track
    if initial_time_signature is not None:
        final_track.append(MetaMessage('time_signature',
                                       numerator=initial_time_signature[0],
                                       denominator=initial_time_signature[1],
                                       clocks_per_click=initial_time_signature[2],
                                       notated_32nd_notes_per_beat=initial_time_signature[3],
                                       time=0))
    if initial_tempo is not None:
        final_track.append(MetaMessage('set_tempo', tempo=initial_tempo, time=0))
    
    # Now, append the messages from all midi files in sequence
    # We will not repeat tempo or time signature changes from other files
    # Just note_on, note_off, and other non-tempo/time-signature events.
    for midi_name in midi_files:
        midi_path = os.path.join(folder_path, midi_name)
        midi = MidiFile(midi_path)
        # Append all tracks. Typically you'd expect a single main track, but we will combine them
        # by simply appending. If you need only a specific track, adjust accordingly.
        for track in midi.tracks:
            for msg in track:
                # Skip tempo and time_signature events from subsequent files
                if msg.type in ('set_tempo', 'time_signature'):
                    continue
                # Append all other messages (note_on, note_off, etc.)
                final_track.append(msg.copy(time=msg.time))
                
    # Save the final file
    final_path = os.path.join(folder_path, "final.mid")
    final_midi.save(final_path)
    print(f"Concatenation complete. The final MIDI file is saved at: {final_path}")

if __name__ == "__main__":
    folder = os.path.join('.', 'MIDI_files_v02', 'ocean_whisper')
    concatenate_midis(folder)
