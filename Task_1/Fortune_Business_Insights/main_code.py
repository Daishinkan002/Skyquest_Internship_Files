import selenium.webdriver as webdriver
import pandas as pd
from bs4 import BeautifulSoup
import re

options = webdriver.FirefoxOptions()
options.headless = True
driver = webdriver.Firefox(options= options)

links = ['https://www.fortunebusinessinsights.com/central-nervous-system-treatment-market-103973']



url = links[0]
#for url in links:
driver.get(url)
table = driver.find_element_by_tag_name('table')
#--------------------------------------------------------
segments = []
subsegments = []
levels = []
useful_trs = []
got_unit = False
got_segmentation = False
got_headings = False
levels_block = []
subseg_store = []
for tr in table.find_elements_by_xpath('.//tr'):
    p = tr.find_elements_by_tag_name('p')
    if(got_unit):
        useful_trs.append(tr)
        heading = p[0].text

        if(heading == 'Segmentation'):
            print("1")
            got_segmentation = True
            segments.append(p[1].text)
            soup = BeautifulSoup(tr.get_attribute('innerHTML'), 'html.parser')
            td1 = ''
            td1 = soup.find_all('td')[1]
            main_ul = td1.find('ul')
            if(not main_ul):
                got_segmentation = False
                got_headings = True
        elif((heading != 'Segmentation') and (got_segmentation)):
            x = re.sub(' ', '', heading)
            if x != '':
                segments.append(heading)
            elif((len(p) > 1) and ('geography' in p[1].text.lower())):
                segments.append(p[1].text)
                
        elif(not got_segmentation):
            if(not got_headings):
                segments.append(heading)
        else:
            pass
    if(p[0].text == 'Unit'):
        #print(tr.text)
        got_unit = True



def printt(array):
    for seg in array:
        print(seg)
        print()

print("\n\n--------------------Segments------------------\n")
printt(segments)
print("\n\n -------------------Seva Samapt Hui -----------------\n\n")

driver.close()