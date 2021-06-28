from bs4 import BeautifulSoup
url = "https://www.alliedmarketresearch.com/recycle-textile-market"
import requests
import re


content = requests.get(url)
soup = BeautifulSoup(content.content, 'lxml')
main_block = soup.find("div", {"class": "tab-pane active talkative"})
all_tags = main_block.find_all(['p','ul', 'li'], recursive = False)
got_key_market_segments = False
counter = -1
levels_block = []
subsegments = ['NA' for i in range(19)]
level = ['NA' for i in range(19)]
key_players = []
key_player_tag = None
key_player_internal_content = None



for i, tags in enumerate(all_tags):
    indicator_symbol = str(tags)[1:3]
    print("IS = ", indicator_symbol)
    if(got_key_market_segments):
        #yahan par tum content filter karoge
        if((indicator_symbol == 'p ') or (indicator_symbol == 'p>')):
            try:
                st_tag = tags.find('strong', recursive = False)
                counter += 1    
            except Exception as e:
                print(e)
            if((tags.text == 'Key Players') or (tags.text == 'Key Players ')):
                key_player_tag = tags
                key_player_internal_content = all_tags[i+1]
                break
        if(indicator_symbol == 'ul'):
           try:
               all_lis = tags.find_all('li', recursive=False)
               for lis in all_lis:
                   #print(lis.find(text = True, recursive=False) for i in range(len(all_lis)))
                   ul = lis.find('ul')
                   if(ul):
                       #text = re.sub("\xa0", "", ul.text)
                       text = ''
                       lis = ul.find_all('li')
                       all_lists = []
                       for li in lis:
                           all_lists.append(li.text)
                       texts = all_lists
                       #texts = ul.text.split("\n")
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
                   level[counter] = ', '.join(levels_block)
                   print("Levels Block = " , levels_block)
                   levels_block = []
               if(counter == -1):
                   counter += 1
               subsegments[counter] = "; ".join([all_lis[i].find(text=True, recursive = False) for i in range(len(all_lis))])
               
           except Exception as e:
               print(e)
    if(indicator_symbol == 'p '):
        if((tags.text == 'Key Market Segments ') or (tags.text == 'Key Market Segments')):
            got_key_market_segments = True
            print("Got True")



def printt(takla):
    for a in takla:
        print(a)
        print()

print("\n\n-----------------\n\n")
printt(subsegments)
print("\n\n-----------------\n\n")
printt(level)
print("\n\n-----------------\n\n")
print(key_player_tag)
print("\n\n-----------------\n\n")
print(key_player_internal_content)
ul = key_player_internal_content
lis = ul.find_all()
for li in lis:
    print(li.text)

print("\n\n-----------------\n\n")
