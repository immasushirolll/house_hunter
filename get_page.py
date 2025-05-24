import requests
from datetime import date
from interactions import listings_form, next_page
import re
from html.parser import HTMLParser
import json
from address_parser import AddressParser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from utils import *

def get_pages():
    url = "https://offcampus.uwo.ca/Listings/"

    # start driver
    page_num = 1
    options = Options()
    options.add_argument("--headless")  # Remove this if you want to see the browser
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(1)  # Wait for page to load

    try:
        driver = listings_form(driver, {'0'}, "Posted")
        driver = listings_form(driver, {'1', '6', '7', '11', '13'}, "SelectedHousing")
        driver = listings_form(driver, {'3'}, "NumberOfBedrooms")
        driver = listings_form(driver, {"1", "3", "4", '5', '6', '7', '12', '14', '13', '16'}, "SelectedLocations")
    except:
        print("Error in filtering options")
        driver.quit()

    html = driver.page_source
    with open(f"raw_output/filtered_page_{page_num}.html", "w", encoding="utf-8") as f:
        f.write(html)
        print(f'Saved filtered page {page_num}')

    total_pages = int(driver.find_element(By.CSS_SELECTOR, "input.total_pages").get_attribute("value"))
    print('Num pages', total_pages)
    today = date.today()
    print("Today's date:", today)

    # for number of results, get the next page
    driver = next_page(driver, total_pages)
    
    # ------ Now we clean the html and get the data ------
    # instead of getting the per page response, we will read the response from the local saved files instead
    page_content = ""
    parser = AddressParser()

    for page_num in range(1, total_pages+1):
        with open(f"raw_output/filtered_page_{page_num}.html", "r", encoding="utf-8") as f:
            page_content = f.read()
            parser.feed(page_content)
            json_output = json.dumps(parser.listings, indent=4)
            json_output = json_output.replace("{},", "")
            # json_ouput = json.dumps(json_output_str, indent=4)
            with open(f"cleaned_output/cleaned_output_{page_num}.json", "w") as f:
                f.write(json_output)
                print(f'written successfully to cleaned_output/cleaned_output_{page_num}.html')
    
    return total_pages

# get_pages()