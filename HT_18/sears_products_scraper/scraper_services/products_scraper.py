import logging
import random
import sys
import time
from pathlib import Path

import requests
from requests import RequestException
from urllib.parse import urljoin

logging.basicConfig(level=logging.INFO)


def scrape_product_data(product_id, headers, cookies):
    try:
        response = requests.get(
            f'https://www.sears.com/api/sal/v3/products/details/{product_id}?storeName=Sears&memberStatus=G&zipCode=10101',
            headers=headers,
            cookies=cookies,
        )
        if response.status_code == 200:
            product_data_json = \
            response.json()['productDetail']['softhardProductdetails'][0]

            return {
                'product_description_name': product_data_json[
                    'descriptionName'],
                'sell_price': product_data_json['price']['finalPriceDisplay'],
                'product_id': product_data_json['identity']['sSin'],
                'short_description': product_data_json['seoDesc'],
                'brand_name': product_data_json['brandName'],
                'category_name':
                    product_data_json['hierarchies']['specificHierarchy'][0][
                        'name'],
                'url': urljoin('https://www.sears.com',
                               product_data_json['seoUrl']),
            }

    except RequestException as e:
        raise RequestException(f"Error during HTTP request: {e}")


headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Content-Type': 'application/json',
    'Authorization': 'SEARS',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
}

cookies = {
    'forterToken': '4c74ca22d2204b00a5a8977c84fd9bd9_1703618055452_520_UDF43_13ck',
    'cf_clearance': 'fjBhn7b4puIJmD6zsORitqD8eFHhsak3vrPG4sUUNUA-1703618021-0-2-8d27329b.7c5ea2f5.54dfe7d4-0.2.1703618021',
    'irp': '960ebf5f-fd56-453a-aeb5-11204e22ed94|6CYQf8MYyvClOg1kIrN2VwfikdNMFFRIfKSK7m0IlxE%3D|G|446f9796-4f30-4964-8372-6476ae0fa16d|0|NO_SESSION_TOKEN_COOKIE',
    'OptanonConsent': 'isIABGlobal=false&datestamp=Tue+Dec+26+2023+21%3A14%3A16+GMT%2B0200+(Eastern+European+Standard+Time)&version=202209.1.0&hosts=&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A1%2CC0002%3A1%2CC0004%3A1%2CSPD_BG%3A1&geolocation=UA%3B71&AwaitingReconsent=false',
    '_ga_L7QE48HF7H': 'GS1.1.1703618022.10.1.1703618056.26.0.0',
    '_ga': 'GA1.1.2137685623.1701973025',
    'ftr_ncd': '6',
    'initialTrafficSource': 'utmcsr=(direct)|utmcmd=(none)|utmccn=(not set)',
    '_gcl_au': '1.1.334987340.1701973026',
    '_fbp': 'fb.1.1701973026418.2117193903',
    '__gsas': 'ID=14d03c8303ce92ce:T=1701973026:RT=1701973026:S=ALNI_MYxhiYBMHytQi9VuEwAq4K6dPJiAQ',
    'GSIDNqXoacKY53MN': 'e469cc91-3335-448c-8aad-d6b409163272',
    'STSID974004': '7ef31104-2e60-487f-b544-22125e2be4fd',
    '_clck': '67hnzg%7C2%7Cfhv%7C0%7C1436',
    'cookie': '7ebf16dc-f4e8-4725-9db1-7a4c18b28b0b',
    'cookie_cst': 'zix7LPQsHA%3D%3D',
    '_lc2_fpi': 'ec742730c587--01hh2qyx04azv15mv30hfvp5sm',
    '_lc2_fpi_meta': '{%22w%22:1701973029892}',
    'cto_bundle': 'kCVi319wYjhva1dLMFUwbiUyQmxDSTI0OXNqJTJGSVp4dVQ5Y0drSlg2Ym03RUtXajVvZ3lkOGNrRlU3Tk9PaXFJSU5uMkhrcCUyRksyd0llaDJmJTJGS0EyODd1TEpYSng4NkZzbmswYklrODdxSGNhc29rSnB5RmdreCUyQnZsQXd4WVMwd2J3N2NKTjFoaXZqajhXSTBzVFdrdkk1VVBRWUl3JTNEJTNE',
    'cto_bidid': 'UXty919hYWdldDA0RDczVGc2Qm5oVW9LV2RYVE1Qbjc1VSUyQnglMkJocFNtOHVlNVNFMCUyRkRJQmJDQnJUbmREbW1tWjFUNkZxJTJCUDFNdWl6VVFBQnNhRHlMN09lYURBc1VGWiUyQk1oZUF2TzhtN0dWNXBvJTJCNCUzRA',
    '__gads': 'ID=eeeb3e53fb765c0d:T=1701973030:RT=1703618029:S=ALNI_MZTKza_W6ZD8VNsryOo1X2yH11Qyw',
    '__gpi': 'UID=00000d0f5dc548e6:T=1701973030:RT=1703618029:S=ALNI_MYe364hMa3ne8TsNtZlXmje_HC2Lg',
    '_li_ss': 'ChMKBgjdARDpFgoJCP____8HEPMW',
    '_li_ss_meta': '{%22w%22:1703618031098%2C%22e%22:1706210031098}',
    '__qca': 'P0-1677372596-1701973029906',
    'cto_dna_bundle': 'UNhY7l9BTFhadDQzNTJjbm1CQyUyQkU0OTI4QlFyVHp0RnhHNHJCUDFQJTJCZGRIdnVRdVNLeFAxRmpwMEZNbzFJN1BkSndJUklXbiUyQk9tYVoydHVJNG5hYkxPUmxVdyUzRCUzRA',
    'OptanonAlertBoxClosed': '2023-12-26T19:14:16.090Z',
    '_li_dcdm_c': '.sears.com',
    '__utmzzses': '1',
    'ltkSubscriber-Footer': 'eyJsdGtDaGFubmVsIjoiZW1haWwiLCJsdGtUcmlnZ2VyIjoibG9hZCJ9',
    'ltkpopup-session-depth': '4-8',
    '__cf_bm': 'Ab6GjLBVIWJWNlO5ppgB996B9Mq8MB9mudlbzpsSG70-1703618018-1-AdSpDelHc9oumBcHZraAn+SEoQki7ukMiHyi+lN12IhHlBdEDkOeCjT/+xP3AhZiKSEtH1TTuIDmInI4unV94wWsZbnqk0l7T0hdsRxb5XHl',
    'ftr_blst_1h': '1703618021414',
    'zipCode': '10101',
    'city': 'New York',
    'state': 'NY',
    '_gid': 'GA1.2.1990459217.1703618022',
    '_gat_UA-224801747-1': '1',
    '__pr.3q8y1p': '7JY9XuqHMq',
    '_uetsid': 'e5284d80a42211eebb83df30999f2807',
    '_uetvid': 'd41d3710952c11eeaaec1fa2b115e97d',
    '_clsk': '1ig43zb%7C1703618028642%7C1%7C1%7Ce.clarity.ms%2Fcollect',
}


def save_or_update_scraped_products_data(products_ids):
    for product_id in products_ids:
        time.sleep(random.randint(7, 10))
        try:
            product_data = scrape_product_data(product_id, headers, cookies)

            obj, created = ScrapedProduct.objects.update_or_create(
                product_id=product_id,
                defaults={**product_data},
            )
            if created:
                logging.info(f"Product ID {product_id} processed. Product data created successfully!")
            else:
                logging.info(f"Product ID {product_id} processed. Product data updated successfully!")
        except Exception as e:
            logging.error((f"Error scraping product {product_id}: {str(e)}"))


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    import django

    django.setup()

    from products.models import ScrapedProduct

    products_ids = sys.argv[1:]
    save_or_update_scraped_products_data(products_ids)
