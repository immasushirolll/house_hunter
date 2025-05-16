from interactions import start_driver, get_page_data, next_page
from address_parser import AddressParser
import json

url = "https://offcampus.uwo.ca/Listings/"

# get 1st page of the raw data
page_num = 1
get_page_data(url, page_num)

# instead of getting the per page response, we will read the response from the local saved files instead
page_content = ""
parser = AddressParser()

# get the first page to extract some info first
page_num = 1
with open(f"raw_output/filtered_page_{page_num}.html", "r", encoding="utf-8") as f:
  page_content = f.read()

parser.feed(page_content)

# for page_num in range(1, 3):
#   # print(page_num)
#   with open(f"raw_output/filtered_page_{page_num}.html", "r", encoding="utf-8") as f:
#     page_content = f.read()

json_output = json.dumps(parser.listings, indent=4)
print(json_output)
  
  # print(page_content)
# with open("output.html", "w") as f:   # write for debugging
#   f.write(page_content)
#   print('written successfully to output.html')


# # with open("output.html", "r") as f:
# #     html_content = f.read()


# # parser = AddressParser()
# parser.feed(page_content)

# json_output = json.dumps(parser.listings, indent=4)
# print(json_output)

# with open("cleaned_output.json", "w") as f:
#   f.write(json_output)

# with open("cleaned_output.json", "r") as f: # read for debugging
#     print(f.read())

