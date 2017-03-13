import requests
import json
from lxml.html import fromstring
from chp6.login import login, parse_form

COUNTRY_URL = 'http://example.webscraping.com/edit/United-Kingdom-239'
VIEW_URL = 'http://example.webscraping.com/view/United-Kingdom-239'


def get_population():
    html = requests.get(VIEW_URL)
    tree = fromstring(html.content)
    population = tree.cssselect(
        '#places_population__row .w2p_fw')[0].text_content()
    return int(population.replace(',', ''))


def add_population():
    session = requests.Session()
    response, session = login(session=session)
    country_html = session.get(COUNTRY_URL)
    data = parse_form(country_html.content)
    print('population is: ', data['population'])
    data['population'] = int(data['population']) + 1
    response = session.post(COUNTRY_URL, data=data)
    test_population = get_population()
    print('population is now:', test_population)
    assert test_population == data['population']


def get_currency():
    html = requests.get(VIEW_URL)
    tree = fromstring(html.content)
    currency = tree.cssselect(
        '#places_currency_name__row .w2p_fw')[0].text_content()
    return currency


def change_currency():
    session = requests.Session()
    response, session = login(session=session)
    country_html = session.get(COUNTRY_URL)
    data = parse_form(country_html.content)
    print('currency is: ', data['currency_name'])
    data['currency_name'] = 'British pounds'
    response = session.post(COUNTRY_URL, data=data)
    test_currency = get_currency()
    print('currency is now: ', test_currency)
    assert test_currency == data['currency_name']


if __name__ == '__main__':
    add_population()
