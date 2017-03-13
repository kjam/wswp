import json
import os
import glob
import requests

from lxml.html import fromstring


def find_ff_sessions():
    paths = [
        '~/.mozilla/firefox/*.default',
        '~/Library/Application Support/Firefox/Profiles/*.default',
        '%APPDATA%/Roaming/Mozilla/Firefox/Profiles/*.default'
    ]
    for path in paths:
        filename = os.path.join(path, 'sessionstore.js')
        matches = glob.glob(os.path.expanduser(filename))
        if matches:
            return matches[0]


def load_ff_sessions(session_filename):
    cookies = {}
    if os.path.exists(session_filename):
        json_data = json.loads(open(session_filename, 'rb').read())
        for window in json_data.get('windows', []):
            for cookie in window.get('cookies', []):
                cookies[cookie.get('name')] = cookie.get('value')
    else:
        print('Session filename does not exist:', session_filename)
    return cookies


def session_login():
    session_filename = find_ff_sessions()
    assert session_filename is not None
    cookies = load_ff_sessions(session_filename)
    print('found cookies: ', cookies)
    url = 'http://example.webscraping.com'
    html = requests.get(url, cookies=cookies)
    tree = fromstring(html.content)
    print(tree.cssselect('ul#navbar li a')[0].text_content())
    return html


if __name__ == '__main__':
    session_login()
