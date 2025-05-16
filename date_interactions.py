# from utils import import_utils
import requests
from html.parser import HTMLParser
import json
from date_parser import DateParser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
# import_utils()

def start_driver(url: str = "https://offcampus.uwo.ca/Listings"):
    # Set up Chrome (headless optional)
    options = Options()
    options.add_argument("--headless")  # Remove this if you want to see the browser
    driver = webdriver.Chrome(options=options)

    # Go to the listings page
    driver.get(url)

    time.sleep(2)  # Wait for page to load
    return driver

def get_page_data(url: str, page_num: int, posting_date_flag: bool = True, housing_type_flag: bool = True, bedroom_count_flag: bool = True, location_flag: bool = True):
    driver = start_driver()

    # Posting Date: 1
    if posting_date_flag:
        target_posting_date_options = {'1'}  # Last 14 Days
        housing_select = driver.find_element(By.ID, "Posted")
        housing_options = housing_select.find_elements(By.TAG_NAME, 'option')
        for option in housing_options:
            if option.get_attribute("value") in target_posting_date_options:
                driver.execute_script("arguments[0].selected = true;", option)
        driver.find_element(By.CSS_SELECTOR, "form.search_listings_form").submit()
        time.sleep(3)  # Wait for filtered results to load
    
    if housing_type_flag:
        # Housing Type options: 1, 2, 6, 7, 13, 11, 12
        target_housing_options = {'1', '6', '7', '11', '13'}  # House, Apartment, Townhouse, etc.
        housing_select = driver.find_element(By.ID, "SelectedHousing")
        housing_options = housing_select.find_elements(By.TAG_NAME, 'option')
        for option in housing_options:
            if option.get_attribute("value") in target_housing_options:
                driver.execute_script("arguments[0].selected = true;", option)
        driver.find_element(By.CSS_SELECTOR, "form.search_listings_form").submit()
        time.sleep(3)  # Wait for filtered results to load

    if bedroom_count_flag:
        # Number of Bedrooms options: 1 through 7
        target_bedroom_options = {'1', '2', '3'}    # 0, 1, 2 bedrooms
        bedroom_select = driver.find_element(By.ID, "NumberOfBedrooms")
        bedroom_options = bedroom_select.find_elements(By.TAG_NAME, 'option')
        for option in bedroom_options:
            if option.get_attribute("value") in target_bedroom_options:
                driver.execute_script("arguments[0].selected = true;", option)
        driver.find_element(By.CSS_SELECTOR, "form.search_listings_form").submit()
        time.sleep(3)

    if location_flag:
        # Mapping location names to option values from the HTML
        target_location_values = {"1", "3", "4", '5', '6', '7', '12', '14', '13', '16'}  # Downtown, Masonville, North London

        # Get the location <select> element
        location_select = driver.find_element(By.ID, "SelectedLocations")
        location_options = location_select.find_elements(By.TAG_NAME, "option")

        # Select the desired locations
        for option in location_options:
            if option.get_attribute("value") in target_location_values:
                driver.execute_script("arguments[0].selected = true;", option)

        # Submit the form (simulate user interaction)
        driver.find_element(By.CSS_SELECTOR, "form.search_listings_form").submit()

        time.sleep(3)  # Wait for filtered results to load

    html = driver.page_source
    with open(f"raw_output/filtered_page_{page_num}.html", "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"Saved filtered page {page_num}")


# -------- Paginate and Save HTML --------
def next_page(driver: webdriver.Chrome, page_number: int):
    for page in range(1, 6):  # Pages 1 to 5
        # Simulate JavaScript GoToPage(n)
        driver.execute_script(f"GoToPage({page})")
        time.sleep(2)  # Allow page to update

        html = driver.page_source
        with open(f"raw_output/filtered_page_{page}.html", "w", encoding="utf-8") as f:
            f.write(html)

        print(f"Saved filtered page {page}")

    driver.quit()

# -------------------------------------------
# from utils import import_utils
from interactions import start_driver, get_page_data, next_page
from address_parser import AddressParser
from date_parser import DateParser
import json
# import_utils()

url = "https://offcampus.uwo.ca/Listings/"
# url = "https://offcampus.uwo.ca/Listings/Details/59146/"

# get 1st page of the data
page_num = 1
# get_page_data(url, page_num)

# instead of getting the per page response, we will read the response from the local saved files instead
page_content = ""
parser = AddressParser()
# date_parser = DateParser()



# # get the first page to extract some info first
# with open(f"raw_output/filtered_page_{page_num}.html", "r", encoding="utf-8") as f:
#   page_content = f.read()

# date_parser.feed(page_content)


# # for page_num in range(1, 3):
# #   # print(page_num)
# #   with open(f"raw_output/filtered_page_{page_num}.html", "r", encoding="utf-8") as f:
# #     page_content = f.read()

# json_output = json.dumps(date_parser.listings, indent=4)
# print(json_output)
  
#   # print(page_content)
# # with open("output.html", "w") as f:   # write for debugging
# #   f.write(page_content)
# #   print('written successfully to output.html')


# # # with open("output.html", "r") as f:
# # #     html_content = f.read()



# # with open("cleaned_output.json", "r") as f: # read for debugging
# #     print(f.read())

