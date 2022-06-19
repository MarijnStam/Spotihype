import sys
from bs4 import BeautifulSoup
import urllib.request


def getAlbums():
    """Retrieves a list of album names from a rating site

    Returns:
        List: :ist of album name strings
    """

    albumList = []
    
    try:
        req = urllib.request.Request(url='https://www.albumoftheyear.org/ratings/6-highest-rated/2022/1', headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(req).read()
    except urllib.error.HTTPError as e:
        print("Caught HTTP Error: ", e.__dict__)
        return albumList
    except urllib.error.URLError as e:
        print("Caught URL Error: ", e.__dict__)
        return albumList
    except ConnectionResetError as e:
        print("Caught URL Error: ", e.__dict__)
        return 

    soup = BeautifulSoup(html, features="html.parser")
    #Retrieve the names of all Artist - Album entries on the webpage
    #Append them into a list

    for name in soup.find_all("meta", itemprop="name"):
        albumList.append(name.get("content", None))

    return albumList
