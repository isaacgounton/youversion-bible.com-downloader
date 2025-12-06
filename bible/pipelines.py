import json
import os


class BiblePipeline(object):

    def __init__(self):
        self.file = None

    def open_spider(self, spider):
        # Get the directory where this file is located (bible/)
        base_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(base_dir, 'data')
        
        # Ensure data directory exists
        os.makedirs(data_dir, exist_ok=True)
        
        output_path = os.path.join(data_dir, 'spider.bible_id.json')
        self.file = open(output_path, 'w', encoding='utf-8')

    def close_spider(self, spider):
        if self.file:
            self.file.close()

    def process_item(self, item, spider):
        # Write the item as JSON
        json.dump(item, self.file, ensure_ascii=False, indent=2)
        return item
