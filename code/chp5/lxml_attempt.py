from lxml.html import fromstring
from chp3.downloader import Downloader

D = Downloader()
html = D('http://example.webscraping.com/search')
tree = fromstring(html)
tree.cssselect('div#results a')
