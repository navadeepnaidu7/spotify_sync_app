import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import argparse
import logging
import spotipy
from spotipy.oauth2 import SpotifyOAuth

logger = logging.getLogger('examples.sync_spotify_youtube')
logging.basicConfig(level=logging.WARNING)

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

def authenticate_youtube():
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        'client_secret.json',
        ['https://www.googleapis.com/auth/youtube.force-ssl']
    )

    credentials = flow.run_local_server(port=8080)
    
    youtube = googleapiclient.discovery.build('youtube', 'v3', credentials=credentials)
    
    return youtube

def create_youtube_playlist(youtube, playlist_name):
    request = youtube.playlists().insert(
        part="snippet,status",
        body={
          "snippet": {
            "title": playlist_name,
            "description": "Playlist created by the Spotify Sync App",
          },
          "status": {
            "privacyStatus": "public",
          }
        }
    )
    response = request.execute()
    return response["id"]

def search_and_add_to_youtube_playlist(youtube, song_name, youtube_playlist_id):
    request = youtube.search().list(
        part="id",
        q=song_name,
        type="video",
        maxResults=1
    )
    response = request.execute()

    if 'items' in response and response['items']:
        video_id = response['items'][0]['id']['videoId']
        add_video_to_playlist(youtube, video_id, youtube_playlist_id)
    else:
        print(f"Song '{song_name}' not found on YouTube.")

def add_video_to_playlist(youtube, video_id, youtube_playlist_id):
    request = youtube.playlistItems().insert(
        part="snippet",
        body={
          "snippet": {
            "playlistId": youtube_playlist_id,
            "resourceId": {
              "kind": "youtube#video",
              "videoId": video_id,
            }
          }
        }
    )
    request.execute()

def main():
    args = get_args()
    
    # Spotify authentication
    scope = "playlist-read-private user-library-read"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    user_id = sp.me()['id']
    
    # Get the user's playlists
    playlists = sp.current_user_playlists()
    
    # Allow the user to select a specific Spotify playlist
    selected_playlist = select_playlist(playlists['items'])
    
    if selected_playlist is None:
        print("Exiting.")
        return
    
    # Print the selected playlist name
    playlist_name = selected_playlist['name']
    print(f"Selected Playlist: {playlist_name}")
    
    # Get the tracks in the selected Spotify playlist
    results = sp.playlist_tracks(selected_playlist['id'])
    
    # Create a list of track names and artist names
    track_list = [f"{track['track']['name']} - {', '.join(artist['name'] for artist in track['track']['artists'])}" for track in results['items']]
    
    # YouTube authentication
    youtube = authenticate_youtube()

    # Create a YouTube playlist with the same name as the selected Spotify playlist
    youtube_playlist_id = create_youtube_playlist(youtube, playlist_name)

    # Iterate through the Spotify track list and add each song to the YouTube playlist
    for song in track_list:
        search_and_add_to_youtube_playlist(youtube, song, youtube_playlist_id)

if __name__ == '__main__':
    main()
