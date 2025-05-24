import requests
import re
from html.parser import HTMLParser
import json
from address_parser import AddressParser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

def listings_form(driver: webdriver, options: dict, id_name: str):
    select = driver.find_element(By.ID, id_name)
    found_options = select.find_elements(By.TAG_NAME, 'option')
    for option in found_options:
        if option.get_attribute("value") in options:
            driver.execute_script("arguments[0].selected = true;", option)
    driver.find_element(By.CSS_SELECTOR, "form.search_listings_form").submit()
    time.sleep(2)  # Wait for filtered results to load
    # print(driver)
    return driver

# -------- Paginate and Save HTML --------
def next_page(driver: webdriver, page_number: int):
    for page in range(2, page_number+1):  # Pages 1 to 5
        # Simulate JavaScript GoToPage(n)
        driver.execute_script(f"GoToPage({page})")
        time.sleep(2)

        html = driver.page_source
        with open(f"raw_output/filtered_page_{page}.html", "w", encoding="utf-8") as f:
            f.write(html)

        print(f"Saved filtered page {page}")

    return driver