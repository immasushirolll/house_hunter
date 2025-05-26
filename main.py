from address_parser import AddressParser
import json
import requests
from notion_client import Client
from write_to_notion import create_notion_entry
from get_page import get_pages

NOTION_TOKEN = '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'
DATABASE_ID = '1e8ccd11787580e1a575c6ade25b0efd'

def main():
    url = "https://offcampus.uwo.ca/Listings/"
    num_pages = get_pages(url)
    create_notion_entry(num_pages)

if __name__ == "__main__":
    main()