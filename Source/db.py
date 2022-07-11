import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class SQLite:
    """
    A class used to connect to the database.


    Attributes
    ----------
        dbName : `str`
            Path to the db in the filesystem
    Methods
    -------
        `addAlbum(artist: str, name: str, uri: str)`
            Adds an album to the db
    """

    def __init__(self):
        self.dbName = os.path.join(BASE_DIR, "AlbumsDB.db")
    def __enter__(self):
        self.conn = sqlite3.connect(self.dbName)
        return self.conn.cursor()
    def __exit__(self, type, value, traceback):
        self.conn.commit()
        self.conn.close()

def addAlbum(artist: str, name: str, uri: str):
    """Adds an album to the database

    Parameters
    ----------
    artist : `str`
        Name of the artist
    name : `str`
        Name of the album
    uri : `str`
        URI of the album

    Raises
    ------
    `sqlite3.Error`
        Error raised when an album URI is already present in the database
    """
    with SQLite() as cur:
        try:
            cur.execute(f"INSERT INTO Albums (Artist, Name, URI) VALUES ('{artist}', '{name}', '{uri}')")
        except sqlite3.Error as e:
            raise sqlite3.Error(e)