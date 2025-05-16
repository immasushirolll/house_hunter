from html.parser import HTMLParser

class DateParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset_flags()
        self.listings = []

    def reset_flags(self):
        self.in_listing = False
        self.items_and_date = False
        self.current = {}

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)

        # Start a new object (1 per page)
        if tag == "div" and attrs.get("id") == "sub-search":
            self.in_listing = True
            self.current = {}

        if not self.in_listing:
            return

        # Start a new items_and_date for that data object
        if tag == "p" and attrs.get("class") == "item_count":
            self.items_and_date = True

    def handle_endtag(self, tag):
        if tag == "div" and self.in_listing:
            # End of listing block
            self.in_listing = False
            self.listings.append(self.current)
            self.reset_flags()

        self.items_and_date = False

    def handle_data(self, data):
        if not self.in_listing:
            return

        data = data.strip()
        if not data:
            return

        if self.items_and_date:
            self.current["items and date"] = data