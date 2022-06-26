from Source import WebScaper as wb

def test_get_albums():
    albums = wb.getAlbums()
    assert len(albums) > 5
    assert isinstance(albums, list)
    assert isinstance(albums[0], tuple)
    assert isinstance(albums[0][0], str)
    assert isinstance(albums[0][1], str)
