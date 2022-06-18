import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import find_dotenv, load_dotenv

#Load our Spotipy enviroment variables 
load_dotenv(find_dotenv())
PLAYLIST_ID = '5hwjLoGifPEGBrBmNZxa0X'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="playlist-modify-public,user-library-read"))

    

def getAlbumURI(albumName=None):
    results = sp.search(q = "album:" + albumName, type = "album")

    # get the first album uri
    album_id = results['albums']['items'][0]['uri']
    return album_id.split(":")[2]

def addAlbumToAOTY(albumURI=None):

    albumTracks = sp.album_tracks(albumURI)
    print(albumTracks)
    for y in albumTracks['items']:
        sp.playlist_add_items(PLAYLIST_ID, [y['id']])

def retrieveAlbumsFromPlaylist(playlist):
    results = sp.playlist_tracks(PLAYLIST_ID, limit=10, fields ="added_at")
    print(results)
        
def moveAlbum(albumURI, sourcePlaylist, targetPlaylist):
    pass

def deleteAlbum(albumURI, playlist):
    pass



