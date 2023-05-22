from Artist import Artist
import json
from tqdm import tqdm

def getPlaylistArtists():
    with open('data/playlistArtists.json', 'r', encoding="utf8") as f:
        playlistArtists = json.load(f)
        return playlistArtists

def createArtist(id:str, name:str) -> Artist:
    artist = Artist(id, name)
    return artist

def createFirstLevelArtists():
    choosenArtists = getPlaylistArtists()
    artists = []
    collaborators = []
    for a in tqdm(choosenArtists, total=len(choosenArtists)):
        print(f'------ {a["name"]} -----')
        artist = createArtist(id=a['id'], name=a['name'])
        artists.append(artist.jsonize())
        for c in artist.collaborators:
            if (c['name'] not in [x['name'] for x in collaborators]) and (c['name'] not in [x['name'] for x in artists]):
                collaborators.append(c)
    
    with open('data/secondLevelArtists.json', 'a') as jf:
        json.dump(collaborators, jf)
    
    return artists, collaborators

def createSecondLevelArtists(artists, collaborators):
    for a in tqdm(collaborators, total=len(collaborators)):
        if a['name'] not in [x['name'] for x in artists]:
            print(f'------ {a["name"]} -----')
            artist = createArtist(id=a['id'], name=a['name'])
            artists.append(artist.jsonize())
    
    with open ('data/artists.json', 'w') as f:
        json.dump(artists, f)
    
def main():
    artists, collaborators = createFirstLevelArtists()
    original_len = len(artists)
    createSecondLevelArtists(artists, collaborators)
    print(f'Total of {len(artists)} artists made by {original_len} first level artists + {len(collaborators)} second level artists')

if __name__ == "__main__":
    main()

    

