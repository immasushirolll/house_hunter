import requests
import re
from html.parser import HTMLParser
import json
from address_parser import AddressParser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

def get_page():
    url = "https://offcampus.uwo.ca/Listings/"

    # get 1st page of the raw data
    page_num = 1
    options = Options()
    options.add_argument("--headless")  # Remove this if you want to see the browser
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(2)  # Wait for page to load

    # Step 3: Locate the parent <div> by ID
    sub_search = driver.find_element(By.ID, "sub-search")
    # Step 4: Get the full text inside the parent div
    full_text = sub_search.text.strip()
    print(full_text)
    lines = full_text.split("\n")
    if len(lines) > 1:
        search_summary = lines[0]
        print("Search Summary:", search_summary)
        match = re.search(r'(Search results: .*?\)) as of (.+)', search_summary)
        if match:
            results_text = match.group(1)
            date_text = match.group(2)
            print("Results:", results_text)
            print("Date:", date_text)

    # Posting Date: 1
    target_posting_date_options = {'1'}  # Last 14 Days
    housing_select = driver.find_element(By.ID, "Posted")
    housing_options = housing_select.find_elements(By.TAG_NAME, 'option')
    for option in housing_options:
        if option.get_attribute("value") in target_posting_date_options:
            driver.execute_script("arguments[0].selected = true;", option)
    driver.find_element(By.CSS_SELECTOR, "form.search_listings_form").submit()
    time.sleep(2)  # Wait for filtered results to load

    # Housing Type options: 1, 2, 6, 7, 13, 11, 12
    target_housing_options = {'1', '6', '7', '11', '13'}  # House, Apartment, Townhouse, etc.
    housing_select = driver.find_element(By.ID, "SelectedHousing")
    housing_options = housing_select.find_elements(By.TAG_NAME, 'option')
    for option in housing_options:
        if option.get_attribute("value") in target_housing_options:
            driver.execute_script("arguments[0].selected = true;", option)
    driver.find_element(By.CSS_SELECTOR, "form.search_listings_form").submit()
    time.sleep(2)  # Wait for filtered results to load

    # Bedroom Count options: 1, 2, 3, 4, 5, 6
    target_bedroom_count_options = {'1', '2', '3', '4', '5', '6'}  # 1 Bedroom, 2 Bedroom, etc.
    bedroom_count_select = driver.find_element(By.ID, "SelectedBedroom")
    bedroom_count_options = bedroom_count_select.find_elements(By.TAG_NAME, 'option')
    for option in bedroom_count_options:
        if option.get_attribute("value") in target_bedroom_count_options:
            driver.execute_script("arguments[0].selected = true;", option)
    driver.find_element(By.CSS_SELECTOR, "form.search_listings_form").submit()
    time.sleep(2)  # Wait for filtered results to load

    # Location options: 1, 2, 3, 4, 5, 6
    target_location_options = {'1', '2', '3', '4', '5', '6'}  # London, Ontario
    location_select = driver.find_element(By.ID, "SelectedLocation")
    location_options = location_select.find_elements(By.TAG_NAME, 'option')
    for option in location_options:
        if option.get_attribute("value") in target_location_options:
            driver.execute_script("arguments[0].selected = true;", option)
    driver.find_element(By.CSS_SELECTOR, "form.search_listings_form").submit()
    time.sleep(2)  # Wait for filtered results to load

    html = driver.page_source
    with open(f"raw_output/filtered_page_{page_num}.html", "w", encoding="utf-8") as f:
        f.write(html)
        print('written successfully to raw_output/filtered_page_1.html')

    num_pages, date = get_page_data(url, page_num)

    # instead of getting the per page response, we will read the response from the local saved files instead
    page_content = ""
    parser = AddressParser()

    # get the first page to extract some info first
    with open(f"raw_output/filtered_page_{page_num}.html", "r", encoding="utf-8") as f:
        page_content = f.read()

    parser.feed(page_content)
    items_and_date = parser.listings[0]["description"]
    print(items_and_date)
    print(num_pages, date)

    # for page_num in range(1, 3):
    #     # print(page_num)
    #     with open(f"raw_output/filtered_page_{page_num}.html", "r", encoding="utf-8") as f:
    #         page_content = f.read()

    json_output = json.dumps(parser.listings, indent=4)
    # print(json_output)

    # with open("output.html", "w") as f:   # write for debugging
    #     f.write(page_content)
    #     print('written successfully to output.html')

    # # with open("output.html", "r") as f:
    # #     html_content = f.read()

    # # parser = AddressParser()
    # parser.feed(page_content)

    # json_output = json.dumps(parser.listings, indent=4)
    # print(json_output)

    # with open("cleaned_output.json", "w") as f:
    #     f.write(json_output)

    # with open("cleaned_output.json", "r") as f: # read for debugging
    #     print(f.read())
