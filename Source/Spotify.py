import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import find_dotenv, load_dotenv

#Load our Spotipy enviroment variables 
load_dotenv(find_dotenv())
AOTY_PLAYLIST_ID = '5hwjLoGifPEGBrBmNZxa0X'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="playlist-modify-public,user-library-read"))

class Album:
    """Class for holding an album object
    """
    def __init__(self, artist = None, name = None, uri = None, img = None):
        self.artist = artist
        self.uri = uri
        self.name = name
        self.img = img


def getAlbumURI(albumName=None):
    """Gets the URI for a single album

    Args:
        albumName (string): Name of the album to search for. Defaults to None.

    Returns:
        stringlike: URI of found album
    """
    results = sp.search(q = "album:" + albumName, type = "album")

    # get the first album uri
    album_id = results['albums']['items'][0]['uri']
    return album_id.split(":")[2]

def addAlbumToPlaylist(albumURI = None, playlist = None):
    """Add an album to a playlist given their respective ids

    Args:
        albumURI : URI of the album. Defaults to None.
        playlist : ID of the playlist. Defaults to None.
    """
    albumTracks = sp.album_tracks(albumURI)
    print(albumTracks)
    for y in albumTracks['items']:
        sp.playlist_add_items(playlist, [y['id']])

def retrieveAlbumsFromPlaylist(playlist):
    albumOffset = 0
    albumList = []
    results = sp.playlist_tracks(playlist, limit=5, offset=albumOffset, fields="items(track(album(id)))")
    print(results)
        
def moveAlbum(albumURI, sourcePlaylist, targetPlaylist):
    pass

def deleteAlbum(albumURI, playlist):
    pass



