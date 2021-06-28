# importing libraries
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import re
import time
import pandas as pd


driver = webdriver.Firefox()


def collector(main_url):
    search_text = input("Enter Text to search : ")
    #twotabsearchtextbox
    inputElement = driver.find_element_by_id("twotabsearchtextbox")
    inputElement.send_keys(search_text)
    #nav-search-submit-button
    enter_button = driver.find_element_by_id("nav-search-submit-button").click()
    time.sleep(2)


    #Find Main Sections Containing all tags
    run_again = True
    counter = 1
    titles = []
    links = []
    while((run_again) and (counter < 6)):
        sections = driver.find_elements_by_class_name("sg-col-4-of-12")
        print("Total_Sections Got = ", len(sections))
        run_again = False
        for section in sections:
            try:
                h2 = section.find_element_by_tag_name("h2")
                title = h2.text
                print(title)
                a_tag = h2.find_element_by_tag_name("a")
                link = a_tag.get_attribute('href')
                print(link)
                titles.append(title)
                links.append(link)
                print("\n-----------------------\n")
            except Exception as e:
                print("\n\n Exception Occured - ", e, "\n\n")

        try:
            a_divs_last = driver.find_elements_by_class_name("a-last")
            for a_div in a_divs_last:
                print("Opposition = ", a_div.text)
                if(a_div.text.split()[0] == "Next→"):
                    run_again = True
                    print("Got Next Page")
                    next_page_link = a_div.find_element_by_tag_name("a").get_attribute('href')
                    driver.get(next_page_link)
                    break
        except Exception as e:
            print("\n\nException Occured in changing pages -> ", e, "\n\n")

        counter += 1
        print("\n\n\n\n--------------")
        print("---------------\nJai Jai Shree Ram\n----------\n\n\n\n\n")
    
    dictionary = {"titles": titles, "links": links}
    df = pd.DataFrame(dictionary)
    df.to_csv(search_text + ".csv")



if __name__ == '__main__':
    main_url = "https://www.amazon.in/"
    driver.get(main_url)
    collector(main_url)

    