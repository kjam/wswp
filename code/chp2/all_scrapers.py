import re
from bs4 import BeautifulSoup
from lxml.html import fromstring

FIELDS = ('area', 'population', 'iso', 'country', 'capital',
          'continent', 'tld', 'currency_code', 'currency_name',
          'phone', 'postal_code_format', 'postal_code_regex',
          'languages', 'neighbours')


def re_scraper(html):
    """ Using regex to extract data from country pages. """
    results = {}
    for field in FIELDS:
        results[field] = re.search(
            '<tr id="places_%s__row">.*?<td class="w2p_fw">(.*?)</td>'
            % field, html).groups()[0]
    return results


def bs_scraper(html):
    """ Using beautifulsoup to extract data from country pages. """
    soup = BeautifulSoup(html, 'html.parser')
    results = {}
    for field in FIELDS:
        results[field] = soup.find('table').find(
            'tr', id='places_%s__row' % field).find(
                'td', class_='w2p_fw').text
    return results


def lxml_scraper(html):
    """ Using lxml and cssselect to extract data from country pages. """
    tree = fromstring(html)
    results = {}
    for field in FIELDS:
        results[field] = tree.cssselect(
            'table > tr#places_%s__row > td.w2p_fw' % field)[0].text_content()
    return results


def lxml_xpath_scraper(html):
    """ Using lxml and xpath to extract data from country pages. """
    tree = fromstring(html)
    results = {}
    for field in FIELDS:
        results[field] = tree.xpath(
            '//tr[@id="places_%s__row"]/td[@class="w2p_fw"]' % field)[0].text_content()
    return results
