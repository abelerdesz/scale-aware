import os
import sys
import json
from music21 import converter, note, chord
import numpy as np

def get_pitch_class_distribution(midi_file, root_pitch_class):
    pitch_classes = np.zeros(12)
    total_notes = 0

    try:
        score = converter.parse(midi_file)
        for element in score.flat.notesAndRests:
            if isinstance(element, note.Note):
                pc = (element.pitch.pitchClass - root_pitch_class) % 12  # Normalize to root note C (0)
                pitch_classes[pc] += 1
                total_notes += 1
            elif isinstance(element, chord.Chord):
                for n in element.notes:
                    pc = (n.pitch.pitchClass - root_pitch_class) % 12
                    pitch_classes[pc] += 1
                    total_notes += 1
    except Exception as e:
        print(f"Error processing {midi_file}: {e}")

    if total_notes > 0:
        return pitch_classes
    else:
        return None

def note_name_to_pitch_class(note_name):
    pitch_class_names_sharp = {
        'C': 0, 'C#': 1, 'D': 2, 'D#': 3, 'E': 4, 'F': 5,
        'F#': 6, 'G': 7, 'G#': 8, 'A': 9, 'A#': 10, 'B': 11
    }

    enharmonic_equivalents = {
        'DB': 'C#', 'EB': 'D#', 'GB': 'F#', 'AB': 'G#', 'BB': 'A#',
        'D♭': 'C#', 'E♭': 'D#', 'G♭': 'F#', 'A♭': 'G#', 'B♭': 'A#',
        'FB': 'E', 'CB': 'B', 'E#': 'F', 'B#': 'C'
    }

    # Clean up the note name
    note_name = note_name.strip().upper().replace('FLAT', 'B').replace('SHARP', '#')
    note_name = note_name.replace('S', '#').replace('-', '').replace('♭', 'B').replace('♯', '#')

    # Handle enharmonic equivalents
    note_name = enharmonic_equivalents.get(note_name, note_name)

    return pitch_class_names_sharp.get(note_name, None)

def extract_profiles(root_directory):
    profiles = {}
    pitch_class_names = ['C', 'C#', 'D', 'D#', 'E', 'F',
                         'F#', 'G', 'G#', 'A', 'A#', 'B']

    for mode_name in os.listdir(root_directory):
        mode_path = os.path.join(root_directory, mode_name)
        if os.path.isdir(mode_path):
            distributions = []
            for file_name in os.listdir(mode_path):
                if file_name.lower().endswith(('.mid', '.midi')):
                    # Extract root note from file name
                    root_note_name = file_name.split()[0]
                    root_pitch_class = note_name_to_pitch_class(root_note_name)
                    if root_pitch_class is None:
                        print(f"Could not determine root note for file {file_name}")
                        continue
                    midi_file = os.path.join(mode_path, file_name)
                    distribution = get_pitch_class_distribution(midi_file, root_pitch_class)
                    if distribution is not None:
                        distributions.append(distribution)
            if distributions:
                # Aggregate and normalize the distributions
                aggregated = np.sum(distributions, axis=0)
                normalized_profile = aggregated / np.sum(aggregated)
                profiles[mode_name] = {
                    pitch_class_names[i]: round(normalized_profile[i], 4)
                    for i in range(12)
                }
                print(f"Processed mode: {mode_name}, Files: {len(distributions)}")
            else:
                print(f"No valid MIDI files found in mode {mode_name}.")

    if profiles:
        with open('pitch_profiles.json', 'w') as json_file:
            json.dump(profiles, json_file, indent=4)
        print("Pitch profiles have been saved to 'pitch_profiles.json'.")
    else:
        print("No profiles were extracted.")

def main():
    if len(sys.argv) != 2:
        print("Usage: python extract_profiles.py path_to_modes_directory")
        sys.exit(1)

    root_directory = sys.argv[1]
    if not os.path.isdir(root_directory):
        print(f"The directory {root_directory} does not exist.")
        sys.exit(1)

    extract_profiles(root_directory)

if __name__ == "__main__":
    main()
