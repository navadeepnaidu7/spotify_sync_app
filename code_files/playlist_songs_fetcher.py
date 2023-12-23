import os
from redis import UsernamePasswordCredentialProvider
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors


# Retrieve API credentials from environment variables
client_id = os.environ.get("SPOTIPY_CLIENT_ID")
client_secret = os.environ.get("SPOTIPY_CLIENT_SECRET")
redirect_uri = os.environ.get("SPOTIPY_REDIRECT_URI")

# Authenticate with Spotify
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Set up YouTube API environment variables
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\navad\Downloads\client_secrets.json"   # Replace with your credentials path

# Authenticate with YouTube
scopes = ["https://www.googleapis.com/auth/youtube"]
client_secrets_file = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
   client_secrets_file, scopes=scopes
)
credentials = flow.run_local_server(port=0)
youtube = googleapiclient.discovery.build("youtube", "v3", credentials=credentials)

# Get user's authorization
scope = "playlist-read-private"
token = spotipy.util.prompt_for_user_token(client_id=client_id,
                                          client_secret=client_secret,
                                          redirect_uri=redirect_uri,
                                          scope=scope)
if token:
   sp = spotipy.Spotify(auth=token)
else:
   print("Can't get token for", UsernamePasswordCredentialProvider)

# Get user's playlists
playlists = sp.current_user_playlists()

# Display available playlists
print("Your Playlists:")
for i, playlist in enumerate(playlists['items']):
   print(f"{i + 1}. {playlist['name']}")

# Ask user to select a playlist
selected_playlist_index = int(input("Select a playlist by number: ")) - 1
selected_playlist_id = playlists['items'][selected_playlist_index]['id']

# Retrieve tracks from the selected playlist
playlist_tracks = sp.playlist_tracks(selected_playlist_id)

# Display song names with artist names
print("Songs in the playlist:")
for track in playlist_tracks['items']:
   song_name = track['track']['name']
   artist_name = track['track']['artists'][0]['name']
   print(f"- {song_name} - {artist_name}")

   # Create a new YouTube playlist
request = youtube.playlists().insert(
    part="snippet,status",
    body={
        "snippet": {
            "title": playlists['items'][selected_playlist_index]['name'],
            "description": "Playlist transferred from Spotify Created By Navadeep Naidu"
        },
        "status": {
            "privacyStatus": "PUBLIC"  # Adjust privacy if needed
        }
    }
)
playlist_response = request.execute()
youtube_playlist_id = playlist_response["id"]

# Search for songs on YouTube and add to playlist
for track in playlist_tracks['items']:
    song_name = track['track']['name']
    artist_name = track['track']['artists'][0]['name']

    search_request = youtube.search().list(
        part="snippet",
        q=f"{song_name} {artist_name}",
        maxResults=1,  # Retrieve only the top result
        type="VIDEO"
    )
    search_response = search_request.execute()

    if search_response["items"]:
        video_id = search_response["items"][0]["id"]["videoId"]
        add_video_request = youtube.playlistItems().insert(
            part="snippet",
            body={
                "snippet": {
                    "playlistId": youtube_playlist_id,
                    "resourceId": {
                        "kind": "youtube#video",
                        "videoId": video_id
                    }
                }
            }
        )
        try:
            add_video_request.execute()
            print(f"Added '{song_name} - {artist_name}' to YouTube playlist")
        except googleapiclient.errors.HttpError as error:
            print(f"Error adding video: {error}")
    else:
        print(f"Song '{song_name} - {artist_name}' not found on YouTube")
