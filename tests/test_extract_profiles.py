import unittest
from unittest.mock import patch, MagicMock
import extract_profiles
import numpy as np

class TestExtractProfiles(unittest.TestCase):

    @patch('json.dump')
    @patch('extract_profiles.get_pitch_class_distribution')
    @patch('extract_profiles.os.listdir')
    @patch('extract_profiles.os.path.isdir')
    @patch('extract_profiles.note_name_to_pitch_class')
    def test_extract_profiles(self, mock_note_name_to_pitch_class, mock_isdir, mock_listdir, mock_get_distribution, mock_json_dump):
        # Setup mocks
        mock_isdir.return_value = True
        mock_listdir.side_effect = [
            ['major'],  # First call: modes directories
            ['C major scale.mid', 'D major scale.mid'],  # Second call: files in 'major' directory
        ]
        mock_note_name_to_pitch_class.side_effect = [0, 2]  # C:0, D:2
        mock_get_distribution.side_effect = [
            np.array([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),  # For C major
            np.array([0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]),  # For D major (transposed to C)
        ]

        expected_aggregated = np.array([1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        expected_normalized = expected_aggregated / np.sum(expected_aggregated)
        expected_profile = {
            'C': round(expected_normalized[0], 4),
            'C#': round(expected_normalized[1], 4),
            'D': round(expected_normalized[2], 4),
            'D#': round(expected_normalized[3], 4),
            'E': round(expected_normalized[4], 4),
            'F': round(expected_normalized[5], 4),
            'F#': round(expected_normalized[6], 4),
            'G': round(expected_normalized[7], 4),
            'G#': round(expected_normalized[8], 4),
            'A': round(expected_normalized[9], 4),
            'A#': round(expected_normalized[10], 4),
            'B': round(expected_normalized[11], 4),
        }

        # Call the function
        extract_profiles.extract_profiles('modes_directory')

        # Assert that json.dump was called with the expected data
        mock_json_dump.assert_called_once()
        args, kwargs = mock_json_dump.call_args
        data_written = args[0]  # This is the data passed to json.dump
        # Assert the profile matches expected values
        self.assertIn('major', data_written)
        self.assertEqual(data_written['major'], expected_profile)

if __name__ == '__main__':
    unittest.main()
