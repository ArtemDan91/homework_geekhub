"""
1. Викорисовуючи requests, написати скрипт, який буде приймати на вхід ID категорії 
із сайту https://www.sears.com і буде збирати всі товари із цієї категорії, збирати 
по ним всі можливі дані (бренд, категорія, модель, ціна, рейтинг тощо) і зберігати 
їх у CSV файл (наприклад, якщо категорія має ID 12345, то файл буде називатись 
12345_products.csv)
"""

import time
import requests
import csv
import random
from pathlib import Path
from urllib.parse import urljoin
from requests import RequestException

category_id = '1101270'
referer = 'https://www.sears.com/appliances-dryers/b-1101270'

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.5',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Referer': f'{referer}',
    'Content-Type': 'application/json',
    'Authorization': 'SEARS',
    'Connection': 'keep-alive',
    # 'Cookie': '__cf_bm=xCXBBqpW7cm76fUjA_cWFKNkYPQ3FaJYurKIC2KRqZk-1701973023-0-AQvvi7kxas/xj2f3ttB1uO1eLu4pBAM1LkP78v3mfV5O7dvw/UzSMQAXqQMSsqRs/IUkWioSQ2rgSAfehcbllSBqMSUsQ5rN1/916U4BRGbA; forterToken=4c74ca22d2204b00a5a8977c84fd9bd9_1701973073062_520_dUAL43c-m4_13ck; cf_clearance=Qhdy4bhd3MQs2zIkbEUm3dKf3NfmsIbaJUzSNWlXgEE-1701973024-0-1-74e7ca2c.29a24422.1230103-0.2.1701973024; irp=a55e48be-7c31-4f73-8d79-ac7b1620bdb4|P87eevn5zO%2BM5kEPtOJEsGn29%2BwXbBd%2FzOQBw7dZuC4%3D|G|a04e9c96-7b53-4278-ae98-6c88be9616ff|0|NO_SESSION_TOKEN_COOKIE; ftr_blst_1h=1701973024657; OptanonConsent=isIABGlobal=false&datestamp=Thu+Dec+07+2023+20%3A17%3A05+GMT%2B0200+(Eastern+European+Standard+Time)&version=202209.1.0&hosts=&landingPath=https%3A%2F%2Fwww.sears.com%2Ftools-tool-storage%2Fb-1025184&groups=C0001%3A1%2CC0003%3A1%2CC0002%3A1%2CSPD_BG%3A1%2CC0004%3A1; _ga_L7QE48HF7H=GS1.1.1701973025.1.1.1701973072.13.0.0; _ga=GA1.2.2137685623.1701973025; ftr_ncd=6; zipCode=10101; city=New York; state=NY; initialTrafficSource=utmcsr=(direct)|utmcmd=(none)|utmccn=(not set); __utmzzses=1; _gcl_au=1.1.334987340.1701973026; _gid=GA1.2.1998817614.1701973026; _gat_UA-224801747-1=1; _fbp=fb.1.1701973026418.2117193903; _uetsid=d41d2660952c11ee817ee99f899a9cfa; _uetvid=d41d3710952c11eeaaec1fa2b115e97d; __gsas=ID=14d03c8303ce92ce:T=1701973026:RT=1701973026:S=ALNI_MYxhiYBMHytQi9VuEwAq4K6dPJiAQ; GSIDNqXoacKY53MN=e469cc91-3335-448c-8aad-d6b409163272; STSID974004=7ef31104-2e60-487f-b544-22125e2be4fd; _clck=67hnzg%7C2%7Cfhc%7C0%7C1436; ltkSubscriber-Footer=eyJsdGtDaGFubmVsIjoiZW1haWwiLCJsdGtUcmlnZ2VyIjoibG9hZCJ9; ltkpopup-session-depth=1-3; _clsk=i1lnco%7C1701973028583%7C1%7C1%7Cp.clarity.ms%2Fcollect; cookie=7ebf16dc-f4e8-4725-9db1-7a4c18b28b0b; cookie_cst=zix7LPQsHA%3D%3D; _li_dcdm_c=.sears.com; _lc2_fpi=ec742730c587--01hh2qyx04azv15mv30hfvp5sm; _lc2_fpi_meta={%22w%22:1701973029892}; cto_bundle=WVQ6xl9wYjhva1dLMFUwbiUyQmxDSTI0OXNqJTJGRWJYUTZocDg0NnF3cG95Rk14d3d0S2JpSnZWMDZiMGFhTEQyMmtFdldjVyUyQmpXcHdidE0xYW1rJTJCR1lOZVVUQXFvY3RhSTZrVlVMMXRNZnprd2s1eGVpTm9OQktKYjBjWTNQUnRpT2xkMVQz; cto_bidid=gz478l9hYWdldDA0RDczVGc2Qm5oVW9LV2RYVE1Qbjc1VSUyQnglMkJocFNtOHVlNVNFMCUyRkRJQmJDQnJUbmREbW1tWjFUNkZxbFFYUXRSRk1icjV5VkpoQ1hpYW5YdyUzRCUzRA; __gads=ID=eeeb3e53fb765c0d:T=1701973030:RT=1701973030:S=ALNI_MZTKza_W6ZD8VNsryOo1X2yH11Qyw; __gpi=UID=00000d0f5dc548e6:T=1701973030:RT=1701973030:S=ALNI_MYe364hMa3ne8TsNtZlXmje_HC2Lg; _li_ss=ChMKBgjdARDWFgoJCP____8HEOAW; _li_ss_meta={%22w%22:1701973031153%2C%22e%22:1704565031153}; __qca=P0-1677372596-1701973029906',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
}

cookies = {
    'forterToken': '4c74ca22d2204b00a5a8977c84fd9bd9_1701988604629_520_UDF43_13ck',
    'cf_clearance': 'Cki.3CZSuPk6yK3m13nWqeeOF.zo3cAMs1aJLYqUoko-1701988605-0-1-c6ab0b40.c0b0dcf.91aa54a0-0.2.1701988605',
    'irp': 'ff8f1bf1-fe36-4355-b352-e52d2117bff9|vtgf%2FaFVEaJ3XseYm7dlb8kcz32O2nvm25FhfYaV3bo%3D|G|bb4d3e03-decf-44b0-9999-ca98c4247139|0|NO_SESSION_TOKEN_COOKIE',
    'OptanonConsent': 'isIABGlobal=false&datestamp=Fri+Dec+08+2023+00%3A36%3A45+GMT%2B0200+(Eastern+European+Standard+Time)&version=202209.1.0&hosts=&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A1%2CC0002%3A1%2CC0004%3A1%2CSPD_BG%3A1&geolocation=UA%3B71&AwaitingReconsent=false',
    '_ga_L7QE48HF7H': 'GS1.1.1701988604.3.0.1701988604.60.0.0',
    '_ga': 'GA1.2.2137685623.1701973025',
    'ftr_ncd': '6',
    'zipCode': '10101',
    'city': 'New York',
    'state': 'NY',
    'initialTrafficSource': 'utmcsr=(direct)|utmcmd=(none)|utmccn=(not set)',
    '_gcl_au': '1.1.334987340.1701973026',
    '_gid': 'GA1.2.1998817614.1701973026',
    '_fbp': 'fb.1.1701973026418.2117193903',
    '__gsas': 'ID=14d03c8303ce92ce:T=1701973026:RT=1701973026:S=ALNI_MYxhiYBMHytQi9VuEwAq4K6dPJiAQ',
    'GSIDNqXoacKY53MN': 'e469cc91-3335-448c-8aad-d6b409163272',
    'STSID974004': '7ef31104-2e60-487f-b544-22125e2be4fd',
    '_clck': '67hnzg%7C2%7Cfhc%7C0%7C1436',
    'cookie': '7ebf16dc-f4e8-4725-9db1-7a4c18b28b0b',
    'cookie_cst': 'zix7LPQsHA%3D%3D',
    '_lc2_fpi': 'ec742730c587--01hh2qyx04azv15mv30hfvp5sm',
    '_lc2_fpi_meta': '{%22w%22:1701973029892}',
    'cto_bundle': 'XPHkO19wYjhva1dLMFUwbiUyQmxDSTI0OXNqJTJGTUZnVUtiV1p1ZTBiR3RkOENzWTluJTJCRnIzc0ZUVVp0YTYzelB1TURjQ0ZVdlB6c2Npekp6eVRySjV5a0NuT2klMkJiRld2czgxWWl0UGtyZmNQUDVtNUd4WXlsQm9DVzl4czF2QzNESncyQldYSWUlMkJSQkV1WTBLYm1GazRwVm1INjVRJTNEJTNE',
    'cto_bidid': 'FE3BhV9hYWdldDA0RDczVGc2Qm5oVW9LV2RYVE1Qbjc1VSUyQnglMkJocFNtOHVlNVNFMCUyRkRJQmJDQnJUbmREbW1tWjFUNkZxJTJCUDFNdWl6VVFBQnNhRHlMN09lYURNRGhlS0lTb1Nva3Q3T1k2N2puR25zJTNE',
    '__gads': 'ID=eeeb3e53fb765c0d:T=1701973030:RT=1701988594:S=ALNI_MZTKza_W6ZD8VNsryOo1X2yH11Qyw',
    '__gpi': 'UID=00000d0f5dc548e6:T=1701973030:RT=1701988594:S=ALNI_MYe364hMa3ne8TsNtZlXmje_HC2Lg',
    '_li_ss': 'ChMKBgjdARDWFgoJCP____8HEOAW',
    '_li_ss_meta': '{%22w%22:1701983138156%2C%22e%22:1704575138156}',
    '__qca': 'P0-1677372596-1701973029906',
    'cto_dna_bundle': 'aESX4l9BTFhadDQzNTJjbm1CQyUyQkU0OTI4QlFyVHp0RnhHNHJCUDFQJTJCZGRIdnVRdVNLeFAxRmpwMEZNbzFJN1BkSndJUndralplbUtZMW1qYVk1NHp6bjkwY3clM0QlM0Q',
    '__utmzzses': '1',
    'ltkSubscriber-Footer': 'eyJsdGtDaGFubmVsIjoiZW1haWwiLCJsdGtUcmlnZ2VyIjoibG9hZCJ9',
    'ltkpopup-session-depth': '1-2',
    '_li_dcdm_c': '.sears.com',
    'OptanonAlertBoxClosed': '2023-12-07T22:36:45.483Z',
    '_uetsid': 'd41d2660952c11ee817ee99f899a9cfa',
    '_uetvid': 'd41d3710952c11eeaaec1fa2b115e97d',
    '__cf_bm': 'axk5F9sSa9Gy6vImSgkgBcDAoeDKaQKU2n.LZR.3I34-1701988604-0-AY42O7DdXtjihdqzD2P4yXcdZLeAhtvHg+NPd85o1srr2/kqLiD4IH+Ruk/NPKJj5Z2sakUx+02pLaut023yILcfGj0IVVTx4ORksjyyvPKS',
    'ftr_blst_1h': '1701988605312',
}


def get_products_list(category_id, headers):
    start_index = 1
    end_index = 300
    products = []
    while True:
        time.sleep(random.randint(15, 20))
        print(f'{start_index=}, {end_index=}')
        try:
            response = requests.get(
                f'https://www.sears.com/api/sal/v3/products/search?startIndex={start_index}&endIndex={end_index}&searchType=category&catalogId=12605&store=Sears&storeId=10153&zipCode=10101&bratRedirectInd=true&catPredictionInd=true&disableBundleInd=true&filterValueLimit=500&includeFiltersInd=true&shipOrDelivery=true&solrxcatRedirection=true&sortBy=ORIGINAL_SORT_ORDER&whiteListCacheLoad=false&eagerCacheLoad=true&slimResponseInd=true&catGroupId={category_id}',
                headers=headers,
                cookies=cookies
            )
            if response.status_code == 200:
                data = response.json()
                items = data.get('items', [])
                if not items:
                    break

                for item in data['items']:
                    products.append(
                        {
                            'brand_name': item['brandName'],
                            'category_name': item['category'],
                            'product_name': item['name'],
                            'sell_price': item['price']['finalPriceDisplay'],
                            'url': urljoin('https://www.sears.com', item['additionalAttributes']['seoUrl']),
                        }
                    )

                start_index += len(items)
                end_index += len(items)
            else:
                break
        except RequestException as e:
            raise RequestException(f"Помилка під час HTTP-запиту: {e}")

    return products


def write_to_csv():
    parent_dir = Path(__file__).resolve().parent
    try:
        products_list = get_products_list(category_id, headers)

        if products_list:
            with open(parent_dir / f'{category_id}_products.csv', 'w') as file:
                fieldnames = ['brand_name', 'category_name', 'product_name', 'sell_price', 'url']
                writer = csv.DictWriter(file, quoting=csv.QUOTE_NONNUMERIC, fieldnames=fieldnames)
                writer.writeheader()
                for product in products_list:
                    writer.writerow(product)
    except RequestException as e:
        print(e)


if __name__ == "__main__":
    write_to_csv()

