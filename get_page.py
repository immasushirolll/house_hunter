import utils

# Save or process pages using your AddressParser

url = "https://offcampus.uwo.ca/Listings/"
# url = "https://offcampus.uwo.ca/Listings/Details/59146/"

response = requests.post(url=url, data={'PageNumber':'2'})

# Check if the request was successful
if response.status_code != 200:
    raise Exception(f"Failed to retrieve a response from web, may be server issue or incorrect url. Status code: {response.status_code}")

page_content = response.text
with open("output.html", "w") as f:   # write for debugging
  f.write(page_content)
  print('written successfully to output.html')


# with open("output.html", "r") as f:
#     html_content = f.read()

parser = AddressParser()
parser.feed(page_content)

json_output = json.dumps(parser.listings, indent=4)

with open("cleaned_output.json", "w") as f:
  f.write(json_output)

# with open("cleaned_output.json", "r") as f: # read for debugging
#     print(f.read())

