#!/usr/bin/env python3

import os
import argparse
import shutil
import numpy as np
import librosa
import json
import re

# Import the Tonal_Fragment class
from tonal_fragment import Tonal_Fragment

def load_pitch_profiles(simplified=False):
    # Adjust the function to locate 'pitch_profiles.json' relative to the script's location
    script_dir = os.path.dirname(os.path.realpath(__file__))
    profiles_path = os.path.join(script_dir, 'pitch_profiles.json')
    with open(profiles_path, 'r') as json_file:
        pitch_profiles = json.load(json_file)
    # Convert pitch names to indices for easier processing
    profiles = {}
    for mode_name, profile in pitch_profiles.items():
        if not simplified or mode_name in ['major', 'minor']:
            profiles[mode_name] = [profile[note] for note in ['C', 'C#', 'D', 'D#', 'E',
                                                              'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']]
    return profiles

def detect_key(file_path, pitch_profiles):
    try:
        waveform, sr = librosa.load(file_path, sr=None)
        if isinstance(waveform, np.ndarray):
            tonal_fragment = Tonal_Fragment(waveform, sr, pitch_profiles)
            key = tonal_fragment.get_key()
            return key
        else:
            raise ValueError("Audio data is not a NumPy array")
    except Exception as e:
        print(f"Error detecting key for {file_path}: {e}")
        return None

def get_new_filename(original_filename, key_info):
    """
    Generates a new filename based on the specified naming convention.
    Modify this function to change the naming convention.
    """
    base, ext = os.path.splitext(original_filename)
    # Shorten key labels (e.g., G#maj or Abmin)
    if ' ' in key_info:
        note, mode = key_info.split(' ', 1)
        mode_abbr = {'major': 'maj', 'minor': 'min'}
        key_info = f"{note}{mode_abbr.get(mode, mode)}"
    new_filename = f"{base} - (tag {key_info}){ext}"
    return new_filename

def is_file_tagged(filename):
    """
    Checks if the file is already tagged using the naming convention.
    """
    pattern = r' - \(tag .+\)\.[^.]+$'
    return re.search(pattern, filename) is not None

def rename_file_with_key(directory, file, key):
    new_filename = get_new_filename(file, key)
    old_file_path = os.path.join(directory, file)
    new_file_path = os.path.join(directory, new_filename)
    shutil.move(old_file_path, new_file_path)
    print(f"Renamed {file} to {new_filename}")

def analyze_and_rename_files(directory, simplified=False):
    pitch_profiles = load_pitch_profiles(simplified=simplified)
    if simplified:
        print("Using simplified analysis mode (only 'major' and 'minor' profiles).")
    else:
        print("Using all mode profiles for analysis.")
    files = [f for f in os.listdir(directory) if f.lower().endswith(('.wav', '.mp3'))]
    total_files = len(files)
    for idx, file in enumerate(files, 1):
        if is_file_tagged(file):
            print(f"Skipping already tagged file: {file}")
            continue
        print(f"Processing file {idx}/{total_files}: {file}")
        file_path = os.path.join(directory, file)
        key = detect_key(file_path, pitch_profiles)
        if key:
            rename_file_with_key(directory, file, key)
        else:
            print(f"Could not detect key for {file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze and rename audio files with their musical key.")
    parser.add_argument(
        "directory",
        type=str,
        nargs='?',
        default='.',
        help="Directory containing the audio files (default: current directory)"
    )
    parser.add_argument(
        "-s",
        "--simplified",
        action="store_true",
        help="Use simplified analysis mode (only 'major' and 'minor' profiles)"
    )
    args = parser.parse_args()

    directory_path = args.directory
    simplified = args.simplified

    if os.path.isdir(directory_path):
        analyze_and_rename_files(directory_path, simplified=simplified)
    else:
        print(f"The directory {directory_path} does not exist.")
