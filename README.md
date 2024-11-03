# scale-aware

_Sound sample scale detection and labeling written in Python_.

## What's this?

> I have a bunch of samples from every corner on the internet including obscure files and vinyl rips, but they have no key/scale data so it's hard to use them in my productions.

If this is you, read on.

## Concepts

#### Pitch profiles

A pitch intensity profile describes how a scale "looks" statistically, in other words, how likely it is that certain notes appear in it.

This program has predefined pitch profiles, but you can also generate your own.

#### Chroma analysis

The script takes slices of an audio sample and creates a representation of the audio waves called a chroma. Then it uses a simplified version of the Krumhansl-Schmuckler key-finding algorithm, which compares the audio’s chroma data against the predefined pitch profiles.

Currently, it can recognize these scales:

1. Major Scales

   It can detect all 12 major scales: C, C#, D, D#, E, F, F#, G, G#, A, A#, and B major.

2. Minor Scales

   It can detect all 12 natural minor scales (also called Aeolian mode: C minor, C# minor, D minor, and so on through B minor.

3. Modes

   In addition to major and minor, these modes are supported:

   - bebop_major
   - bebop_minor
   - chromatic
   - dorian
   - harmonic minor
   - harmonic_major
   - locrian
   - lydian
   - major pentatonic
   - major_blues
   - melodic_minor
   - minor pentatonic
   - minor_blues
   - mixolydian
   - phrygian

4. No microtonal or non-Western scales: for now, only Western 12-tone scales are supported, so it won’t detect any quarter tones or microtonal nuances.

   However, you can read learn adding **custom profiles** in the Usage section.

5. **Complex** and **simplified** analysis

   By default, **all** built-in profiles are used. To use major and minor only, pass the `-s` flag to the script:

   `python analyze_keys.py [path_to_folder] -s`

## Installation

1. Create a virtual environment

`python3 -m venv myenv`

2. Activate the virtual environment

3. On Windows:

`myenv\Scripts\activate`

4. On macOS and Linux:

`source myenv/bin/activate`

5. Install required packages

`pip install librosa numpy pydub mutagen`

6. Verify installation

`pip list`

7. Save the dependencies to a requirements file

`pip freeze > requirements.txt`

## Usage

### Analyzing a folder of samples

Use the following command, replacing [path_to_folder] with your actual folder path:

`python analyze_keys.py [path_to_folder]`

For example:

`analyze_keys.py /Users/username/Music/Sounds`

Output: The script will rename each file by appending ` - (tag [scale name])`. This convention was invented for easy debugging, and searching/filtering in audio applications, and will become configurable in the future.

For now, sample.wav will become `sample - (tag G Major).wav` if the script detects G major.

### Adding custom profiles

You can easily create your own profiles for other scales and modes:

1. Add a subfolder inside the root `/modes` folder.
2. The name will be used for labeling your files, so make it suitable for file names.
3. Populate the folder with MIDI files that use the scale. The more files, the more statistically precise your profile, so provide as many examples as you can.
4. Execute `python extract_profiles.py modes`. This will populate the `pitch_profiles.json` file in the root and update your scale repertoire.

## Running tests

`python -m unittest discover -s tests`

From your project root directory, use unittest to discover and run tests.

## Roadmap

- Better default profiles
- Extract profiles from audio, not just MIDI
- Custom label formats
- Skipping tagged files is optional
- Better progress indicators
- Confidence scores and tolerance options
- Non-destructive labeling (create new file instead of rename)
- Dry run (no file renaming, just text output)
