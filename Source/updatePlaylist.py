import sys
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from retrieveAlbums import Albums

def main():

    spotifyInterface = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="playlist-modify-public,user-library-read"))
 
    albumGetter = Albums()
    albumList = albumGetter.getAlbum()

    print(albumList)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Done, interrupted')    
        sys.exit(0)