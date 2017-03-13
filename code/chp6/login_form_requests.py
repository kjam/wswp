import requests

LOGIN_URL = 'http://example.webscraping.com/user/login'
LOGIN_EMAIL = 'example@webscraping.com'
LOGIN_PASSWORD = 'example'
data = {'email': LOGIN_EMAIL, 'password': LOGIN_PASSWORD}

response = requests.post(LOGIN_URL, data)
print(response.url)
