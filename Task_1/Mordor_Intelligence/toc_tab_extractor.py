import selenium.webdriver as webdriver
import pandas as pd
from bs4 import BeautifulSoup
import re
import time
import requests


driver = webdriver.Firefox()

url = "https://www.mordorintelligence.com/industry-reports/organophosphate-pesticides-market"
driver.get(url)

segments = []
subsegments = [[] for i in range(10)]
levels = [[] for i in range(10)]


time.sleep(5)
try:
    cookies = driver.find_element_by_css_selector('/html/body/footer/div/div[2]/button').click()
    page = driver.find_element_by_xpath('/html/body/div[7]/div/div/div[2]/button/svg/g/path').click()
except:
    pass
toc_tab = driver.find_element_by_id("toc-tab").click()
try:
    cookies = driver.find_element_by_css_selector('/html/body/footer/div/div[2]/button').click()
    page = driver.find_element_by_xpath('/html/body/div[7]/div/div/div[2]/button/svg/g/path').click()
except:
    pass
time.sleep(10)
full_content = driver.find_elements_by_class_name('old-toc-content')[1]
all_ps = full_content.find_elements_by_tag_name('p')
get_market_segmentation = False
segment_spaces = 0
subsegment_spaces = 0
get_companies = False
companies = []
counter = -1
for i, ps in enumerate(all_ps):
    try:
        cookies = driver.find_element_by_css_selector('/html/body/footer/div/div[2]/button').click()
        page = driver.find_element_by_xpath('/html/body/div[7]/div/div/div[2]/button/svg/g/path').click()
    except:
        pass
    ps_content = ps.text
    total_spaces = 0
    for text in ps_content:
        if(text == ' '):
            total_spaces += 1
        else:
            break
    if((total_spaces == 0) and ('company' in ps_content.split())):
        print("Companies_Heading = ", ps_content)
        get_companies = True
    elif((total_spaces == 0) and (('market' in ps_content.split()) and ('segmentation' in ps_content.split()))):
        get_market_segmentation = True
        next_ps_content = all_ps[i+1].text
        for text in next_ps_content:
            if(text == ' '):
                segment_spaces += 1
            else:
                break
            #print(ps_content)
    elif((total_spaces == 0) and ((get_market_segmentation) or (get_companies))):
        print("<----- Finishing the Work ----> ")
        #print(ps_content)
        if(get_market_segmentation):
            get_market_segmentation = False
        if(get_companies):
            get_companies = False
    elif(get_market_segmentation):
        if(total_spaces != segment_spaces):
            if(subsegment_spaces == 0):
                subsegment_spaces = total_spaces
        a = 1
        print("Segment Spaces = ", segment_spaces, "  -Content = ", ps_content)
        print("Subsegment Spaces = ", subsegment_spaces, " - Content = ", ps_content)
        #content = ps_content.split(".")[-1][2:]
        ps_content = " ".join(re.sub(r"[ ]{2,}|^\d+.|.\d+|\s\d\s+$", '', ps_content).split()[1:])
        if(total_spaces == segment_spaces):
            segments.append(ps_content)
            counter += 1
        elif(total_spaces == subsegment_spaces):
            subsegments[counter].append(ps_content)
        else:
            levels[counter].append(ps_content)
    elif(get_companies):
        ps_content = " ".join(re.sub(r"[ ]{2,}|^\d+.|.\d+|\s\d\s+$", '', ps_content).split()[1:])
        companies.append(ps_content)
        #print(ps_content)
        #print()
#except Exception as e:
#    print("Exception = ", e)





def printt(storage):
    for content in storage:
        print(content)
        print()


print("\n\n------------------------------\n\n")
printt(segments)


print("\n\n------------------------------\n\n")
printt(subsegments)


print("\n\n------------------------------\n\n")
printt(levels)

print("\n\n------------------------------\n\n")
print("Companies ---- ")
print(companies)

time.sleep(3)
driver.close()