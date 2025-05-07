from html.parser import HTMLParser

class AddressParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset_flags()
        self.listings = []

    def reset_flags(self):
        self.in_listing = False
        self.in_address = False
        self.in_location = False
        self.in_rent = False
        self.in_availability = False
        self.in_description = False
        self.current = {}

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)

        # Start a new listing
        if tag == "div" and attrs.get("class") == "rental-listing":
            self.in_listing = True
            self.current = {}

        if not self.in_listing:
            return

        # Address link
        if tag == "a" and attrs.get("href", "").startswith("/Listings/Details"):
            if "background-image" in attrs.get("style", ""):
                self.current["image_url"] = attrs["style"].split("url(")[1].split(")")[0]
            else:
                self.in_address = True
                self.current["listing_url"] = "https://offcampus.uwo.ca" + str(attrs["href"])

        # Location
        if tag == "a" and attrs.get("class") == "location_map_link":
            self.in_location = True

        # Rent
        if tag == "h3":
            self.in_rent = True

        # Availability
        if tag == "h4":
            self.in_availability = True

        # Description
        if tag == "p":
            self.in_description = True

    def handle_endtag(self, tag):
        if tag == "div" and self.in_listing:
            # End of listing block
            self.in_listing = False
            self.listings.append(self.current)
            self.reset_flags()

        self.in_address = False
        self.in_location = False
        self.in_rent = False
        self.in_availability = False
        self.in_description = False

    def handle_data(self, data):
        if not self.in_listing:
            return

        data = data.strip()
        if not data:
            return

        if self.in_address:
            self.current["address"] = data
        elif self.in_location:
            self.current["location"] = data
        elif self.in_rent:
            self.current["rent_info"] = data
        elif self.in_availability:
            self.current["available"] = data
        elif self.in_description:
            self.current["description"] = self.current.get("description", "") + data + " "