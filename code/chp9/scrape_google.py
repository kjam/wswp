import requests
from urllib.parse import parse_qs, urlparse
from lxml.html import fromstring

# get results from search
html = requests.get('https://www.google.com/search?q=test')
tree = fromstring(html.content)
results = tree.cssselect('h3.r a')
print(results)

# grab the first link
link = results[0].get('href')
print(link)

# parse the destination url from the querystring
qs = urlparse(link).query
parsed_qs = parse_qs(qs)
print(parsed_qs)
print(parsed_qs.get('q', []))


# as one list
links = []
for result in results:
    link = result.get('href')
    qs = urlparse(link).query
    links.extend(parse_qs(qs).get('q', []))

print(links)
