import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
from tqdm import tqdm
import os
import json

client_id = os.environ.get('CLIENT_ID')
client_secret = os.environ.get('CLIENT_SECRET')
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Get all the artists from the playlist
playlist_id = '37i9dQZEVXbIQnj7RRhdSX' #Top-50 italy
results = sp.playlist(playlist_id, fields='tracks,next')
tracks = results['tracks']
artists = []
while tracks:
    for item in tracks['items']:
        track = item['track']
        artist = track['artists'][0]
        if artist['name'] not in [x['name'] for x in artists]:
            artists.append({
                'name': artist['name'],
                'id': artist['id']
            })
            
    if tracks['next']:
        tracks = sp.next(tracks)
    else:
        tracks = None

with open('data/choosenArtists.json', 'w') as f:
    json.dump(artists, f)