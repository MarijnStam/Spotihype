import sys
from bs4 import BeautifulSoup
import urllib.request

LINK_URI_INDEX = 30

def getAlbums():
        
    req = urllib.request.Request(url='https://www.albumoftheyear.org/ratings/6-highest-rated/2022/1', headers={'User-Agent': 'Mozilla/5.0'})
    html = urllib.request.urlopen(req).read()
    soup = BeautifulSoup(html, features="html.parser")

    #Retrieve the names of all Artist - Album entries on the webpage
    #Append them into a list
    albumList = []
    for name in soup.find_all("meta", itemprop="name"):
        albumList.append(name.get("content", None))

    return albumList
