import pandas as pd
import selenium.webdriver as webdriver
import time
import pandas as pd
from bs4 import BeautifulSoup
import re
import requests

df=pd.read_csv('technavio_healthcare_links.csv')

driver = webdriver.Firefox()
#urls=['https://www.technavio.com/report/gaming-console-market-industry-analysis']
forecasted_market_size=[]
current_market_size=[]
cagr=[]
companies=[]
segments=[]
titles=[]
subsegment_1=[]
subsegment_2=[]
subsegment_3=[]
subsegment_4=[]
subsegment_5=[]
subsegment_6=[]
subsegment_7=[]
subsegment_8=[]

links = df['Links']

links = list(links)
#print("Length of links = ", len(links))

for k in range(4):
    link = links[k]
    #for cagr, usd, segments, forecasted size, current size, companies
    print('-----------------------------------------------------------------')
    print('Link ',k)
    print(link)
    print('-------------------------------------------------------------------')
    url=link
    try:
        r=requests.get(url)
        driver.get(url)
        time.sleep(3)
    except:
        time.sleep(7)
        driver.get(url)
    
    soup=BeautifulSoup(driver.page_source,'html.parser')

    soup=soup.findAll('div',{'class':'panel-body'})
    print(len(soup))
    if len(soup)!=0:
        for i in range(len(soup)):
            if i==0:
                flag_usd1=0
                flag_usd2=0
                counter=0
                para=soup[i].text.split()
                for count in range(len(para)):
                    if para[count][0]=='$':
                        counter+=1
                for count in range(len(para)):
                    text=''
                    if para[count][0]=='$' and counter==1:
                        text=para[count]+' '+para[count+1]
                        forecasted_market_size.append(text)
                        counter-=1
                        flag_usd1=1
                    elif para[count][0]=='$' and counter==2:
                        text=para[count]+' '+para[count+1]
                        current_market_size.append(text)
                        counter-=1
                        flag_usd2=1
                if flag_usd1==0:
                    forecasted_market_size.append('NA')
                if flag_usd2==0:
                    current_market_size.append('NA')
            elif i==1:
                print(para)
                para=soup[i].text.split()
                flag_cagr=0
                for count in range(len(para)):
                    if para[count][-1]=='%':
                        cagr.append(para[count])
                        flag_cagr=1
                if flag_cagr==0:
                    cagr.append('NA')
            elif i==2:
                para=soup[i].text
                para=[para]
                print(para)
                for title in para:
                    string=title
                    balance=0
                    word=''
                    List=[]
                    for ch in string:
                        if ch=='(':
                            balance=balance+1
                        elif ch==")":
                            balance=balance-1
                        if balance>0:
                            word=word+ch
                        if balance==0 and len(word)>0:
                            if word[0]=='(':
                                word=word[1:]
                            List.append(word)
                            print('hello')
                            print(List)
                            word=''
                print(List)
                flag1=0
                flag2=0
                flag3=0
                flag4=0
                flag5=0
                flag6=0
                flag7=0
                flag8=0            
                for i in range(len(List)):
                    if i==0:
                        flag1=1
                        subsegment_1.append(List[i])
                    elif i==1:
                        flag2=1
                        subsegment_2.append(List[i])
                    elif i==2:
                        flag3=1
                        subsegment_3.append(List[i])
                    elif i==3:
                        flag4=1
                        subsegment_4.append(List[i])
                    elif i==4:
                        flag5=1
                        subsegment_5.append(List[i])
                    elif i==5:
                        flag6=1
                        subsegment_6.append(List[i])
                    elif i==6:
                        flag7=1
                        subsegment_7.append(List[i])
                    elif i==7:
                        flag8=1
                        subsegment_8.append(List[i])
                print("Flag 1:",flag1)
                print("Flag 2:",flag2)
                print("Flag 3:",flag3)
                print("Flag 4:",flag4)
                print("Flag  5:",flag5)
                print("Flag 6:",flag6)
                print("Flag 7:",flag7)
                print("Flag 8:",flag8)
                if flag1==0:
                    subsegment_1.append('NA')
                if flag2==0:
                    subsegment_2.append('NA')
                if flag3==0:
                    subsegment_3.append('NA')
                if flag4==0:
                    subsegment_4.append('NA')
                if flag5==0:
                    subsegment_5.append('NA')
                if flag6==0:
                    subsegment_6.append('NA')
                if flag7==0:
                    subsegment_7.append('NA')
                if flag8==0:
                    subsegment_8.append('NA')
            elif i==3:
                flag_com=0
                para=soup[i].text
                if len(para)!=0:
                    flag_com=1
                    companies.append(para)
                
                if flag_com==0:
                    companies.append('NA')
            else:
                break
                
    elif len(soup)==0:
        
        subsegment_1.append('NA')
        subsegment_2.append('NA')
        subsegment_3.append('NA')
        subsegment_4.append('NA')
        subsegment_5.append('NA')
        subsegment_6.append('NA')
        subsegment_7.append('NA')
        subsegment_8.append('NA')
        
        try:
            ul=0
            flag_com=0
            driver.get(url)
            time.sleep(3)
            soup=BeautifulSoup(driver.page_source,'html.parser')
            all_tags=soup.findAll(['h2','h3','p','ul','tr'])
            for i,tags in enumerate(all_tags):
                indicator_symbol = str(tags)[1]
                if(indicator_symbol == 'p' or indicator_symbol=='h'):
                    x=re.compile('key vendors|companies',re.IGNORECASE)
                    if x.search(tags.text.lower()):
                        key_player_tags=tags
                        key_player_internal_content=all_tags[i+1]
            companies_final_final=[]
            ul=key_player_internal_content
            print("UL IS:",ul)
            if len(ul)!=0:
                lis=ul.find_all('li')
                for li in lis:
                    companies_final_final.append(li.text)
                    flag_com=1
            else:
                pass
            
            ul=0
            for i,tags in enumerate(all_tags):
                indicator_symbol = str(tags)[1]
                if(indicator_symbol == 'p' or indicator_symbol=='h'):
                    x=re.compile('prominent vendors|company profiles',re.IGNORECASE)
                    if x.search(tags.text.lower()):
                        key_player_tags=tags
                        key_player_internal_content=all_tags[i+1]
            ul=key_player_internal_content
            print("UL IS:",ul)
            if len(ul)!=0:
                lis=ul.find_all('li')
                for li in lis:
                    companies_final_final.append(li.text)
                    flag_com=1
            else:
                pass
            if flag_com==1:
                companies_final_final=';'.join(companies_final_final)
                companies.append(companies_final_final)
            if flag_com==0:
                companies.append('NA')
            
                
                
                
                
                
        except:
            companies.append('NA')
        
        try:
            
            driver.get(url)
            soup=BeautifulSoup(driver.page_source,'html.parser')
            soup=soup.find('div',{'class':'inner-div'})
            soup=soup.find('p')
            para=soup.text.split()
            string=''
            usd_counter=0
            flag_usd1=0
            flag_usd2=0
            for i in range(len(para)):
                if para[i]=='USD':
                    usd_counter+=1
            for i in range(len(para)):
                if para[i]=='USD' and usd_counter==2:
                    string=para[i]+' '+para[i+1]+' '+para[i+2]
                    forecasted_market_size.append(string)
                    flag_usd1=1
                    usd_counter-=1
                elif para[i]=='USD' and usd_counter==1:
                    string=para[i]+' '+para[i+1]+' '+para[i+2]
                    current_market_size.append(string)
                    flag_usd2=1
                    usd_counter-=1
                    
            if flag_usd1==0:
                forecasted_market_size.append('NA')
            if flag_usd2==0:
                current_market_size.append('NA')
        
        except:
            forecasted_market_size.append('NA')
            current_market_size.append('NA')
        try:
            driver.get(url)
            soup=BeautifulSoup(driver.page_source,'html.parser')
            soup=soup.find('div',{'class':'inner-div'})
            soup=soup.find('p')
            para=soup.text.split()
            string=''
            flag_cagr=0
            for i in range(len(para)):
                if para[i][-1]=='%':
                    cagr.append(para[i])
                    flag_cagr=1
                    break
                elif para[i][-1]=='.' and para[i][-2]=='%':
                    string=''
                    string=para[i][:-1]
                    cagr.append(string)
                    flag_cagr=1
                    break
            if flag_cagr==0:
                cagr.append('NA')
        
        except:
            cagr.append('NA')
    else:
        pass
    #for titles    
    print(link)
    url=link
    r=requests.get(url)
    soup=BeautifulSoup(r.content,'html.parser')
    soup=soup.findAll('h1',{'class':'heading_title'})
    if len(soup)>0:    
        print(soup[0].text)
        titles.append(soup[0].text)
    else:
        titles.append('NA')  
    print("\n\n\n-----------Ending with ", k , " --------------\n\n\n")




for title in titles:
    character=[]
    List=[]
    flag=0
    flag2=0
    print('hola',title)
    para=[title]
    print(len(title))
    counter_of_dash=0
    for i,word in enumerate(title):
        if title[i]=='-':
            counter_of_dash+=1
            
    for i,word in enumerate(title):
    
        if title[i]==' ' and title[i+1]=='b' and title[i+2]=='y' and title[i+3]==' ' :
            for j in range(i+4,len(title),1):
                if counter_of_dash!=1:
                    character.append(title[j])
                    if title[j]=='-':
                        counter_of_dash-=1
                        character.pop()
                elif title[j]=='-' and counter_of_dash==1:
                    break
                
               
               
                
                
            flag2=1
        
        
    print(flag2)
    if flag2==0:
        segments.append('NA')
        continue
        
    character=''.join(character)
    print(character)
    for i,word in enumerate(character):
    
        try:
            if character[i]==',' and character[i+1]==' ' and character[i+2]=='a' and character[i+3]=='n' and character[i+4]=='d' and character[i+5]==' ':
                List=character.split(',')
                flag=1
                print(List)
                break
        except:
            pass
    print(flag)
    if flag==0:
        for i,word in enumerate(character):
            if character[i+1]==' ' and character[i+2]=='a' and character[i+3]=='n' and character[i+4]=='d' and character[i+5]==' ':
                List=character.split('and')
                flag=1
                break
    segments.append(List)
                
    
titles_final=pd.DataFrame(titles)
links_final=pd.DataFrame(links)
companies_final=pd.DataFrame(companies)
cagr_final=pd.DataFrame(cagr)
current_market_final=pd.DataFrame(current_market_size)
forecasted_market_final=pd.DataFrame(forecasted_market_size)
segments_final=pd.DataFrame(segments)
subsegment_1=pd.DataFrame(subsegment_1)
subsegment_2=pd.DataFrame(subsegment_2)
subsegment_3=pd.DataFrame(subsegment_3)
subsegment_4=pd.DataFrame(subsegment_4)
subsegment_5=pd.DataFrame(subsegment_5)
subsegment_6=pd.DataFrame(subsegment_6)
subsegment_7=pd.DataFrame(subsegment_7)
subsegment_8=pd.DataFrame(subsegment_8)
frames=[titles_final,links_final,companies_final,cagr_final,current_market_final,forecasted_market_final,segments_final,subsegment_1,subsegment_2,subsegment_3,subsegment_4,subsegment_5,subsegment_6,subsegment_7,subsegment_8]
df=pd.concat(frames,keys=['Titles','Links','Companies','CAGR(%)','Current market size','Forecasted market size','Segments','Subsegment 1','Subsegment 2','Subsegment 3', 'Subsegment 4','Subsegment 5','Subsegment 6','Subsegment 7','Subsegment 8'],axis=1)
df.to_csv('technavio healthcare.csv')

driver.close()