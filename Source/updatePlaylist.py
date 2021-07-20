import sys
import spotipy
from spotipy.oauth2 import SpotifyOAuth

def main():
    spotifyInterface = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="playlist-modify-public,user-library-read"))
    results = spotifyInterface.current_user_saved_tracks()
    for idx, item in enumerate(results['items']):
        track = item['track']
        print(idx, track['artists'][0]['name'], " – ", track['name'])
    

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Done, interrupted')    
        sys.exit(0)