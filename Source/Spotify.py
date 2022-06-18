import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import find_dotenv, load_dotenv

#Load our Spotipy enviroment variables 
load_dotenv(find_dotenv())
PLAYLIST_ID = '5hwjLoGifPEGBrBmNZxa0X'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="playlist-modify-public,user-library-read"))

    # for x in albumList:
    #     spotifyAlbumList = spotifyInterface.album(x)

    # for x in albumList:
    #     album = spotifyInterface.album_tracks(x)
    #     for y in album['items']:
    #         spotifyInterface.playlist_add_items(PLAYLIST_ID, [y['id']])

def getAlbumURI(albumName=None):
    results = sp.search(q = "album:" + albumName, type = "album")

    # get the first album uri
    album_id = results['albums']['items'][0]['uri']
    print(album_id.split(":")[2])
