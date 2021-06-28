import time
import csv
import requests
import re
from tqdm import tqdm
from selenium import webdriver
from bs4 import BeautifulSoup
from collections import defaultdict
#from selenium.webdriver.chrome.options import Options


#CHROMEDRIVER_PATH = '/home/anujrana/Documents/SkyQuest/Scraper/chromedriver'



option = webdriver.FirefoxOptions()
option.headless = True
driver = webdriver.Firefox(options = option)
#chrome_options = Options()
#chrome_options.add_argument("--headless")

#driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH,
#                          options=chrome_options
#                          )

driver.get("https://www.theinsightpartners.com/categories/healthcare-it")

driver.find_element_by_id("PublishedStatus").click()

time.sleep(10)

soup = BeautifulSoup(driver.page_source, 'lxml')

total_pages = len(soup.find('div', class_='pagination').find_all('a'))

links = []
links.extend([link['href']
                for link in soup.find_all('a', class_='g-text-reset')])

button = driver.find_element_by_xpath('//*[@id="postList"]/div[12]/a[1]')
driver.execute_script("arguments[0].click();", button)
time.sleep(10)
soup = BeautifulSoup(driver.page_source, 'lxml')

links.extend([link['href']
                for link in soup.find_all('a', class_='g-text-reset')])

for i in range(2, total_pages):

    button = driver.find_element_by_xpath('//*[@id="postList"]/div[12]/a['+str(i+1)+']')
    driver.execute_script("arguments[0].click();", button)
    time.sleep(10)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    # else:
    links.extend([link['href']
                for link in soup.find_all('a', class_='g-text-reset')])
    )
csv_file = open('healthcare-it.csv', 'w')
csv_writer = csv.writer(csv_file)

DATA = []
SEGMENTS = []
SUB_SEGMENTS = []
LEVELS = []

max_seg_size = 0
for link in tqdm(links[43:45]):
    if(link )
    try:
        report = requests.get(link).text
        soup = BeautifulSoup(report, 'lxml')

        title = soup.find('h1').text

        main_div = soup.find('div', class_='card-body')

        description = main_div.p.text

        revenue, forecast = re.findall(
            'US\$ ?[0-9]+,*[0-9]+?.?[0-9]+ [a-zA-Z]+', description)

        per_match = re.search('[0-9]+.?[0-9]+ ?%', description).group(0)

        segments = []
        sub_segments_dict = defaultdict(list)
        levels_dict = defaultdict(list)
        companies = []
        for ps in main_div.find_all('p'):

            if re.search(' . by [A-Z][a-z]+ ?([A-Z][a-z]+)?', ps.text):
                seg = re.search(
                    ' . by [A-Z][a-z]+ ?([A-Z][a-z]+)?', ps.text).group(0)
                seg = re.sub(' . by ', '', seg)
                segments.append(seg)
                ul = ps.findNext('ul')
                for l in ul.find_all('li', recursive=False):
                    sub_segments_dict[seg].append(l.span.text)
                    if l.find('li'):
                        for ll in l.find_all('li'):
                            levels_dict[seg].append(ll.text)
                    else:
                        if not len(levels_dict[seg]):
                            levels_dict[seg].append(None)
            
            elif re.search('By [A-Z][a-z]+ ?([A-Z][a-z]+)?', ps.text):
                seg = re.search(
                    'By [A-Z][a-z]+ ?([A-Z][a-z]+)?', ps.text).group(0)
                seg = re.sub('By ', '', seg)
                segments.append(seg)
                ul = ps.findNext('ul')
                for l in ul.find_all('li', recursive=False):
                    sub_segments_dict[seg].append(l.span.text)
                    if l.find('li'):
                        for ll in l.find_all('li'):
                            levels_dict[seg].append(ll.text)
                    else:
                        if not len(levels_dict[seg]):
                            levels_dict[seg].append(None)
            
            elif re.search(' . By [A-Z][a-z]+ ?([A-Z][a-z]+)?', ps.text):
                seg = re.search(
                    ' . By [A-Z][a-z]+ ?([A-Z][a-z]+)?', ps.text).group(0)
                seg = re.sub(' . By ', '', seg)
                segments.append(seg)
                ul = ps.findNext('ul')
                for l in ul.find_all('li', recursive=False):
                    sub_segments_dict[seg].append(l.span.text)
                    if l.find('li'):
                        for ll in l.find_all('li'):
                            levels_dict[seg].append(ll.text)
                    else:
                        if not len(levels_dict[seg]):
                            levels_dict[seg].append(None)

            if re.search('Company Profiles', ps.text):
                ul = ps.findNext('ul')
                for l in ul.find_all('li'):
                    companies.append(l.text)

        companies = ', '.join(companies)

        sub_segments = []
        regions = None
        for key, value in sub_segments_dict.items():
            value = ', '.join(value)
            sub_segments.append(value)
            if key == 'Geography':
                regions = value

        levels = []
        for key, value in levels_dict.items():
            if None in value:
                levels.append(None)
            else:
                levels.append(', '.join(value))

        if max_seg_size < len(segments):
            max_seg_size = len(segments)

        DATA.append([title, link, revenue, forecast,
                     per_match, companies, regions])
        SEGMENTS.append([s for s in segments])
        SUB_SEGMENTS.append([s for s in sub_segments])
        LEVELS.append([l for l in levels])
    except Exception as error:
        print(error)
        print(link)

csv_writer.writerow(['Title', 'Link', 'Market size', 'Forecasted Market Size/ Revenue',
                     'CAGR (%) ', 'Companies ', 'Geographies/ Regions covered'] +
                    ['Segment ' + str(i+1) for i in range(max_seg_size)] +
                    ['Sub-segment ' + str(i+1) for i in range(max_seg_size)] +
                    ['Level ' + str(i+1) for i in range(max_seg_size)])

for i, d in enumerate(DATA):
    csv_writer.writerow(d + [s for s in SEGMENTS[i]] +
                        [None for _ in range(max_seg_size - len(SEGMENTS[i]))] +
                        [s for s in SUB_SEGMENTS[i]] +
                        [None for _ in range(max_seg_size - len(SUB_SEGMENTS[i]))] +
                        [l for l in LEVELS[i]] +
                        [None for _ in range(max_seg_size - len(LEVELS[i]))])

csv_file.close()
