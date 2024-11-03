import numpy as np
import librosa

class Tonal_Fragment:
    def __init__(self, waveform, sr, pitch_profiles):
        self.waveform = waveform
        self.sr = sr
        self.pitch_profiles = pitch_profiles
        self.y_segment = self.waveform
        self.chromograph = librosa.feature.chroma_cqt(y=self.y_segment, sr=self.sr, bins_per_octave=12)
        # Sum the chroma features to get the total intensity of each pitch class
        self.chroma_vals = np.sum(self.chromograph, axis=1)
        # Normalize chroma values
        self.chroma_vals = self.chroma_vals / np.sum(self.chroma_vals)
        self.keyfreqs = self.chroma_vals.tolist()
        self.pitch_class_names = ['C', 'C#', 'D', 'D#', 'E',
                                  'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        self.key_dict = self.calculate_correlations()

    def calculate_correlations(self):
        key_dict = {}
        for mode_name, profile in self.pitch_profiles.items():
            for i in range(12):
                rotated_profile = profile[i:] + profile[:i]
                corr = np.corrcoef(self.keyfreqs, rotated_profile)[0, 1]
                note = self.pitch_class_names[i]
                key_name = f"{note} {mode_name}"
                key_dict[key_name] = corr
        return key_dict

    def get_key(self):
        # Select the key with the highest correlation
        key = max(self.key_dict, key=self.key_dict.get)
        return key
