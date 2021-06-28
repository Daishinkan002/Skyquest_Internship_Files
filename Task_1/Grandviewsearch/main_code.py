import re
import csv
import requests
from bs4 import BeautifulSoup
from collections import defaultdict
from tqdm import tqdm


industries_file = open('industries.txt', 'r')
industries = industries_file.readlines()

for industry in industries[1:]:

    source = requests.get(
        ' https://www.grandviewresearch.com/industry/' + industry).text

    soup = BeautifulSoup(source, 'lxml')

    csv_file = open(industry[:-1] + '.csv', 'w')
    csv_writer = csv.writer(csv_file)

    DATA = []
    SEGMENTS = []
    SUB_SEGMENTS = []
    LEVELS = []

    max_seg_size = 0
    for report in tqdm(soup.find_all('div', class_='advanced_report_list')):
        
        # Title
        title = report.a.text
        
        # Link
        link = 'https://www.grandviewresearch.com' + report.a['href']
        
        # Market value
        description = report.p.text
        usd_match = re.search('(USD) ?[0-9]+.?[0-9]+ ?[a-z]+ ', description)
        if usd_match:
            revenue = usd_match.group(0)
        else:
            revenue = None
        
        # CAGR percentage
        per_match = re.search('[0-9]+.?[0-9]+ ?%', description)
        if per_match:
            cagr = per_match.group(0)
        else:
            cagr = None
        
        ind_report = requests.get(link).text
        ind_soup = BeautifulSoup(ind_report, 'lxml')
        
        # Segements, Sub-segments, Regions, and Levels
        segments_dict = defaultdict(list)

        summary = ind_soup.find('div', class_='report_summary')
        
        if summary:
            for uls in summary.find_all('ul'):
                if re.search('(.)utlook', uls.li.text):
                    for lis in uls.find_all('li'):
                        try:
                            if re.search('[a-zA-Z]* ?[a-zA-Z]* (.)utlook', lis.text):
                                seg = re.search('[a-zA-Z]* ?[a-zA-Z]* (.)utlook', lis.text).group(0)
                                levels_list = []
                                sub_segments_dict = defaultdict(list)
                                for liss in lis.find_all('li'):
                                    if liss.find('li'):
                                        for lisl in liss.find_all('li'):
                                            levels_list.append(lisl.p.text)
                                            
                                            sub_segments_dict[liss.p.text].append(lisl.p.text)
                                    else:
                                        if liss.p.text not in levels_list:
                                            sub_segments_dict[liss.p.text].append(None)
                                seg = seg.replace('Outlook', '')
                                seg = seg.replace('outlook', '')
                                segments_dict[seg] = (sub_segments_dict)
                        except:
                            pass
                
        regions = []
        segments = []
        sub_segments_dict = defaultdict(list)
        levels_dict = defaultdict(list)
        for key, value in segments_dict.items():
            segments.append(key)
            for sub_seg, lev in value.items():
                # sub_segments_val = ', '.join(value[0])
                if None not in lev:
                    levels_dict[key].extend(lev)
                else:
                    levels_dict[key].extend('')
                    
                sub_segments_dict[key].append(sub_seg)
                if key == 'Regional ':
                    regions.append(sub_seg)
        
        if not len(regions):
            regions = None
        else:
            regions = ', '.join(regions)
                    
        levels = []
        for _, value in levels_dict.items():
            value = ', '.join(value)
            levels.append(value)
        sub_segments = []
        for _, value in sub_segments_dict.items():
            value = ', '.join(value)
            sub_segments.append(value)
               
        if max_seg_size < len(sub_segments):
            max_seg_size = len(sub_segments)
        
        # Forcast value and Companies
        forecast_rev = None
        companies = None
        
        table = ind_soup.find('tbody')
        
        if table:
            
            for trs in table.find_all('tr'):
            
                if re.search('Revenue forecast in [0-9]+', trs.find_all('td')[0].text):
                    forecast_rev = trs.find_all('td')[1].text  
                
                if re.search('Key companies profiled', trs.find_all('td')[0].text):
                    companies = trs.find_all('td')[1].text
                    companies = companies.replace(';', ',')      
        
        DATA.append([title, link, revenue, forecast_rev, cagr, companies, regions])
        SEGMENTS.append([s for s in segments])
        SUB_SEGMENTS.append([s for s in sub_segments])
        LEVELS.append([l for l in levels])
    
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
