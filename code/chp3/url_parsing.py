import re
from urllib.parse import urlsplit

# how to manage converting urls into filenames

url = 'http://example.webscraping.com/default/view/Australia-1'
filename = re.sub('[^/0-9a-zA-Z\-.,;_ ]', '_', url)
filename = '/'.join(segment[:255] for segment in filename.split('/'))
print(filename)

# how to handle edge case where we need to append index.html for parent urls
# such as http://example.webscraping.com/index/

components = urlsplit('http://example.webscraping.com/index/')
print(components)
print(components.path)
path = components.path
if not path:
    path = '/index.html'
elif path.endswith('/'):
    path += 'index.html'
filename = components.netloc + path + components.query
filename = re.sub('[^/0-9a-zA-Z\-.,;_ ]', '_', filename)
filename = '/'.join(segment[:255] for segment in filename.split('/'))
print(filename)
