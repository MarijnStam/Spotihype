import unittest
import sys
from dotenv import load_dotenv, find_dotenv
sys.path.append('Source')
import Spotify as sp

load_dotenv(find_dotenv())

class SpotifyTest(unittest.TestCase):

    def testAlbumInit(self):
        with self.subTest("Test album init with Artists - Name"):
            name = [("Black Country - New Road", "Ants From Up There"), ()]
            album = sp.Album(name)
            self.assertIsNotNone(album.link)
            self.assertIsNotNone(album.uri)
            self.assertIsNotNone(album.img)
            self.assertIsNotNone(album.name)
            self.assertIsNotNone(album.artist)
        with self.subTest("Test album init with URI"):
            uri = '41ycYGcnhkDb3pFkL8vSPJ'
            album = sp.Album(uri=uri)
            self.assertIsNotNone(album.link)
            self.assertIsNotNone(album.uri)
            self.assertIsNotNone(album.img)
            self.assertIsNotNone(album.name)
            self.assertIsNotNone(album.artist)

if __name__ == '__main__':
    unittest.main()