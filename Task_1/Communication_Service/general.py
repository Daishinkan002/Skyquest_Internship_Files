import selenium.webdriver as webdriver
import time
import pandas as pd
from bs4 import BeautifulSoup
import re
import requests


driver = webdriver.Firefox()
subsegment_1 = ['NA']

#links = ['https://www.technavio.com/report/global-standby-rental-power-market']
#links=['https://www.technavio.com/report/stroke-therapeutics-market-industry-analysis']
links=['https://www.technavio.com/report/lead-acid-battery-market-industry-analysis']
for kk,link in enumerate(links):
    print('----------------------------------------------------------------------')
    print(link)
    print(kk)
    if subsegment_1[kk]=='NA':
        try:
            url=link
            driver.get(url)
            print('opened')
            time.sleep(3)
            html = driver.page_source
            time.sleep(3)
            soup = BeautifulSoup(html, 'lxml')
            
            soup=soup.find('div',{'class':'inner-div'})
            
            subsegmentation_tags=[]
            all_tags=soup.findAll(['h2','h3','p','ul','tr'])
            for w,tags in enumerate(all_tags):
                indicator_symbol = str(tags)[1]
                if(indicator_symbol == 'p' or indicator_symbol=='h'):
                    x=re.compile('segmentation',re.IGNORECASE)

                    if x.search(tags.text.lower()):

                        key_player_tags=tags

                        print(key_player_tags)
                        try:
                            key_player_internal_content=all_tags[w+1]
                        except:
                            continue
                        subsegmentation_tags.append(key_player_internal_content)
            flag_1=0
            flag_2=0
            flag_3=0
            flag_4=0
            flag_5=0
            flag_6=0
            flag_7=0
            flag_8=0

            string_1=''
            string_2=''
            string_3=''
            string_4=''
            string_5=''
            string_6=''
            string_7=''
            string_8=''
            for i,ul in enumerate(subsegmentation_tags):
                tags_=ul.findAll('li')
                print("Internal Content = ", tags.text)
                print('hi')
                for k,lis in enumerate(tags_):
                    print(k,lis.text)

                    if i==0:
                        string_1=lis.text+', '+string_1
                        flag_1=1
                    elif i==1:
                        string_2=lis.text+', '+string_2
                        flag_2=1
                    elif i==2:
                        string_3=lis.text+', '+string_3
                        flag_3=1
                    elif i==3:
                        string_4=lis.text+', '+string_4
                        flag_4=1
                    elif i==4:
                        string_5=lis.text+', '+string_5
                        flag_5=1
                    elif i==5:
                        string_6=lis.text+', '+string_6
                        flag_6=1
                    elif i==6:
                        string_7=lis.text+', '+string_7
                        flag_7=1
                    elif i==7:
                        string_8=lis.text+', '+string_8
                        flag_8=1


            if len(string_1)!=0:
                string_1=string_1[:-2]
                print(string_1)
                subsegment_1[kk]=string_1
            print(string_2)
            print(string_3)
            print(string_4)
            print(string_5)
            print(string_6)
            print(string_7)
            print(string_8)
            #if len(stristring_2ng_2)!=0:
            #    print(string_2)
            #    string_2=string_2[:-2]
            #    subsegment_2[kk]=string_2
            #if len(string_3)!=0:
            #    print(string_3)
            #    string_3=string_3[:-2]
            #    subsegment_3[kk]=string_3
            #if len(string_4)!=0:
            #    print(string_4)
            #    string_4=string_4[:-2]
            #    subsegment_4[kk]=string_4
            #if len(string_5)!=0:
            #    print(string_5)
            #    string_5=string_5[:-2]
            #    subsegment_5[kk]=string_5
            #if len(string_6)!=0:
            #    print(string_6)
            #    string_6=string_6[:-2]
            #    subsegment_6[kk]=string_6
            #if len(string_7)!=0:
            #    print(string_7)
            #    string_7=string_7[:-2]
            #    subsegment_7[kk]=string_7
            #if len(string_8)!=0:
            #    print(string_8)
            #    string_8=string_8[:-2]
            #    subsegment_8[kk]=string_8
        except:
            pass
    print("XXXXXXXXXXXXX-------------------------------XXXXXX")
    if(subsegment_1[0] =='NA'):
        subsegments = ['NA' for i in range(8)]
        ul_active = False
        counter = 0
        #all_tags=soup.findAll(['h2','h3','p','ul','tr'])
        opening_closing_tag = ''
        for w,tags in enumerate(all_tags):
                indicator_symbol = str(tags)[1:3]
                if(indicator_symbol == 'p ' or indicator_symbol == 'p>' or indicator_symbol=='h2' or indicator_symbol == 'h3'):
                    x=re.compile('segmentation',re.IGNORECASE)
                    #print("Indicator_Symbol : ", indicator_symbol, " tags.text.lower = ", tags.text.lower())
                    if x.search(tags.text.lower()):
                        if(opening_closing_tag == ''):
                            opening_closing_tag = indicator_symbol
                            #print("Opened at : ", tags.text.lower)
                        ul_active = True
                    elif((not x.search(tags.text.lower())) and (indicator_symbol == opening_closing_tag)):
                        #print("Closed at : ", tags.text.lower)
                        opening_closing_tag = ''
                        ul_active = False
                if((ul_active) and (indicator_symbol == 'ul')):
                    li_array = []
                    all_lis = tags.findAll('li')
                    #print("\n\n-------------\n All_Lis text = ", tags.text, "\n------------\n\n")
                    for li in all_lis:
                        #print("Li text = ", li.text)
                        li_array.append(li.text)
                    subsegment_string = ", ".join(li_array)
                    if(subsegment_string != ''):
                        
                        if(counter == 0):
                            subsegments_1[kk] = subsegment_string
                        if(counter == 1):
                            subsegments_2[kk] = subsegment_string
                        #### ------------- Your code -----------------
                        counter +=1
                        #print("Subsegment String = ", subsegment_string)
                            
        print(counter)
        
                        
            

    print('-----------------------------------------------------------')

driver.close()