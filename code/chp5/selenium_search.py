from selenium import webdriver

driver = webdriver.Firefox()
driver.get('http://example.webscraping.com/search')
driver.find_element_by_id('search_term').send_keys('.')
js = "document.getElementById('page_size').options[1].text = '1000';"
driver.execute_script(js)
driver.find_element_by_id('search').click()
driver.implicitly_wait(30)
links = driver.find_elements_by_css_selector('#results a')
countries = [link.text for link in links]
print(countries)

driver.close()
