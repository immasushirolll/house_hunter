from address_parser import AddressParser
import json
import requests
from notion_client import Client
from notion_actions import create_notion_entry
from get_page import get_pages


def main():
    url = "https://offcampus.uwo.ca/listings/"
    num_pages = get_pages(url)
    create_notion_entry(num_pages)

if __name__ == "__main__":
    main()