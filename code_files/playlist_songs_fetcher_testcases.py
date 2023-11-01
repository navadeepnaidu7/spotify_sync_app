import unittest
from unittest.mock import patch
import io
from playlist_songs_fetcher import select_playlist, main

class TestSelectPlaylist(unittest.TestCase):
    @patch('builtins.input', side_effect=["1"])
    def test_select_valid_playlist(self, mock_input):
        playlists = [{'name': 'Playlist 1'}, {'name': 'Playlist 2'}]
        selected = select_playlist(playlists)
        self.assertEqual(selected, playlists[0])

    @patch('builtins.input', side_effect=["0"])
    def test_select_exit(self, mock_input):
        playlists = [{'name': 'Playlist 1'}, {'name': 'Playlist 2'}]
        selected = select_playlist(playlists)
        self.assertEqual(selected, None)

    @patch('builtins.input', side_effect=["3", "2"])
    def test_select_invalid_then_valid_playlist(self, mock_input):
        playlists = [{'name': 'Playlist 1'}, {'name': 'Playlist 2'}]
        selected = select_playlist(playlists)
        self.assertEqual(selected, playlists[1])

class TestMain(unittest.TestCase):
    @patch('builtins.input', return_value="no")
    def test_main_no_track_list(self, mock_input):
        with patch('sys.stdout', new_callable=io.StringIO) as mock_output:
            main()
            output = mock_output.getvalue()
        self.assertIn("Exiting.", output)
        self.assertNotIn("Track List:", output)

if __name__ == '__main__':
    unittest.main()
