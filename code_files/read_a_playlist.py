from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import json

client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

playlist_id = 'https://open.spotify.com/playlist/1pBcJvVkK6IqCkwNr5JszR?si=e74d8edf93b343c3'
results = sp.playlist(playlist_id)
print(json.dumps(results, indent=4))