import sys
import json
from typing import List
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from WebScaper import getAlbum

PLAYLIST_ID = '5hwjLoGifPEGBrBmNZxa0X'

def main():

    spotifyInterface = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="playlist-modify-public,user-library-read"))
 

    albumList = getAlbum()
    
    for x in albumList:
        spotifyAlbumList = spotifyInterface.album(x)

    for x in albumList:
        album = spotifyInterface.album_tracks(x)
        for y in album['items']:
            spotifyInterface.playlist_add_items(PLAYLIST_ID, [y['id']])
        



if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Done, interrupted')    
        sys.exit(0)