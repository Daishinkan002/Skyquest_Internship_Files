import selenium.webdriver as webdriver
import time
import pandas as pd
from bs4 import BeautifulSoup
import re
import requests


driver = webdriver.Firefox()
url = 'https://www.technavio.com/industries/communication-services'


driver.get(url)

time.sleep(3)
length_of_all_pages = 19
links = []
for i in range(2):

    # ... bs4 code
    html = driver.page_source
    soup = BeautifulSoup(html)

    main_block = soup.find_all(class_="upcomingprolist")[0]
    product_block = main_block.find("div", {"id": "product-tn-block"})
    sm12 = product_block.find_all(class_="col-sm-12 listviews")
    for sm in sm12:
        sm_10 = sm.find(class_="col-sm-10")
        a_tag = sm_10.find('a')
        print(a_tag.get_attribute_list('href')[0])
        links.append(a_tag.get_attribute_list('href')[0])
        print("\n-----------\n--------------\n")

    pagination_tab = driver.find_element_by_class_name('pagination')
    clickable_li = pagination_tab.find_elements_by_tag_name('li')[-2]
    a_tag = clickable_li.find_element_by_tag_name('a').click()
    time.sleep(3)
    print("Scrolled ", i+1, " page")



driver.close()