import mechanize

LOGIN_URL = 'http://example.webscraping.com/user/login'
LOGIN_EMAIL = 'example@webscraping.com'
LOGIN_PASSWORD = 'example'
COUNTRY_URL = 'http://example.webscraping.com/edit/United-Kingdom-239'


br = mechanize.Browser()
br.open(LOGIN_URL)
br.select_form(nr=0)
br['email'] = LOGIN_EMAIL
br['password'] = LOGIN_PASSWORD
response = br.submit()
br.open(COUNTRY_URL)
br.select_form(nr=0)
br['population'] = str(int(br['population']) + 1)
br.submit()
