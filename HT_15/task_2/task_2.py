"""
2. Викорисовуючи requests, заходите на ось цей сайт "https://www.expireddomains.net/deleted-domains/" 
(з ним будьте обережні), вибираєте будь-яку на ваш вибір доменну зону і парсите список  доменів - 
їх там буде десятки тисяч (звичайно ураховуючи пагінацію). Всі отримані значення зберігти в CSV файл.
"""

import requests
import time
import csv
import random
from pathlib import Path
from bs4 import BeautifulSoup
from requests.exceptions import RequestException

base_url = "https://www.expireddomains.net/deleted-com-domains/?start=0#listing"
headers = {
    'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
}


def get_next_page_url(base_url, headers):
    while True:
        try:
            response = requests.get(base_url, headers=headers)

            soup = BeautifulSoup(response.text, 'lxml')
            next_page_tag = soup.find('a', class_='next')

            if next_page_tag:
                next_page_url = "https://www.expireddomains.net" + next_page_tag.get('href')
                yield next_page_url
                base_url = next_page_url

            else:
                break

        except RequestException as e:
            raise RequestException(f"Помилка під час HTTP-запиту: {e}")


def scrape_domains_from_page(url, headers):
    try:
        response = requests.get(url, headers=headers)    
        soup = BeautifulSoup(response.text, 'lxml')

        domain_table = soup.find('table', {'class': 'base1'})

        if domain_table:
            rows = domain_table.find_all('tr')
            domains_list = [row.find('td').find('a').text.strip() for row in rows[1:]]
            return domains_list
        
    except RequestException as e:
        raise RequestException(f"Помилка під час HTTP-запиту: {e}")


def scrape_domains(base_url, headers):
    all_domains_list = []
    try:
        domains_from_first_page = scrape_domains_from_page(base_url, headers)
        print(domains_from_first_page)
        
        if domains_from_first_page:
            all_domains_list.extend(domains_from_first_page)
        
        for next_page_url in get_next_page_url(base_url, headers):
            domains_list = scrape_domains_from_page(next_page_url, headers)
            print(next_page_url)
            print(domains_list)
            
            if domains_list is not None:
                all_domains_list.extend(domains_list)
            time.sleep(random.randint(5, 10))
        
        return all_domains_list
    except RequestException as e:
        raise RequestException(f"Помилка під час HTTP-запиту: {e}")


def write_to_csv():
    parent_dir = Path(__file__).resolve().parent
    try:
        domains_list = scrape_domains(base_url, headers)
        
        if domains_list:
            
            with open(parent_dir / 'domains.csv', 'w') as file:
                writer = csv.writer(file)
                writer.writerow(['Domains'])
                writer.writerows([[domain] for domain in domains_list])
    except RequestException as e:
        print(e)


if __name__== "__main__":
    write_to_csv()