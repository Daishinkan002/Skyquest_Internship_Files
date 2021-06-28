import selenium.webdriver as webdriver
import time
import pandas as pd

x = ['healthcare_industry', 'food-and-beverages-industry', 'chemicals-and-materials-industry', 'agriculture-industry']

for j in range(1,len(x)):
    url = "https://www.fortunebusinessinsights.com/" + x[j]
    print("For url = ", url)
    options = webdriver.FirefoxOptions()
    options.headless = True
    driver = webdriver.Firefox(options = options)
    driver.get(url)

    lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    match=False
    while(match==False):
            lastCount = lenOfPage
            time.sleep(5)
            lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
            if lastCount==lenOfPage:
                match=True

    print(lenOfPage)

    titles = []
    links = []

    try:

        main_class = driver.find_element_by_id('listingsearch')
        all_lis = main_class.find_elements_by_tag_name('li')
        print("Got Lis = ", len(all_lis))
        for i, lis in enumerate(all_lis):
            h4 = lis.find_element_by_tag_name('h4')
            a_tag = h4.find_element_by_tag_name('a')
            title = a_tag.text
            link = a_tag.get_attribute('href')
            titles.append(title)
            links.append(link)
            print("\n\n I finished \n\n")
    except:
        print('Not found for url = ',x[i])
        print('\n\n--------bhag yahan se\n\n')

    print("titles length = ", len(titles), " len_links = ", len(links))

    helper_dictionary = {'Title': titles, 'Links': links}
    df = pd.DataFrame(helper_dictionary)
    df.to_csv(x[j] + '_helper_file.csv')
driver.close()

##listingsearch