import selenium.webdriver as webdriver
import pandas as pd
from bs4 import BeautifulSoup
import re
import requests


#url = 'https://www.mordorintelligence.com/industry-reports/facility-management-market-kuwait'
#url = 'https://www.mordorintelligence.com/industry-reports/optical-wavelength-services-market'
url = 'https://www.mordorintelligence.com/industry-reports/utility-billing-software'


response = requests.get(url)
soup = BeautifulSoup(response.content, 'lxml')
main_section = soup.find(class_ = 'page-content')
all_parent_divs = main_section.find_all('div', recursive = False)




def printt(storage):
    for content in storage:
        print(content)
        print()


segment = []
subsegment = []
levels = []
for div in all_parent_divs:
    got_market_segmentation = False
    alternate_market_segmentation_section = ''
    heading_class = div.find(class_ = 'component-heading')
    try:
        heading_splitted_text = heading_class.text.lower().split()
        if(('table' in heading_splitted_text) and ('contents' in heading_splitted_text)):
            ol_section = div.find('ol')
            all_parent_lis = ol_section.find_all('li', recursive = False)
            print("Length of all_parent_lis = ", len(all_parent_lis))
            for i, li in enumerate(all_parent_lis):
                first_p_tag = li.find('p')
                first_p_splitted_text = first_p_tag.text.lower().split()
                print(first_p_splitted_text)
                if(('market' in first_p_splitted_text) and ('dynamics' in first_p_splitted_text)):
                    alternate_market_segmentation_section = all_parent_lis[i+1]
                    print("Alternate market segmentation ki jay ho")

                if(('market' in first_p_splitted_text) and ('segmentation' in first_p_splitted_text)):
                    got_market_segmentation = True
                    internal_ol_section = li.find('ol')
                    all_internal_lis = internal_ol_section.find_all('li', recursive = False)
                    for internal_li in all_internal_lis:
                        segment_section = internal_li.find('p')
                        segment_text = " ".join(segment_section.text.split()[1:])
                        segment.append(segment_text)
                        subseg_store = []
                        levels_store = []
                        subseg_ols = internal_li.find('ol')
                        subseg_lis = subseg_ols.find_all('li', recursive = False)
                        for subseg_li in subseg_lis:
                            p = subseg_li.find('p')
                            subseg_store.append(" ".join(p.text.split()[1:]))
                            levels_ol = subseg_li.find('ol')
                            if(levels_ol):
                                levels_lis = levels_ol.find_all('li', recursive = False)
                                for levels_li in levels_lis:
                                    levels_text = " ".join(levels_li.text.split()[1:])
                                    levels_store.append(levels_text)
                        subseg_store = "; ".join(subseg_store)
                        
                        if(not len(levels_store)):
                            levels.append('NA')
                        else:
                            levels.append("; ".join(levels_store))
                        a = 1
                        if(not len(subseg_store)):
                            subsegment.append('NA')
                        else:
                            subsegment.append(subseg_store)
            print("got market segmentation " , got_market_segmentation, " hai ")
            if(not got_market_segmentation):
                print("Andar toh aa gaya bhai alternate ke")
                internal_ol_section = alternate_market_segmentation_section.find('ol')
                all_internal_lis = internal_ol_section.find_all('li', recursive = False)
                for internal_li in all_internal_lis:
                    segment_section = internal_li.find('p')
                    segment_text = " ".join(segment_section.text.split()[1:])
                    segment.append(segment_text)
                    subseg_store = []
                    levels_store = []
                    subseg_ols = internal_li.find('ol')
                    subseg_lis = subseg_ols.find_all('li', recursive = False)
                    for subseg_li in subseg_lis:
                        p = subseg_li.find('p')
                        subseg_store.append(" ".join(p.text.split()[1:]))
                        levels_ol = subseg_li.find('ol')
                        if(levels_ol):
                            levels_lis = levels_ol.find_all('li', recursive = False)
                            for levels_li in levels_lis:
                                levels_text = " ".join(levels_li.text.split()[1:])
                                levels_store.append(levels_text)
                    subseg_store = "; ".join(subseg_store)
                    
                    if(not len(levels_store)):
                        levels.append('NA')
                    else:
                        levels.append("; ".join(levels_store))
                    a = 1
                    if(not len(subseg_store)):
                        subsegment.append('NA')
                    else:
                        subsegment.append(subseg_store)

        print("------------------")
    except Exception as e:
        print(e)
        print()

print("\n\n------------------------------\n\n")
printt(segment)


print("\n\n------------------------------\n\n")
printt(subsegment)
print("subsegment 1= ", subsegment[0])


def convert_function(i):
    return "Subsegment_" + str(i)

dataframe = {}
for i, subseg in enumerate(subsegment):
    try:
        dataframe[convert_function].append(subseg)
    except:
        dataframe[convert_function(i)] = [subseg]
    #print(type(convert_function(i)), " --> ", type(subseg))
# subsegment = "; ".join(subsegment)
print("Dataframe = ", dataframe)
df = pd.DataFrame(dataframe, index=[0])
df.to_csv('test.csv')

print("\n\n------------------------------\n\n")
printt(levels)
