# importing libraries
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import re

driver = webdriver.Firefox()


# Storing file in the form of -----
# Title || Price || Rating || Availability Status || Manufacturer || Country of Origin || Product Description || Reviews || Reviews_Rating


def main(URL):
    # openning our output file in append mode
    driver.get(URL)
    File = open("out.csv", "a")

    # specifying user agent, You can use other user agents
    # available on the internet
    HEADERS = ({'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'})

    # Making the HTTP Request
    webpage = requests.get(URL, headers=HEADERS)

    # Creating the Soup Object containing all data
    soup = BeautifulSoup(webpage.content, "lxml")

    # retreiving product title
    try:
        # Outer Tag Object
        title = soup.find("span", 
                attrs={"id": 'productTitle'})

        # Inner NavigableString Object
        title_value = title.string

        # Title as a string value
        title_string = title_value.strip().replace(',', '')

    except AttributeError:
        title_string = "NA"
    print("product Title = ", title_string)

    # saving the title in the file
    File.write(f"{title_string},")

    # retreiving price
    try:
        price = soup.find("span", attrs={'id': 'priceblock_ourprice'}).string.strip().replace(',', '')
        # we are omitting unnecessary spaces
        # and commas form our string
    except AttributeError:
        price = "NA"
        try:
            price = soup.find("span", attrs={'id': 'priceblock_dealprice'}).string.strip().replace(',', '')
        except:
            pass
        
    print("Products price = ", price)

    # saving
    File.write(f"{price},")

    # retreiving product rating
    try:
        rating = soup.find("i", attrs={
            'class': 'a-icon a-icon-star a-star-4-5'}).string.strip().replace(',', '')

    except AttributeError:

        try:
            rating = soup.find("span", attrs={'class': 'a-icon-alt'}).string.strip().replace(',', '')
        except:
            rating = "NA"
    print("Overall rating = ", rating)

    File.write(f"{rating},")

    try:
        review_count = soup.find(
                "span", attrs={'id': 'acrCustomerReviewText'}).string.strip().replace(',', '')

    except AttributeError:
        review_count = "NA"
    print("Total reviews = ", review_count)
    File.write(f"{review_count},")

    # print availiblility status
    try:
        available = soup.find("div", attrs={'id': 'availability'})
        available = available.find("span").string.strip().replace(',', '')

    except AttributeError:
        available = "NA"
    print("Availability = ", available)

    # saving the availibility and closing the line
    File.write(f"{available},")

    

    #Manufacturer, Country_of_Origin Extract from plain list
    manufacturer = 'NA'
    country_of_origin = 'NA'
    try:
        specifications = driver.find_element_by_id("biss-product-specification-product-details-link").click()
    except:
        pass
    try:
        product_div = driver.find_element_by_id("detailBullets_feature_div")
        main_ul = product_div.find_element_by_tag_name("ul")
        all_lis = main_ul.find_elements_by_tag_name("li")
        for lis in all_lis:
            try:
                textual_part = re.sub(',', '', lis.text)
                list_of_text = textual_part.split()
                if(list_of_text[0] == 'Manufacturer'):
                    manufacturer = " ".join(list_of_text[2:])
                if((list_of_text[0] == 'Country') and  (list_of_text[1]=='of') and (list_of_text[2] =='Origin')):
                    country_of_origin = " ".join(list_of_text[4:])
            except:
                pass
    except Exception as e:
        print("\n\n--------------Exception Occurred ------------ ")
        print(e, "\n\n")
    


    # Manufacturer and Country of Origin Type 2 Table wala
    try:
        table_section_product_details = driver.find_element_by_id("productDetails_techSpec_section_1")
        all_trs = table_section_product_details.find_elements_by_tag_name("tr")
        for tr in all_trs:
            th = tr.find_element_by_tag_name("th")
            td = tr.find_element_by_tag_name("td")
            if(th.text == 'Manufacturer'):
                manufacturer = td.text
            if(th.text == 'Country of Origin'):
                country_of_origin = td.text
    except Exception as e:
        print("\n\n--------------Exception Occurred ------------ ")
        print(e, "\n\n")

    manufacturer = re.sub(',|;', '', manufacturer)
    manufacturer = re.sub('\n', ' ', manufacturer)

    #Saving manufacturer and country of origin
    print("Manufacturer = ", manufacturer)
    File.write(f"{manufacturer},")
    print("Country Of Origin = ", country_of_origin)
    File.write(f"{country_of_origin},")



    #Product Description ---
    product_description = "NA"
    try:
        description_block = driver.find_element_by_id("productDescription_feature_div")
        p_tag = description_block.find_elements_by_tag_name("p")
        product_description = re.sub(',|;', '', " ".join([p.text for p in p_tag]))
        product_description = re.sub('\n', '___', product_description)  # ___ for identifying new line
    except Exception as e:
        print("\n\n---------------Exception Occurred in Extracting Product Description ------------")
        print(e)


    #If Product Description is not given --- Extract from the bullet points given in about product section
    if(product_description == "NA"):
        try:
            description_block = driver.find_element_by_id("feature-bullets")
            main_ul = description_block.find_element_by_tag_name("ul")
            all_lis = main_ul.find_elements_by_tag_name('li')
            full_text = " ".join(all_lis)
            product_description = re.sub(',|;', '', full_text)
            product_description = re.sub('\n', ' ', product_description)
        except Exception as e:
            print("\n\n---------------Exception Occurred in Extracting Product Description ------------")
            print(e)


    print("\n\nProduct Description = ", product_description, "--")
    File.write(f"{product_description},")
    
    # Extracting Reviews ------------->
    reviews = "NA"
    reviews_rating = "NA"
    try:
        run = True
        reviews_full_section = driver.find_element_by_id("reviewsMedley")
        all_ids= driver.find_elements_by_id("cr-pagination-footer-0")
        for ids in all_ids:
            all_anchors = id.find_elements_by_tag_name("a")
            for anchor in all_anchors:
                if(anchor.text == "See all reviews"):
                    anchor.click()
                    print("\n\n\nClicked the necessary anchor tag\n\n\n")
                    run = False
                    break
            if(not run):
                break

        all_reviews = []
        all_review_ratings = []
        if(run):
            reviews_full_section = driver.find_element_by_id("reviews-medley-footer")
            a_tag = reviews_full_section.find_element_by_css_selector(".a-link-emphasis").click()        
        parent_review_tag = driver.find_element_by_id("cm_cr-review_list")
        all_div = parent_review_tag.find_elements_by_class_name("a-section.review.aok-relative")
        for div in all_div:
            a_row_div = div.find_element_by_class_name("a-row")
            i = 1   
            a_link_normal = a_row_div.find_elements_by_class_name("a-link-normal")[1]
            icon_span = div.find_element_by_class_name("a-icon-alt")
            all_reviews.append(a_link_normal.text)
            all_review_ratings.append(icon_span.get_attribute('innerHTML'))
            print(a_link_normal.text, " }---{ ", icon_span.get_attribute('innerHTML'))
            print("\n------------------\n")
        #next_button = driver.find_element_by_class_name("a-last").click()
        #current_url = next_url
        #next_url = driver.current_url
        #driver.get(next_url)
        #print("\n\n\n\nJAI JAI SHREE RAM\n\n\n\n")
        
        
        
        reviews = "|| ".join(all_reviews)
        reviews = re.sub(',|;', '', reviews)
        reviews = re.sub('\n', ' ', reviews)

        reviews_rating = "|| ".join(all_review_ratings)
        reviews_rating = re.sub(',|;', '', reviews_rating)
        reviews_rating = re.sub('\n', ' ', reviews_rating)
    except Exception as e:
        print("\n\n--------> Exception Occured <-----------\n ")
        print(e)
        print("\n\n")

    
    File.write(f"{reviews},")
    File.write(f"{reviews_rating},\n")


    # closing the file
    File.close()


if __name__ == '__main__':
    # openning our url file to access URLs
    file = open("list.txt", "r")

    # iterating over the urls
    for links in file.readlines():
        main(links)

driver.close()


'''
Testing Links _--------->

https://www.amazon.in/WOL-3D-Original-Creality-Printer/dp/B089W7J8L3/ref=sr_1_1_sspa?dchild=1&keywords=3d+printers&qid=1623388325&sr=8-1-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUFIR1o1WDVONjBSQUwmZW5jcnlwdGVkSWQ9QTA0MzAxMjYxV0VUN0s0RklHUTQ5JmVuY3J5cHRlZEFkSWQ9QTA1NzQ2NTAxR1dBTkQ5Nlk0QzdBJndpZGdldE5hbWU9c3BfYXRmJmFjdGlvbj1jbGlja1JlZGlyZWN0JmRvTm90TG9nQ2xpY2s9dHJ1ZQ==
https://www.amazon.in/Super-Personalized-McQueen-Theme-Combo/dp/B096QND58Z/ref=sr_1_1_sspa?dchild=1&keywords=cars&qid=1623396780&sr=8-1-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUFZQ09aTVBaQkpMVFEmZW5jcnlwdGVkSWQ9QTA3NzAyMjZZTDFPVVpXNU1BWk4mZW5jcnlwdGVkQWRJZD1BMDg5MDE4MUtEWUg4UjVJRVZSQiZ3aWRnZXROYW1lPXNwX2F0ZiZhY3Rpb249Y2xpY2tSZWRpcmVjdCZkb05vdExvZ0NsaWNrPXRydWU=
https://www.amazon.in/dp/B08SLY3KPX/ref=sspa_dk_detail_3?psc=1&pd_rd_i=B08SLY3KPX&pd_rd_w=jPD32&pf_rd_p=22b566f7-b705-4003-ab1d-17d90225e15f&pd_rd_wg=9VYvS&pf_rd_r=QXABHRG5YWE25D947EK1&pd_rd_r=861ccd7f-d6f3-4ab7-8094-88b2b6080e9a&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUExUlpIWTFDMDFUUkhKJmVuY3J5cHRlZElkPUEwMDk1ODA4MUU4SVBTSzlINTAxWSZlbmNyeXB0ZWRBZElkPUEwOTgwOTU3MlZGVDdIOFpXSUs5QSZ3aWRnZXROYW1lPXNwX2RldGFpbCZhY3Rpb249Y2xpY2tSZWRpcmVjdCZkb05vdExvZ0NsaWNrPXRydWU=
https://www.amazon.in/First-Course-Probability-Sheldon-Ross/dp/9353065607/ref=pd_rhf_dp_s_ci_mcx_mr_hp_d_1/258-7423128-6325812?pd_rd_w=PDmEn&pf_rd_p=1849d6da-d38e-465f-ab9e-0b31b1d1949e&pf_rd_r=6JQSKASEM5TKNJ6YHHF7&pd_rd_r=ea9f3f18-4e95-4737-8979-e2ecb10c2e64&pd_rd_wg=cIi9s&pd_rd_i=9353065607&psc=1
https://www.amazon.in/Colgate-Strong-Anticavity-Toothpaste-Shakti/dp/B082LDRTD1/ref=sr_1_1_sspa?dchild=1&keywords=colgate&qid=1624272361&smid=AT95IG9ONZD7S&sr=8-1-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUFQN1hSTENHVDMzM0QmZW5jcnlwdGVkSWQ9QTAzMzM4NzBWTzBUM1BSRzRCRVMmZW5jcnlwdGVkQWRJZD1BMDk3OTIzNjEySzFLS080TVJZWCZ3aWRnZXROYW1lPXNwX2F0ZiZhY3Rpb249Y2xpY2tSZWRpcmVjdCZkb05vdExvZ0NsaWNrPXRydWU=
https://www.amazon.in/Colgate-Max-Fresh-Spicy-Toothpaste/dp/B01NAZBI08/ref=sr_1_7?dchild=1&keywords=colgate&qid=1624272361&smid=AT95IG9ONZD7S&sr=8-7
https://www.amazon.in/Surf-Excel-Easy-Detergent-Powder/dp/B00TS8ABHC/ref=sr_1_1_sspa?dchild=1&keywords=Tide&qid=1624275641&smid=AT95IG9ONZD7S&sr=8-1-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUE0STVYU0w4WE1aRk8mZW5jcnlwdGVkSWQ9QTAyODkxOTZUWUpXQ1kwTFBLRkwmZW5jcnlwdGVkQWRJZD1BMTAyNzg1MFUxRzI1UVcyTkUwVCZ3aWRnZXROYW1lPXNwX2F0ZiZhY3Rpb249Y2xpY2tSZWRpcmVjdCZkb05vdExvZ0NsaWNrPXRydWU=
https://www.amazon.in/Pears-Soft-Fresh-Bathing-Pack/dp/B06WWR7W3V/ref=sr_1_1_sspa?dchild=1&keywords=soap&qid=1624275857&sr=8-1-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUFLREZVRlc2WlYyT1YmZW5jcnlwdGVkSWQ9QTA3Mjk3MzYxTEcxM0FCRkJLVVBPJmVuY3J5cHRlZEFkSWQ9QTAzMDMzNzZBSlNYWkRIUkI2Wjkmd2lkZ2V0TmFtZT1zcF9hdGYmYWN0aW9uPWNsaWNrUmVkaXJlY3QmZG9Ob3RMb2dDbGljaz10cnVl
https://www.amazon.in/gp/slredirect/picassoRedirect.html/ref=pa_sp_atf_aps_sr_pg1_1?ie=UTF8&adId=A0259195DZJ2S7GUU09J&url=%2FVaseline-Body-Ice-Cream-165%2Fdp%2FB085WKL537%2Fref%3Dsr_1_1_sspa%3Fdchild%3D1%26keywords%3DBody%2BCream%26qid%3D1624283239%26sr%3D8-1-spons%26psc%3D1&qualifier=1624283239&id=8919141745039535&widgetName=sp_atf

'''