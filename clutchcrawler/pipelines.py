from scrapy.exceptions import DropItem

class DuplicatesPipeline:
    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        # Check for duplicates based on the company title or link
        if item['title'] in self.ids_seen:
            raise DropItem(f"Duplicate item found: {item['title']}")
        else:
            self.ids_seen.add(item['title'])
            return item
