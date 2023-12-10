import scrapy
import sys
from pathlib import Path
from scrapy import Request
from scrapy.http import Response
from urllib.parse import urljoin

parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from items import GoogleChromeExtensionsItem
from parsers.extentions_parser.parser import ChromeExtensionsParser


class ChromeExtensionsSpider(scrapy.Spider):
    parser = ChromeExtensionsParser()
    name = 'chrome_extensions'
    start_urls = [urljoin(parser.BASE_URL, 'webstore/sitemap')]

    def parse(self, response, **kwargs):
        try:
            results = self.parser.parse_sitemap(response.text)
            for result in results:
                yield Request(
                    url=result.location,
                    callback=self.parse_location,
                )
        except Exception as e:
            self.logger.error(f"Error in parse method: {e}")

    def parse_location(self, response: Response, **kwargs):
        try:
            results = self.parser.parse_location(response.text)
            for result in results:
                yield Request(
                    url=result.location,
                    callback=self.parse_extension,
                )
                self.logger.info(f"Requested URL: {result.location}")
        except Exception as e:
            self.logger.error(f"Error in parse_location method: {e}")

    def parse_extension(self, response: Response):
        try:
            result = self.parser.parse_extension(response.text)
            print("Item:", result)

            self.logger.info(f"Requested URL: {result.location}")

            item = GoogleChromeExtensionsItem(
                extension_id=result.extension_id,
                location=result.location,
                short_description=result.short_description,
                title=result.title
            )
            self.logger.info(f"Item: {item}")
            return item
        except Exception as e:
            self.logger.error(f"Error in parse_extension method: {e}")
