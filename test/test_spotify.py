import pytest

from Source import Spotify as sp

name = [("Black Country - New Road", "Ants From Up There"), ()]
uriName = '41ycYGcnhkDb3pFkL8vSPJ'

@pytest.mark.skip(reason="Cannot test OAuth2 workflow on GitHub Actions")
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

@pytest.mark.skip(reason="Cannot test OAuth2 workflow on GitHub Actions")
def test_get_playlist():
    name, link = sp.getPlaylist(sp.AOTY_PLAYLIST_ID)
    assert name != None
    assert link != None
