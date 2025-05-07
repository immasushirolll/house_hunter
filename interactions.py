# THIS FINALLY WORKED OMG FINALLY YES
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

# Set up Chrome (headless optional)
options = Options()
options.add_argument("--headless")  # Remove this if you want to see the browser
driver = webdriver.Chrome(options=options)

# Go to the listings page
driver.get("https://offcampus.uwo.ca/Listings")

time.sleep(2)  # Wait for page to load

# -------- Apply Filters --------
# Number of Bedrooms options: 1 through 7
target_bedroom_options = {'1', '2', '3'}    # 0, 1, 2 bedrooms
bedroom_select = driver.find_element(By.ID, "NumberOfBedrooms")
bedroom_options = bedroom_select.find_elements(By.TAG_NAME, 'option')
for option in bedroom_options:
    if option.get_attribute("value") in target_bedroom_options:
        driver.execute_script("arguments[0].selected = true;", option)
driver.find_element(By.CSS_SELECTOR, "form.search_listings_form").submit()
time.sleep(3)


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

# -------- Paginate and Save HTML --------

for page in range(1, 6):  # Pages 1 to 5
    # Simulate JavaScript GoToPage(n)
    driver.execute_script(f"GoToPage({page})")
    time.sleep(2)  # Allow page to update

    html = driver.page_source
    with open(f"raw_output/filtered_page_{page}.html", "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Saved filtered page {page}")

driver.quit()