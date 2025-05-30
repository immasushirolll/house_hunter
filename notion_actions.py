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
                        "ID": {
                            "title": [
                                {
                                    "text": {
                                        "content": listing.get("ID", "")
                                    }
                                }
                            ]
                        },
                        "URL": {
                            "url": listing.get("URL", "")
                        },
                        "Address": {
                            "rich_text": [
                                {
                                    "text": {
                                        "content": listing.get("Address", "")
                                    }
                                }
                            ]
                        },
                        "Location": {
                            "select": {
                                "name": listing.get("Location", "")
                            }
                        },
                        "Price": {
                            "rich_text": [
                                {
                                    "text": {
                                        "content": listing.get("Price", "")
                                    }
                                }
                            ]
                        },
                        "Available": {
                            "rich_text": [
                                {
                                    "text": {
                                        "content": listing.get("Available", "")
                                    }
                                }
                            ]
                        },
                        "Description": {
                            "rich_text": [
                                {
                                    "text": {
                                        "content": listing.get("Description", "")[:2000]  # text limit
                                    }
                                }
                            ]
                        },
                        "Date": {
                            "date": 
                                {
                                    "start": listing.get("Timestamp", "")
                                }
                            
                        }
                    }
                )
            except Exception as e:
                print(f"{listing.get("URL", "")} failed with error: {e}")

def delete_all_entries():
    notion = Client(auth=NOTION_TOKEN)

    notion.pages.update(
        page_id="1e8ccd117875800aa865000c4e4cffdd",  # NOT the database_id, but the parent page that holds the database
        archived=True
    )

    new_db = notion.databases.create(
                parent={"type": "page_id", "page_id": "1e8ccd117875800aa865000c4e4cffdd"},
                title=[{"type": "text", "text": {"content": "My New Database"}}],
                properties={
                        "ID": {
                            "title": [
                                {}
                            ]
                        },
                        "URL": {
                            "url": {}
                        },
                        "Address": {
                            "rich_text": {}
                        },
                        "Location": {
                            "select": {}
                        },
                        "Price": {
                            "rich_text": [
                                {}
                            ]
                        },
                        "Available": {
                            "rich_text": [
                                {}
                            ]
                        },
                        "Description": {
                            "rich_text": [
                                {}
                            ]
                        },
                        "Date": {
                            "date": {}
                    }
                }
            )


def drop_duplicates():
    notion = Client(auth=NOTION_TOKEN)
    results = notion.databases.query(database_id=DATABASE_ID)

    seen_urls = set()
    start_cursor = None

    while True:
        response = notion.databases.query(
            database_id=DATABASE_ID,
            start_cursor=start_cursor
        )
        pages = response.get("results", [])

        for page in pages:
            props = page["properties"]
            page_id = page["id"]

            ID = props.get("URL", {}).get("url")

            if url in seen_urls:
                # Duplicate detected, archive this page
                notion.pages.update(page_id=page_id, archived=True)
                print(f"Archived duplicate: {url}")
            else:
                seen_urls.add(url)

        if response.get("has_more"):
            start_cursor = response["next_cursor"]
        else:
            break

delete_all_entries()