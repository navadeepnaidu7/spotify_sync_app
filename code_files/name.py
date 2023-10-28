import argparse
import logging

import spotipy
from spotipy.oauth2 import SpotifyOAuth

logger = logging.getLogger('examples.get_playlists_and_songs')
logging.basicConfig(level='DEBUG')

def get_args():
    parser = argparse.ArgumentParser(description='Get user playlists and their songs')
    return parser.parse_args()

def main():
    args = get_args()
    
    # Define the scopes needed for accessing playlists and their tracks
    scope = "playlist-read-private user-library-read"
    
    # Create a SpotifyOAuth instance
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    
    # Retrieve the user's Spotify ID
    user_id = sp.me()['id']
    
    # Get the user's playlists
    playlists = sp.current_user_playlists()
    
    # Iterate through the playlists
    for playlist in playlists['items']:
        playlist_name = playlist['name']
        print(f'Playlist: {playlist_name}')
        
        # Get the tracks in each playlist
        results = sp.playlist_tracks(playlist['id'])
        
        # Iterate through the tracks in the playlist
        for track in results['items']:
            track_name = track['track']['name']
            print(f'   Track: {track_name}')

if __name__ == '__main__':
    main()
