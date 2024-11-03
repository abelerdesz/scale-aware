import unittest
from unittest.mock import patch, MagicMock
import os
import analyze_keys
import numpy as np

class TestAnalyzeKeys(unittest.TestCase):

    @patch('analyze_keys.load_pitch_profiles')
    @patch('analyze_keys.detect_key')
    @patch('analyze_keys.shutil.move')
    @patch('os.listdir')
    @patch('os.path.isdir')
    def test_analyze_and_rename_files(self, mock_isdir, mock_listdir, mock_move, mock_detect_key, mock_load_profiles):
        # Setup
        mock_isdir.return_value = True
        mock_listdir.return_value = ['test1.mp3', 'test2.wav', 'test3.txt']
        mock_detect_key.side_effect = ['C# major', 'A# minor', None]
        mock_load_profiles.return_value = {'dummy_mode': [0]*12}  # Return a dummy profile

        directory = 'test_directory'

        # Call the function
        analyze_keys.analyze_and_rename_files(directory)

        # Assertions
        mock_detect_key.assert_any_call(os.path.join(directory, 'test1.mp3'), mock_load_profiles.return_value)
        mock_detect_key.assert_any_call(os.path.join(directory, 'test2.wav'), mock_load_profiles.return_value)
        self.assertEqual(mock_detect_key.call_count, 2)  # Only audio files should be processed

        # Adjust expected new filenames to match the shortened key labels and sharp notation
        mock_move.assert_any_call(
            os.path.join(directory, 'test1.mp3'),
            os.path.join(directory, 'test1 - C#maj.mp3')
        )
        mock_move.assert_any_call(
            os.path.join(directory, 'test2.wav'),
            os.path.join(directory, 'test2 - A#min.wav')
        )
        self.assertEqual(mock_move.call_count, 2)  # Only renamed files should be moved

    @patch('analyze_keys.librosa.load')
    @patch('analyze_keys.Tonal_Fragment')
    def test_detect_key(self, mock_tonal_fragment, mock_librosa_load):
        mock_waveform = np.array([0.1, 0.2, 0.3])  # Example waveform data
        mock_librosa_load.return_value = (mock_waveform, 22050)  # Return mock waveform data
        mock_tonal_fragment_instance = mock_tonal_fragment.return_value
        mock_tonal_fragment_instance.get_key.return_value = 'C# major'

        file_path = 'test1.mp3'
        pitch_profiles = {'dummy_mode': [0]*12}

        key = analyze_keys.detect_key(file_path, pitch_profiles)

        mock_librosa_load.assert_called_once_with(file_path, sr=None)
        mock_tonal_fragment.assert_called_once_with(mock_waveform, 22050, pitch_profiles)  # Ensure Tonal_Fragment constructor is called with correct args
        mock_tonal_fragment_instance.get_key.assert_called_once()  # Assert that get_key() is called
        self.assertEqual(key, 'C# major')

    @patch('shutil.move')
    def test_rename_file_with_key(self, mock_move):
        directory = 'test_directory'
        file = 'test1.mp3'
        key = 'C# major'

        analyze_keys.rename_file_with_key(directory, file, key)

        old_file_path = os.path.join(directory, file)
        new_file_path = os.path.join(directory, 'test1 - C#maj.mp3')

        mock_move.assert_called_once_with(old_file_path, new_file_path)

if __name__ == '__main__':
    unittest.main()
