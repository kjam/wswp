from urllib.parse import urlencode
from urllib.request import Request, urlopen

LOGIN_URL = 'http://example.webscraping.com/user/login'
LOGIN_EMAIL = 'example@webscraping.com'
LOGIN_PASSWORD = 'example'
data = {'email': LOGIN_EMAIL, 'password': LOGIN_PASSWORD}
encoded_data = urlencode(data)
request = Request(LOGIN_URL, encoded_data.encode('utf-8'))
response = urlopen(request)
print(response.geturl())
