from bs4 import BeautifulSoup
from chp1.advanced_link_crawler import download

broken_html = '<ul class=country><li>Area<li>Population</ul>'

soup = BeautifulSoup(broken_html, 'html.parser')
fixed_html = soup.prettify()
print(fixed_html)

# still broken, so try a different parser

soup = BeautifulSoup(broken_html, 'html5lib')
fixed_html = soup.prettify()
print(fixed_html)

# now we can try and extract the data from the html

ul = soup.find('ul', attrs={'class': 'country'})
print(ul.find('li'))  # returns just the first match
print(ul.find_all('li'))  # returns all matches
