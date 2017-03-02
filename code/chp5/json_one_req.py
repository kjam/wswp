from csv import DictWriter
import requests


PAGE_SIZE = 1000

template_url = 'http://example.webscraping.com/ajax/' + \
    'search.json?page=0&page_size={}&search_term=.'

resp = requests.get(template_url.format(PAGE_SIZE))
data = resp.json()
records = data.get('records')

with open('../data/countries.csv', 'w') as countries_file:
    wrtr = DictWriter(countries_file, fieldnames=records[0].keys())
    wrtr.writeheader()
    wrtr.writerows(records)
