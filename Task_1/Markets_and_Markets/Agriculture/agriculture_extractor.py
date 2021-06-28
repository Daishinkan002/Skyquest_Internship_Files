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

for i in range(5):
    url = "https://www.marketsandmarkets.com/agriculture-market-research-173.html"
    if(i):
        url = "https://www.marketsandmarkets.com/agriculture-market-research-173_" + str(i) + ".html"

    response = requests.get(url)
    print(response.status_code)
    html = response.text
    soup = BeautifulSoup(response.content, 'lxml')
    all_trs = soup.findAll('tr')
    print("Len of all trs = ", len(all_trs))

    
    for i in range(1, len(all_trs)-1):
        a_tag = all_trs[i].find('a')
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
file.to_csv('helper_file.csv')