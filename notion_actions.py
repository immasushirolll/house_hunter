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
                        "ScanDate": {
                            "date": 
                                {
                                    "start": listing.get("Timestamp", "")
                                }
                            
                        }
                    }
                )
            except Exception as e:
                with open("failed_pages.txt", "a") as error_file:
                    error_file.write(f"{listing} failed with error: {e}\n\n")

# notion = Client(auth=NOTION_TOKEN)

# # Replace with the page where you want to create the database
# parent_page_id = "1e8ccd1178758003b76eeb02b7f3d73b"

# # Create a new database
# new_database = notion.databases.create(
#     parent={"type": "page_id", "page_id": parent_page_id},
#     title=[{
#         "type": "text",
#         "text": {"content": "House Hunter"}
#     }],
#     properties={
#         "ID": {
#             "title": [
#                 {
#                     "text": {}
#                 }
#             ]
#         },
#         "URL": {
#             "url": ''
#         },
#         "Address": {
#             "rich_text": [
#                 {
#                     "text": {
#                         "content": ''
#                     }
#                 }
#             ]
#         },
#         "Location": {
#             "select": {
#                 "name": ''}
#         },
#         "Price": {
#             "rich_text": [
#                 {
#                     "text": {}
#                 }
#             ]
#         },
#         "Available": {
#             "rich_text": [
#                 {
#                     "text": {}
#                 }
#             ]
#         },
#         "Description": {
#             "rich_text": [
#                 {
#                     "text": {}
#                 }
#             ]
#         },
#         "ScanDate": {
#             "date": 
#                 {}
            
#         }
#     }
# )

# print(f"Created database: {new_database['id']}")


# def drop_duplicates():
#     notion = Client(auth=NOTION_TOKEN)
#     results = notion.databases.query(database_id=DATABASE_ID)

#     seen_urls = set()
#     start_cursor = None

#     while True:
#         response = notion.databases.query(
#             database_id=DATABASE_ID,
#             start_cursor=start_cursor
#         )
#         pages = response.get("results", [])

#         for page in pages:
#             props = page["properties"]
#             page_id = page["id"]

#             ID = props.get("URL", {}).get("url")

#             if url in seen_urls:
#                 # Duplicate detected, archive this page
#                 notion.pages.update(page_id=page_id, archived=True)
#                 print(f"Archived duplicate: {url}")
#             else:
#                 seen_urls.add(url)

#         if response.get("has_more"):
#             start_cursor = response["next_cursor"]
#         else:
#             break