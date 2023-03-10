import re
from urllib.request import urlopen
from bs4 import BeautifulSoup
import random

pages = set()


def getLinks(articleUrl):
    global pages
    html = urlopen("http://en.wikipedia.org/{}".format(articleUrl))
    bs = BeautifulSoup(html, 'html.parser')
    for link in bs.findAll('a', href=re.compile("^(/wiki/)")):
        if 'href' in link.attrs:
            if link.attrs['href'] not in pages:
                newPage = link.attrs['href']
                print(newPage, pages)
                pages.add(newPage)
                getLinks(newPage)


getLinks('')

