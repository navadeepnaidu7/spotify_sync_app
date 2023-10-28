import argparse
import logging

import spotipy
from spotipy.oauth2 import SpotifyOAuth

logger = logging.getLogger('examples.select_playlist')
logging.basicConfig(level='DEBUG')

def get_args():
    parser = argparse.ArgumentParser(description='Select a specific playlist to view songs')
    return parser.parse_args()

def select_playlist(playlists):
    print("Your Playlists:")
    for index, playlist in enumerate(playlists):
        print(f"{index + 1}: {playlist['name']}")
    
    while True:
        try:
            choice = int(input("Enter the number of the playlist you want to view or enter 0 to exit: "))
            if choice == 0:
                return None
            elif 1 <= choice <= len(playlists):
                return playlists[choice - 1]
            else:
                print("Invalid choice. Please enter a valid number or 0 to exit.")
        except ValueError:
            print("Invalid input. Please enter a valid number or 0 to exit.")

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
    
    # Allow the user to select a specific playlist
    selected_playlist = select_playlist(playlists['items'])
    
    if selected_playlist is None:
        print("Exiting.")
        return
    
    # Print the selected playlist name
    playlist_name = selected_playlist['name']
    print(f"Selected Playlist: {playlist_name}")
    
    # Get the tracks in the selected playlist
    results = sp.playlist_tracks(selected_playlist['id'])
    
    # Create a list of track names and artist names
    track_list = [f"{track['track']['name']} - {', '.join(artist['name'] for artist in track['track']['artists'])}" for track in results['items']]
    
    while True:
        choice = input("Do you want to view the track list? (yes/no): ")
        if choice.lower() == 'yes':
            print("Track List:")
            for index, track_info in enumerate(track_list):
                print(f"{index + 1}: {track_info}")
            break
        elif choice.lower() == 'no':
            print("Exiting.")
            break
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

if __name__ == '__main__':
    main()
