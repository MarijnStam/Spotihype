import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class SQLite:
    """
    This class is a context manager for the database.
    Use this for handling db operations within this file
    """
    def __init__(self):
        self.dbName = os.path.join(BASE_DIR, "AlbumsDB.db")
    def __enter__(self):
        self.conn = sqlite3.connect(self.dbName)
        return self.conn.cursor()
    def __exit__(self, type, value, traceback):
        self.conn.commit()
        self.conn.close()

def addAlbum(artist: str=None, name: str=None, uri: str=None):
    """Adds an album entry to the db

    Args:
        artist (str): Defaults to None.
        name (str): Defaults to None.
        uri (str): Defaults to None.
    """
    with SQLite() as cur:
        try:
            cur.execute(f"INSERT INTO Albums (Artist, Name, URI) VALUES ('{artist}', '{name}', '{uri}')")
        except sqlite3.Error as e:
            raise sqlite3.Error(e)