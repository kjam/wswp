import requests
import base64
from configparser import ConfigParser
from time import sleep
from lxml.html import fromstring
from chp6.login import parse_form
from chp7.image_processing import get_captcha_img, get_b64_string

API_URL = 'https://www.9kw.eu/index.cgi'
REGISTER_URL = 'http://example.webscraping.com/user/register'


def get_api_key():
    config = ConfigParser()
    config.read('../config/api.cfg')
    return config.get('captcha_api', 'key')


def send_captcha(api_key, img_data):
    data = {
        'action': 'usercaptchaupload',
        'apikey': api_key,
        'file-upload-01': img_data,
        'base64': '1',
        'selfsolve': '1',
        'json': '1',
        'maxtimeout': '300'
    }
    resp = requests.post(API_URL, data)
    return resp.json()


def get_captcha_text(api_key, captcha_id):
    data = {
        'action': 'usercaptchacorrectdata',
        'id': captcha_id,
        'apikey': api_key,
        'json': '1',
    }
    resp = requests.get(API_URL, data)
    print('captcha text response:', resp.json())
    answer = resp.json().get('answer')
    return answer


def register(first_name, last_name, email, password):
    session = requests.Session()
    html = session.get(REGISTER_URL)
    form = parse_form(html.content)
    form['first_name'] = first_name
    form['last_name'] = last_name
    form['email'] = email
    form['password'] = form['password_two'] = password
    img_data = get_b64_string(html.content)
    img = get_captcha_img(html.content)
    img.show()  # This will show the image locally when run
    api_key = get_api_key()
    captcha_id = send_captcha(api_key, img_data)
    print('submitted captcha, got id:', captcha_id)
    sleep(300)
    captcha = get_captcha_text(api_key, captcha_id)
    print('captcha solve:', captcha)
    form['recaptcha_response_field'] = captcha
    resp = session.post(html.url, form)
    success = '/user/register' not in resp.url
    if not success:
        form_errors = fromstring(resp.content).cssselect('div.error')
        print('Form Errors:')
        print('\n'.join(
            ('  {}: {}'.format(f.get('id'), f.text) for f in form_errors)))
    return success
