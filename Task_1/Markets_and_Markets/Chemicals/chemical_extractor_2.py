from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

df = pd.read_csv('chemical_helper_file.csv')
market_helper = df['Market size']
cagr_helper = df['CAGR (%)']
forecast_helper = df['Forecasted Market Size']
links = df['Link']


class Chemical_Extractor:
    def __init__(self, url, index):
        self.index = index
        self.url = url
        self.market_size = 'NA'
        self.forecasted_market_size = 'NA'
        self.cagr = 'NA'
        self.companies = ['NA']
        self.geographies = ['NA']
        self.segments = ['NA']
        self.subsegments = ['NA' for i in range(19)]
        self.level = ['NA' for i in range(14)]
        self.table_dictionary = {}

    def preprocessing(self):
        response = requests.get(self.url)
        html = response.text
        soup = BeautifulSoup(response.content, 'lxml')
        related_section = soup.find(class_ = 'reportTabContent')
        self.get_initials(related_section)
        rel_tags = related_section.findAll(['h3', 'table', 'ul', 'p', 'h2', 'h4'], recursive = False)
        self.extraction(rel_tags)
        


    def get_companies(self):
        for keys in self.table_dictionary.keys():
            if(('Companies' in keys.split()) or ('Companie' in keys.split())):
                self.companies[0] = self.table_dictionary[keys]

    def get_geographies(self):
        for keys in self.table_dictionary.keys():
            if (('Geographies' in keys.split()) or ('Regions' in keys.split()) or ('Geographie' in keys.split()) or ('Region' in keys.split())):
                self.geographies[0] = self.table_dictionary[keys]
        
    
    def get_segments(self):
        for keys in self.table_dictionary.keys():
            if(('Segments' in keys.split()) or ('Segment' in keys.split())):
                self.segments[0] = self.table_dictionary[keys]
        


    def fill_table(self, tags):
        tbody = tags.find('tbody')
        all_trs = tbody.find_all('tr', recursive = False)
        for trs in all_trs:
            #print("Trs = ", trs)
            all_tds = trs.find_all('td', recursive = False)
            key = ''
            try:
                key = re.sub('\n|\xa0', '', all_tds[0].text)[:-1]
            except:
                pass
            value = ''
            try:
                value = re.sub('\n|\xa0', '', all_tds[1].text)
                if(',' in value):
                    pass
                else:
                    value = re.sub('\xa0', '', all_tds[1].text)
                    texts = value.split("\n")
                    length = len(texts)
                    i=0
                    while(i<(length-1)):
                        if(texts[i] == '' or texts[i] == " "):
                            texts.pop(i)
                            length = length-1
                        else:
                            i+=1
                    value = ", ".join(texts)

            except:
                pass
            self.table_dictionary[key] = value


    def get_market_size(self, words):
        count = 0
        for index, word in enumerate(words):
            if(word == 'USD'):
                if(count == 0):
                    self.market_size = " ".join(words[index: index+3])
                if(count == 1):
                    self.forecasted_market_size = " ".join(words[index:index+3])
                count+=1
                if(count == 2):
                    break
                
        if(count==0):
            self.market_size = market_helper[self.index]
            self.forecasted_market_size = forecast_helper[self.index]
        elif(count == 1):
            self.forecasted_market_size = forecast_helper[self.index]

    def get_cagr(self, words):
        got_percent = False
        for index, word in enumerate(words):
            if(word[-1] == '%'):
                self.cagr = word
                got_percent = True
                break
        if(not got_percent):
            self.cagr = cagr_helper[self.index]

    def get_initials(self, related_section):
        rel_p = related_section.find('p')
        description = rel_p.text
        words = description.split()
        self.get_market_size(words)
        self.get_cagr(words)
        


    def extraction(self, rel_tags):
        counter = -1
        level_counter = 0
        got_table = False
        levels_block = []
        got_target_audience = False
        for tags in rel_tags:
            indicator_symbol = str(tags)[1:3]
            #print(indicator_symbol)

            #print("\n----------------------------------------")
            #print("Tags Init= ", tags)
            #print()
            if(got_table):
                if((indicator_symbol == 'h3') or (indicator_symbol == 'h4')):
                    table_h3_tags = tags
                    if((table_h3_tags.text != None) and (('target' in table_h3_tags.text.split()) or \
                    ('Target' in table_h3_tags.text.split()) or ('Audience' in table_h3_tags.text.split()) or ('Report' in table_h3_tags.text.split()) or ('report' in table_h3_tags.text.split()))):
                        got_target_audience = True
                        continue
                    if(('Region' in str(tags.text).split()) or ('region' in str(tags.text).split()) or ('region,' in str(tags.text).split()) \
                        or ('Region,' in str(tags.text).split()) or ('Region:' in str(tags.text).split()) or ('region:' in str(tags.text).split())):
                        alt_tags = tags.find_next('ul')
                        counter += 1
                        all_lis = alt_tags.find_all('li', recursive = False)
                        for lis in all_lis:
                            
                            all_uls = lis.find_all('ul')
                            for ul in all_uls:
                                text = re.sub("\xa0", "", ul.text)
                                texts = ul.text.split("\n")
                                length = len(texts)
                                i=0
                                while(i<(length-1)):
                                    if(texts[i] == '' or texts[i] == " "):
                                        texts.pop(i)
                                        length = length-1
                                    else:
                                        i+=1
                                texts = ", ".join(texts)
                                levels_block.append(texts)
                                print("Levels Block = " , levels_block)
                        if(len(levels_block)):
                            self.level[counter] = ', '.join(levels_block)
                            levels_block = []
                        break
                    else:
                        counter += 1

                
                
                if(indicator_symbol == 'ul'):
                    if(not got_target_audience):
                        try:
                            all_lis = tags.find_all('li', recursive=False)
                            for lis in all_lis:
                                #print(lis.find(text = True, recursive=False) for i in range(len(all_lis)))
                                ul = lis.find('ul')
                                if(ul):
                                    text = re.sub("\xa0", "", ul.text)
                                    texts = ul.text.split("\n")
                                    length = len(texts)
                                    i=0
                                    while(i<(length-1)):
                                        if(texts[i] == '' or texts[i] == " "):
                                            texts.pop(i)
                                            length = length-1
                                        else:
                                            i+=1
                                    texts = ", ".join(texts)
                                    levels_block.append(texts)
                            if(len(levels_block)):
                                if(counter == -1):
                                    counter +=1 
                                self.level[counter] = ', '.join(levels_block)
                                print("Levels Block = " , levels_block)
                                levels_block = []
                            if(counter == -1):
                                counter += 1
                            self.subsegments[counter] = ", ".join([all_lis[i].find(text=True, recursive = False) for i in range(len(all_lis))])
                            h2_tag = tags.find('h2', recursive=False)
                            if(('Recent' in h2_tag.text.split()) or ('Development' in h2_tag.text.split()) or ('development' in h2_tag.text.split())):
                                break
                            h3_tag = tags.find('h3', recursive=False)
                            if(('Recent' in h3_tag.text.split()) or ('Development' in h3_tag.text.split()) or ('development' in h3_tag.text.split())):
                                break
                        except Exception as e:
                            print(e)
                    else:
                        print("got_target_audience")
                        got_target_audience = False
                        continue
                
                if((indicator_symbol == 'p ') or (indicator_symbol == 'p>')):
                    try:
                        st_tag = tags.find('strong', recursive = False)
                        if(('Region' in str(st_tag.text).split()) or ('region' in str(st_tag.text).split()) or ('region,' in str(st_tag.text).split()) \
                            or ('Region,' in str(st_tag.text).split()) or ('Region:' in str(st_tag.text).split()) or ('region:' in str(st_tag.text).split())):
                            #print("Came Inside region")
                            alt_tags = st_tag.find_next('ul')
                            counter += 1
                            all_lis = st_tag.find_all('li', recursive = False)
                            for lis in all_lis:
                                all_uls = lis.find_all('ul')
                                for ul in all_uls:
                                    text = re.sub("\xa0", "", ul.text)
                                    texts = ul.text.split("\n")
                                    i = 0
                                    length = len(texts)
                                    while(i<(length-1)):
                                        if(texts[i] == '' or texts[i] == " "):
                                            texts.pop(i)
                                            length = length-1
                                        else:
                                            i+=1
                                    texts = ", ".join(texts)
                                    levels_block.append(texts)
                                    print("Levels Block = " , levels_block)
                            if(len(levels_block)):
                                self.level[counter] = ', '.join(levels_block)
                                levels_block = []
                            break
                        else:
                            counter += 1
                            
                    except Exception as e:
                        print(e)

                if(indicator_symbol == 'h2'):
                    table_h2_tags = tags
                    print(tags.text.split())
                    if((table_h2_tags.text != None) and (('target' in table_h2_tags.text.split()) or \
                    ('Target' in table_h2_tags.text.split()) or ('Audience' in table_h2_tags.text.split()))):
                        got_target_audience = True
                    if(('Developments' in str(tags.text).split()) or ('developments,' in str(tags.text).split()) or \
                        ('Region' in str(tags.text).split()) or ('region' in str(tags.text).split()) or ('region,' in str(tags.text).split()) \
                        or ('Region,' in str(tags.text).split()) or ('Region:' in str(tags.text).split()) or ('region:' in str(tags.text).split())):
                        break

            if(indicator_symbol == 'ta'):
                self.fill_table(tags)
                self.get_companies()
                self.get_geographies()
                self.get_segments()
                table_h2_tags = tags.find_all('h2')
                if(len(table_h2_tags)> 0):
                    table_h2_tags = table_h2_tags[-1]
                #print(table_h2_tags.text)
                    if((table_h2_tags.text != None) and (('target' in table_h2_tags.text.split()) or \
                        ('Target' in table_h2_tags.text.split()) or ('Audience' in table_h2_tags.text.split()))):
                        got_target_audience = True;
                got_table = True
            
                
    
    def pprint(self):
        print("\n\n------------------\n\n")
        print("Table Dictionary = ", self.table_dictionary)
        print("\n\n------------------\n\n")
        print("CAGR = ", self.cagr)
        print("\n\n------------------\n\n")
        print("Market Size = ", self.market_size)
        print("\n\n------------------\n\n")
        print("Forecasted = ", self.forecasted_market_size)
        print("\n\n------------------\n\n")
        print("Companies = ", self.companies)
        print("\n\n------------------\n\n")
        print("Geographies = ",self.geographies)
        print("\n\n------------------\n\n")
        print("Segments = ", self.segments)
        print("\n\n------------------\n\n")
        for i in range(len(self.subsegments)):
            print("Subsegments = ", self.subsegments[i])
            print()
        print("\n\n------------------\n\n")
        for i in range(len(self.level)):
            print("Levels = ", self.level[i])
            print()
        print("\n\n------------------\n\n")
        
    
    def get_attributes(self):
        return self.market_size, self.forecasted_market_size, self.cagr, self.companies, self.geographies, self.segments, self.subsegments, self.level


market_size_list = []
forecasted_market_size_list = []
cagr_list = []
companies_list = []
geographies_list = []
segments_list = []

subsegments_1 = []
subsegments_2 = []
subsegments_3 = []
subsegments_4 = []
subsegments_5 = []
subsegments_6 = []
subsegments_7 = []
subsegments_8 = []
subsegments_9 = []
subsegments_10 = []
subsegments_11 = []
subsegments_12 = []
subsegments_13 = []
subsegments_14 = []
subsegments_15 = []
subsegments_16 = []
subsegments_17 = []
subsegments_18 = []
subsegments_19 = []

levels_1 = []
levels_2 = []
levels_3 = []
levels_4 = []
levels_5 = []
levels_6 = []
levels_7 = []
levels_8 = []
levels_9 = []
levels_10 = []
levels_11 = []
levels_12 = []
levels_13 = []
levels_14 = []

titles_list = df['Title']
#links = ['https://www.marketsandmarkets.com/Market-Reports/starter-culture-market-213083494.html']
for i, url in enumerate(links):
#urls = ['https://www.marketsandmarkets.com/Market-Reports/mobile-wireless-backhaul-market-1034.html']
#for i,url in enumerate(urls):
    chemical_data = Chemical_Extractor(url, i)
    chemical_data.preprocessing()
    chemical_data.pprint()
    mark, forecast_mark, cagr, comp, geo, seg, subseg, lev = chemical_data.get_attributes()

    market_size_list.append(mark)
    
    forecasted_market_size_list.append(forecast_mark)
    
    cagr_list.append(cagr)

    companies_list.append(comp[0])
    geographies_list.append(geo[0])
    segments_list.append(seg[0])
    subsegments_1.append(subseg[0])
    subsegments_2.append(subseg[1])
    subsegments_3.append(subseg[2])
    subsegments_4.append(subseg[3])
    subsegments_5.append(subseg[4])
    subsegments_6.append(subseg[5])
    subsegments_7.append(subseg[6])
    subsegments_8.append(subseg[7])
    subsegments_9.append(subseg[8])
    subsegments_10.append(subseg[9])
    subsegments_11.append(subseg[10])
    subsegments_12.append(subseg[11])
    subsegments_13.append(subseg[12])
    subsegments_14.append(subseg[13])
    subsegments_15.append(subseg[14])
    subsegments_16.append(subseg[15])
    subsegments_17.append(subseg[16])
    subsegments_18.append(subseg[17])
    subsegments_19.append(subseg[18])
    levels_1.append(lev[0])
    levels_2.append(lev[1])
    levels_3.append(lev[2])
    levels_4.append(lev[3])
    levels_5.append(lev[4])
    levels_6.append(lev[5])
    levels_7.append(lev[6])
    levels_8.append(lev[7])
    levels_9.append(lev[8])
    levels_10.append(lev[9])
    levels_11.append(lev[10])
    levels_12.append(lev[11])
    levels_13.append(lev[12])
    levels_14.append(lev[13])
    print(" -------------- ", i, " Finished -------------------------")

dictionary = {'Title': titles_list, 'Link': links, 'Market size': market_size_list, 'Forecasted Market Size': forecasted_market_size_list,\
     'CAGR (%)': cagr_list, 'Companies': companies_list, 'Geographies/Region': geographies_list, 'Segments': segments_list, \
         'Sub-segment 1': subsegments_1, 'Sub-segment 2': subsegments_2, 'Sub-segment 3': subsegments_3, 'Sub-segment 4': subsegments_4,\
              'Sub-segment 5': subsegments_5,'Sub-segment 6': subsegments_6,'Sub-segment 7': subsegments_7,'Sub-segment 8': subsegments_8,\
                'Sub-segment 9': subsegments_9,'Sub-segment 10': subsegments_10,'Sub-segment 11': subsegments_11,'Sub-segment 12': subsegments_12\
                    ,'Sub-segment 13': subsegments_13,'Sub-segment 14': subsegments_14,'Sub-segment 15': subsegments_15,'Sub-segment 16': \
                        subsegments_16,'Sub-segment 17': subsegments_17,'Sub-segment 18': subsegments_18,'Sub-segment 19': subsegments_19, \
                            'Level 1': levels_1, 'Level 2': levels_2, 'Level 3': levels_3, 'Level 4': levels_4, 'Level 5': levels_5 \
                                , 'Level 6': levels_6, 'Level 7': levels_7, 'Level 8': levels_8, 'Level 9': levels_9, 'Level 10': levels_10\
                                    , 'Level 11': levels_11, 'Level 12': levels_12, 'Level 13': levels_13, 'Level 14': levels_14}





save_df = pd.DataFrame(dictionary)

save_df.to_csv('Chemicals.csv')
