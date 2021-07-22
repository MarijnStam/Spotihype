import sys
from bs4 import BeautifulSoup
import urllib.request


class Albums:

    def getAlbum(self):
        
        req = urllib.request.Request(url='https://www.albumoftheyear.org/ratings/6-highest-rated/2021/1', headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(req).read()
    
        soup = BeautifulSoup(html, features="html.parser")

        table = soup.findAll('a',attrs={"data-track-action":"Spotify"})
        albumList = []
        for idx, x in enumerate(table):
            albumList.append(x.get('href'))
        return albumList