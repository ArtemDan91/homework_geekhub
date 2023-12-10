# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import csv
import logging
from pathlib import Path

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class GoogleChromeExtensionsPipeline:
    RESULTS_DIRECTORY = Path(Path.cwd(), 'results')
    CSV_FILE_PATH = Path(RESULTS_DIRECTORY, 'extensions.csv')

    def open_spider(self, spider):
        self.RESULTS_DIRECTORY.mkdir(parents=True, exist_ok=True)

        if not self.CSV_FILE_PATH.exists():
            with open(self.CSV_FILE_PATH, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['extension_id', 'location', 'short_description', 'title']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()

    def process_item(self, item, spider):
        try:
            with open(self.CSV_FILE_PATH, 'a', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['extension_id', 'location', 'short_description', 'title']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writerow({
                    'extension_id': item['extension_id'],
                    'location': item['location'],
                    'short_description': item['short_description'],
                    'title': item['title'],
                })
        except FileNotFoundError as e:
            spider.log(f"CSV file not found: {e}", logging.ERROR)
        except Exception as e:
            spider.log(f"Error writing to CSV file: {e}", logging.ERROR)
        
        spider.log(f"{item['title']}", logging.INFO)
        return item


