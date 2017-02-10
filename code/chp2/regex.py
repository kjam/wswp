import re
from chp1.advanced_link_crawler import download

url = 'http://example.webscraping.com/view/UnitedKingdom-239'
html = download(url)

print(re.findall(r'<td class="w2p_fw">(.*?)</td>', html))

print(re.findall('<td class="w2p_fw">(.*?)</td>', html)[1])

print(re.findall('<tr id="places_area__row"><td class="w2p_fl"><label for="places_area" id="places_area__label">Area: </label></td><td class="w2p_fw">(.*?)</td>', html))

print(re.findall('''<tr id="places_area__row">.*?<td\s*class=["']w2p_fw["']>(.*?)</td>''', html))
