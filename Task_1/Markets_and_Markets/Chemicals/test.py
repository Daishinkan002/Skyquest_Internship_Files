got_key_market_segments = False
counter = -1
levels_block = []
subsegments = ['NA' for i in range(19)]
level = ['NA' for i in range(19)]
for tags in all_tags:
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
        if(indicator_symbol == 'ul'):
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
                   level[counter] = ', '.join(levels_block)
                   print("Levels Block = " , levels_block)
                   levels_block = []
               if(counter == -1):
                   counter += 1
               subsegments[counter] = ", ".join([all_lis[i].find(text=True, recursive = False) for i in range(len(all_lis))])
               
           except Exception as e:
               print(e)
    if(indicator_symbol == 'p '):
        try:
            print(tags.text[1:10])
        except:
            print("Got error")
        if(tags.text[1:10] == "ey Market"):
            print(tags.text)
        if((tags.text == 'Key Market Segments ') or (tags.text == 'Key Market Segments')):
            got_key_market_segments = True
            print("Got True")
