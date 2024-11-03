import unittest
from unittest.mock import patch, MagicMock
import numpy as np
import tonal_fragment

class TestTonalFragment(unittest.TestCase):

    @patch('tonal_fragment.librosa.feature.chroma_cqt')
    def test_calculate_correlations(self, mock_chroma_cqt):
        # Mock chroma features with varying values
        mock_chroma = np.tile(np.arange(1, 13).reshape(12, 1), (1, 3))
        mock_chroma_cqt.return_value = mock_chroma

        waveform = np.array([0.1, 0.2, 0.3])
        sr = 22050
        pitch_profiles = {
            'major': [0.5 if i in [0, 4, 7] else 0.05 for i in range(12)],  # Emphasize C, E, G
            'minor': [0.5 if i in [9, 0, 4] else 0.05 for i in range(12)],  # Emphasize A, C, E
        }

        # Normalize profiles
        for key in pitch_profiles:
            total = sum(pitch_profiles[key])
            pitch_profiles[key] = [v / total for v in pitch_profiles[key]]

        tf = tonal_fragment.Tonal_Fragment(waveform, sr, pitch_profiles)
        key_dict = tf.calculate_correlations()

        # Expected correlations
        expected_correlations = {}
        for mode_name, profile in pitch_profiles.items():
            for i in range(12):
                rotated_profile = profile[i:] + profile[:i]
                corr = np.corrcoef(tf.keyfreqs, rotated_profile)[0, 1]
                note = tf.pitch_class_names[i]
                key_name = f"{note} {mode_name}"
                expected_correlations[key_name] = corr

        # Assert that the calculated correlations match expected values
        for key_name in expected_correlations:
            if np.isnan(expected_correlations[key_name]):
                self.assertTrue(np.isnan(key_dict[key_name]), f"Expected nan for {key_name}")
            else:
                self.assertAlmostEqual(key_dict[key_name], expected_correlations[key_name], places=7, msg=f"Correlation mismatch for {key_name}")

if __name__ == '__main__':
    unittest.main()
