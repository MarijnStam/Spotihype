import pytest
import os

from Source import Spotify as sp

path = os.path.dirname(os.path.abspath(__file__))
skip = (path == "/home/runner/work/Spotihype/Spotihype/test")

name = [("Black Country - New Road", "Ants From Up There"), ()]
uriName = '41ycYGcnhkDb3pFkL8vSPJ'

@pytest.mark.skipif(skip, reason="Spotipy tests are not supported on CI")
@pytest.mark.parametrize("name, uriName", [
    (name, uriName),
    (name, None),
    (None, uriName),
    ])
def test_album_init(name, uriName): 
    album = sp.Album(artistAlbum=name, uri=uriName) 
    assert (album.link) != None     
    assert (album.artist) != None
    assert (album.name) != None
    assert (album.uri) != None

@pytest.mark.skipif(skip, reason="Spotipy tests are not supported on CI")
def test_get_playlist():
    name, link = sp.getPlaylist(sp.AOTY_PLAYLIST_ID)
    assert name != None
    assert link != None
