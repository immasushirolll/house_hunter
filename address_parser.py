from html.parser import HTMLParser
import json
from html.parser import HTMLParser

class AddressParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset_flags()
        self.listings = []

    def reset_flags(self):
        self.in_listing = False
        self.in_Address = False
        self.in_Location = False
        self.in_rent = False
        self.in_availability = False
        self.in_Description = False
        self.current = {}

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)

        if tag == "div" and attrs.get("class") == "rental-listing":
            self.in_listing = True
            self.current = {}

        if not self.in_listing:
            return

        if tag == "a" and attrs.get("href", "").startswith("/Listings/Details"):
            if "background-image" in attrs.get("style", ""):
                pass
            else:
                self.in_Address = True
                self.current["ID"] = str(attrs["href"]).split("/")[-1]
                self.current["URL"] = "https://offcampus.uwo.ca" + str(attrs["href"])

        if tag == "a" and attrs.get("class") == "location_map_link":
            self.in_Location = True

        if tag == "h3":
            self.in_rent = True

        if tag == "h4":
            self.in_availability = True

        if tag == "p":
            self.in_Description = True

    def handle_endtag(self, tag):
        if tag == "div" and self.in_listing:
            for field in ["ID", "URL", "Address", "Location", "Price", "Available", "Description"]:
                self.current.setdefault(field, "")

            self.listings.append(self.current)
            self.reset_flags()

        # reset parsing state
        self.in_Address = False
        self.in_Location = False
        self.in_rent = False
        self.in_availability = False
        self.in_Description = False

    def handle_data(self, data):
        if not self.in_listing:
            return

        data = data.strip()
        if not data:
            return

        if self.in_Address:
            self.current["Address"] = data
        elif self.in_Location:
            self.current["Location"] = data
        elif self.in_rent:
            self.current["Price"] = data
        elif self.in_availability:
            self.current["Available"] = data
        elif self.in_Description:
            self.current["Description"] = self.current.get("Description", "") + data + " "