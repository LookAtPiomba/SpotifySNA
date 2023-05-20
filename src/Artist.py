import itertools
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os, json

client_id = os.environ.get('CLIENT_ID')
client_secret = os.environ.get('CLIENT_SECRET')
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

class Artist:
    def __init__(self, id:str, name:str) -> None:
        self.id = id
        self.name = name
        self.collaborators = self.getCollaborators()
        self.genres = self.getGenres()

    def getTracks(self) -> list:
        tracks = []
        albums = sp.artist_albums(self.id, album_type='album', country='it')
        singles = sp.artist_albums(self.id, album_type='single', country='it')
        songs = albums['items'] + singles['items']

        for song in songs:
            album_tracks = sp.album_tracks(song['id'])
            tracks.extend(album_tracks['items'])
        
        return tracks
                
    def getCollaborators(self) -> dict:
        collaborators = {}
        tracks = self.getTracks()
        # Now access the list of tracks
        for track in tracks:
            featured_artists = track['artists']
            for featured_artist in featured_artists:
                if featured_artist['name'] not in featured_artists:
                    collaborators[featured_artist['name']] =  featured_artist['id']
        return collaborators

    def getGenres(self) -> None:
        artist = sp.artist(self.id)
        return list(artist['genres'])

    def jsonize(self):
        artist_json = {
            'id': self.id,
            'name': self.name,
            'genres': len(self.genres),
            'collaborators': list(self.collaborators.keys())
        }
        return artist_json
