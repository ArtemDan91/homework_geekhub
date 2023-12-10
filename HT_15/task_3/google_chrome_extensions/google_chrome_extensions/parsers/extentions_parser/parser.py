import logging
import sys
import warnings
from bs4 import BeautifulSoup, XMLParsedAsHTMLWarning
from pathlib import Path

parent_dir = Path(__file__).parent
sys.path.insert(0, str(parent_dir))

from datacls import ExtensionInfo
from datacls import LocationItem
from datacls import SitemapItem

warnings.filterwarnings(action='ignore', category=XMLParsedAsHTMLWarning)


class ChromeExtensionsParser:
    BASE_URL = 'https://chrome.google.com'

    def parse_sitemap(self, response_text):
        try:
            soup = BeautifulSoup(response_text, 'lxml')
            return [
                SitemapItem(
                    location=location.loc.text
                )
                for location in soup.select('sitemap')
            ]
        except Exception as e:
            logging.error(f"Error in parse_sitemap: {e}")
            
    def parse_location(self, response_text):
        try:
            soup = BeautifulSoup(response_text, 'lxml')
            return [
                LocationItem(
                    location=location.find('loc').text,
                )
                for location in soup.select('url')
            ]
        except Exception as e:
            logging.error(f"Error in parse_location: {e}")

    def parse_extension(self, response_text):
        try:
            soup = BeautifulSoup(response_text, 'lxml')

            return ExtensionInfo(
                extension_id=
                soup.find('meta', {'property': 'og:url'}).get('content').split('/')[-1],
                location=soup.find('meta', {'property': 'og:url'}).get('content'),
                short_description=soup.find('meta', {'property': 'og:description'}).get('content').strip().replace('\n', ''),
                title=soup.find('meta', {'property': 'og:title'}).get('content'),
            )
        except Exception as e:
            logging.error(f"Error in parse_extension: {e}")