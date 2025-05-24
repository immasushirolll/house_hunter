from address_parser import AddressParser
import json
import requests
from notion_client import Client
from get_page import get_pages

NOTION_TOKEN = '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'
DATABASE_ID = '1e8ccd11787580e1a575c6ade25b0efd'

def create_notion_entry(total_pages):
    notion = Client(auth=NOTION_TOKEN)

    for i in range(total_pages):
        with open(f'cleaned_output/cleaned_output_{i+1}.json', 'r') as f:
            data = json.load(f)

        for listing in data:
            try:
                notion.pages.create(
                    parent={"database_id": DATABASE_ID},
                    properties={
                        "URL": {
                            "title": [
                                {
                                    "text": {
                                        "content": listing["URL"]
                                    }
                                }
                            ]
                        },
                        "Address": {
                            "rich_text": [
                                {
                                    "text": {
                                        "content": listing["Address"]
                                    }
                                }
                            ]
                        },
                        "Location": {
                            "rich_text": [
                                {
                                    "text": {
                                        "content": listing["Location"]
                                    }
                                }
                            ]
                        },
                        "Price": {
                            "rich_text": [
                                {
                                    "text": {
                                        "content": listing["Price"]
                                    }
                                }
                            ]
                        },
                        "Available": {
                            "rich_text": [
                                {
                                    "text": {
                                        "content": listing["Available"]
                                    }
                                }
                            ]
                        },
                        "Description": {
                            "rich_text": [
                                {
                                    "text": {
                                        "content": listing["Description"]
                                    }
                                }
                            ]
                        }
                    }
                )
            except Exception as e:
                print(f"{listing['URL']} failed")

create_notion_entry(4)
