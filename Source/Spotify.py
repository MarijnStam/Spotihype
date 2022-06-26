import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import find_dotenv, load_dotenv

#Load our Spotipy enviroment variables 
load_dotenv(find_dotenv())
AOTY_PLAYLIST_ID = '5hwjLoGifPEGBrBmNZxa0X'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="playlist-modify-public,user-library-read"))

class NotFoundError(Exception):
    pass

class Album:
    """Class for holding an album object. Can be initialized with either artist/album name or album URI
    
    Args:
        artistAlbum (tuple): tuple of (artist, album). Defaults to None.
    Args:
        uri (string): tuple of (artist, album). Defaults to None.

    Returns:
        Album object
    """
    def __init__(self, artistAlbum: tuple=None, uri: str=None, json: str=None):
        if artistAlbum is not None:
        #Use name/album to find album data
            results = sp.search(q = f"album:{artistAlbum[1]}artist:{artistAlbum[0]}", type = "album")
            try:
                self.artist = results['albums']['items'][0]['artists'][0]['name']
                self.uri = results['albums']['items'][0]['uri'].split(":")[2]
                self.name = results['albums']['items'][0]['name']
                self.img = results['albums']['items'][0]['images'][0]['url']
                self.link = results['albums']['items'][0]['external_urls']['spotify']
            except IndexError as e:
                print(results)
                raise NotFoundError(f"Album :{artistAlbum[1]}{artistAlbum[0]} was not found")

        #Use URI to find album data
        elif uri is not None:
            results = sp.album(uri)
            try:
                self.artist = results['artists'][0]['name']
                self.uri = results['uri'].split(":")[2]
                self.name = results['name']
                self.img = results['images'][0]['url']
                self.link = results['external_urls']['spotify']
            except IndexError as e:
                print(results)
                raise NotFoundError(f"Album :{artistAlbum[1]}{artistAlbum[0]} was not found")

    def __str__(self) -> str:
        return f"Artist: {self.artist}\nName: {self.name}\nURI: {self.uri}\n"
  
def addAlbumToPlaylist(albumURI: str=None, playlist: str=None):
    """Add an album to a playlist given their respective ids

    Args:
        albumURI : URI of the album. Defaults to None.
        playlist : ID of the playlist. Defaults to None.
    """
    albumTracks = sp.album_tracks(albumURI)
    for y in albumTracks['items']:
        sp.playlist_add_items(playlist, [y['id']])

def getPlaylistTracks(playlist: str=None):
    """Retrieves the tracks of a playlist given its ID

    Args:
        playlist (str, optional): URI of the playlist. Defaults to None.

    Returns:
        list: list of Album objects
    """
    albumList = []
    uriList = []
    results = sp.playlist_tracks(playlist, fields="items(track(album(id))), next", limit=100)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    for track in tracks:
        albumUri = track['track']['album']['id']
        #add albumURI to albumList if it is not already in the list (to avoid duplicates)
        if albumUri not in uriList:
            albumList.append(Album(uri=albumUri))
            uriList.append(albumUri)
    return albumList
        
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
