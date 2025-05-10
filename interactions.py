from utils import import_utils
import_utils()

def start_driver(url: str = "https://offcampus.uwo.ca/Listings"):
    # Set up Chrome (headless optional)
    options = Options()
    options.add_argument("--headless")  # Remove this if you want to see the browser
    driver = webdriver.Chrome(options=options)

    # Go to the listings page
    driver.get(url)

    time.sleep(2)  # Wait for page to load
    return driver

def apply_filters(posting_date_flag: bool = True, housing_type_flag: bool = True, bedroom_count_flag: bool = True, location_flag: bool = True):
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