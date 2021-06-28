import time
import csv
import requests
import re
from tqdm import tqdm
from selenium import webdriver
from bs4 import BeautifulSoup



url = 'https://www.mordorintelligence.com/industry-reports/category/information-communications-technology'
driver = webdriver.Firefox()

driver.get(url)

time.sleep(5)
a = []
for i in range(130):
    ## BS4 code to be added ---------------a.append()
    pagination_section = driver.find_element_by_css_selector('.MuiTablePagination-root')
    next_icon = pagination_section.find_elements_by_class_name('MuiSvgIcon-root')[-1].click()
    time.sleep(3)
    print("On Page ", i+1)
