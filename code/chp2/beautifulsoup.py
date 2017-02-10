from bs4 import BeautifulSoup
from chp1.advanced_link_crawler import download

url = 'http://example.webscraping.com/view/UnitedKingdom-239'
html = download(url)
soup = BeautifulSoup(html, 'html5lib')

# locate the area row
tr = soup.find(attrs={'id': 'places_area__row'})
td = tr.find(attrs={'class': 'w2p_fw'})  # locate the data
area = td.text  # extract the data
print(area)
