import unittest

from Source import WebScaper as wb

class ScrapeAlbums(unittest.TestCase):   
    def testGetAlbums(self):
        albums = wb.getAlbums()
        self.assertIsNotNone(albums)
        self.assertGreater(len(albums), 0)
        self.assertIsInstance(albums, list)
        self.assertIsInstance(albums[0], tuple)
        self.assertIsInstance(albums[0][0], str)
        self.assertIsInstance(albums[0][1], str)

if __name__ == '__main__':
    unittest.main()