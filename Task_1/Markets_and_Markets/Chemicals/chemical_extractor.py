from bs4 import BeautifulSoup
import requests
import pandas as pd



links = []
titles = []
dates = []
descriptions = []
market_size = []
forecasted_market_size = []
CAGR = []

for i in range(23):
    url = "https://www.marketsandmarkets.com/chemicals-market-research-10.html"
    if(i):
        url = "https://www.marketsandmarkets.com/chemicals-market-research-10_" + str(i) + ".html"

    response = requests.get(url)
    print(response.status_code)
    html = response.text
    soup = BeautifulSoup(response.content, 'lxml')
    main_class = soup.find(class_ = "markeList")
    #print("len of all markelist = ", len(main_class))
    all_trs = main_class.findAll('li', recursive=False)
    print("Len of all trs = ", len(all_trs))

    
    for i in range(0, len(all_trs)):
        #print("TRS = ", all_trs[i])
        title_section = all_trs[i].find('h3')
        #print("Title Section = ", title_section)
        a_tag = title_section.find('a')
        link = a_tag['href']
        p_tag = all_trs[i].find('p')
        description = p_tag.text
        #descriptions.append(description)
        words = description.split()


        #MARKET_SIZE
        count = 0
        for index, word in enumerate(words):
            if(word == 'USD'):
                if(count == 0):
                    market_size.append(" ".join(words[index: index+3]))
                if(count == 1):
                    forecasted_market_size.append(" ".join(words[index:index+3]))
                count+=1
                if(count == 2):
                    break
                
        if(count==0):
            market_size.append('NA')
            forecasted_market_size.append('NA')
        elif(count == 1):
            forecasted_market_size.append('NA')


        ##CAGR
        got_percent = False
        for index, word in enumerate(words):
            if(word[-1] == '%'):
                CAGR.append(word)
                got_percent = True
                break
        if(not got_percent):
            CAGR.append('None')


        #Links
        links.append('https://www.marketsandmarkets.com' + link)
        title = a_tag.text
        titles.append(title)
        #tds = all_trs[i].find_all('td')
        #date = tds[1].text
        #dates.append(date)
        print("i = ", i, " finished")

print(len(titles), len(links), len(market_size), len(forecasted_market_size), len(CAGR))
dictionary = {'Title': titles, 'Link': links, 'Market size': market_size, 'Forecasted Market Size': forecasted_market_size, 'CAGR (%)': CAGR}
file = pd.DataFrame(dictionary)
file.to_csv('chemical_helper_file.csv')