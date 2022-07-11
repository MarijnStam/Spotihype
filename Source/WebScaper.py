import sys
from bs4 import BeautifulSoup
import urllib.request


def getAlbums():

    """Gets a list of highest rated albums from a website

    Returns
    -------
    `tuple`
        List of tuples: : [(artist, album), (artist, album), etc]
    """    
    #Make a list of tuples for the albums. [(artist, album), (artist, album), etc]
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

    #Results are given as "Artist - Album". Split the string at "-" and make a tuple (artist, album)
    #Append the tuple to the list
    for name in soup.find_all("meta", itemprop="name"):
        albumList.append(tuple(name.get("content", None).split("-")))

    return albumList
