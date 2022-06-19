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
    def __init__(self, artist = None, name = None, uri = None, img = None, link=None):
        self.artist = artist
        self.uri = uri
        self.name = name
        self.img = img
        self.link = link
    def __str__(self) -> str:
        return f"Artist: {self.artist}\nName: {self.name}\nURI: {self.uri}\n"

def getAlbum(artistAlbum: tuple=None):
    """Gets album information based on the name of the album retrieved from the web

    Args:
        artistAlbum (tuple): tuple of (artist, album). Defaults to None.

    Returns:
        Album object
    """
    results = sp.search(q = f"album:{artistAlbum[1]}artist:{artistAlbum[0]}", type = "album")

    album = Album()

    #Populate the album object with the relevant data
    album.uri = results['albums']['items'][0]['uri'].split(":")[2]
    album.name = results['albums']['items'][0]['name']
    album.img = results['albums']['items'][0]['images'][0]['url']
    album.artist = results['albums']['items'][0]['artists'][0]['name']
    album.link = results['albums']['items'][0]['external_urls']['spotify']

    return album

def addAlbumToPlaylist(albumURI: str=None, playlist: str=None):
    """Add an album to a playlist given their respective ids

    Args:
        albumURI : URI of the album. Defaults to None.
        playlist : ID of the playlist. Defaults to None.
    """
    albumTracks = sp.album_tracks(albumURI)
    for y in albumTracks['items']:
        sp.playlist_add_items(playlist, [y['id']])

def retrieveAlbumsFromPlaylist(playlist: str=None):
    albumOffset = 0
    albumList = []
    results = sp.playlist_tracks(playlist, limit=5, offset=albumOffset, fields="items(track(album(id)))")
        
def moveAlbum(albumURI: str=None, sourcePlaylist: str=None, targetPlaylist: str=None):
    pass

def deleteAlbum(albumURI: str=None, playlist: str=None):
    pass

def getPlaylist(playlist_id: str=None):
    """Retrieves the name and the link to a playlist given its ID

    Args:
        playlist_id (str, optional): URI ID of the playlist. Defaults to None.

    Returns:
        name: name of the playlist
        link: link to the playlist
    """
    results = sp.playlist(playlist_id)

    return results['name'], results['external_urls']['spotify']
