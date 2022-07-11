import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import find_dotenv, load_dotenv

#Load our Spotipy enviroment variables 
load_dotenv(find_dotenv())
AOTY_PLAYLIST_ID = '5hwjLoGifPEGBrBmNZxa0X'
LIKED_PLAYLIST_ID = '2b6diSqGc06kqlJOUfADn0'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="playlist-modify-public,user-library-read"))

class NotFoundError(Exception):
    pass

class Album:
    """Class for creating an album.
    Supply either artistAlbum or uri to find the album.

    Parameters
    ----------
    artistAlbum : `tuple`, optional
        A tuple containing (artist, album), by default None
    uri : `str`, optional
        The URI of the Spotify Album, by default None
    json : `str`, optional
        Raw JSON of the album, NOT SUPPORTED YET, by default None

    Raises
    ------
    `NotFoundError`
        Raised when album is not found by searching with artistAlbum
    `NotFoundError`
        Raised when album is not found by searching with URI
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
  
def addAlbumToPlaylist(albumURI: str, playlist: str):
    """Adds an album to a playlist given its URI and the playlist's URI

    Parameters
    ----------
    albumURI : `str`
        URI of the album
    playlist : `str`
        URI of the playlist
    """    
    albumTracks = sp.album_tracks(albumURI)
    for y in albumTracks['items']:
        sp.playlist_add_items(playlist, [y['id']])

def getPlaylistAlbums(playlist: str):
    """Gets a list of albums from a playlist

    Parameters
    ----------
    playlist : `str`
        URI of the playlist, by default None

    Returns
    -------
    `list` of `Album` objects
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
        
def moveAlbum(albumURI: str, sourcePlaylist: str, targetPlaylist: str):
    """Moves an album from one playlist to another.

    Parameters
    ----------
    albumURI : `str`
        URI of the album to move.
    sourcePlaylist : `str`
        URI of the playlist to remove the album from.
    targetPlaylist : `str`
        URI of the playlist to move the album to.
    """    
    albumTracks = sp.album_tracks(albumURI)
    for y in albumTracks['items']:
        sp.playlist_remove_all_occurrences_of_items(sourcePlaylist, [y['id']])
        sp.playlist_add_items(targetPlaylist, [y['id']])

def deleteAlbum(albumURI: str, playlist: str):
    """Deletes an album from a playlist given its URI and the playlist's URI.

    Parameters
    ----------
    albumURI : `str`
        URI of the album to delete.
    playlist : `str`
        URI of the playlist to delete the album from.
    """
    albumTracks = sp.album_tracks(albumURI)
    for y in albumTracks['items']:
        sp.playlist_remove_all_occurrences_of_items(playlist, [y['id']])

def getPlaylist(playlist_id: str):
    """Gets a playlist name and link, given its URI.

    Parameters
    ----------
    playlist_id : `str`
        URI of the playlist to get

    Returns
    -------
    `str`
        Playlist name
    `str`
        Playlist link
    """
    results = sp.playlist(playlist_id)
    return results['name'], results['external_urls']['spotify']
