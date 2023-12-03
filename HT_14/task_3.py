"""
3. http://quotes.toscrape.com/ - написати скрейпер для збору всієї доступної 
інформації про записи: цитата, автор, інфа про автора тощо. 
- збирається інформація з 10 сторінок сайту.
- зберігати зібрані дані у CSV файл
"""

import requests
import csv
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
from pathlib import Path

session = requests.Session()


def get_total_pages_count():
    page_number = 1

    while True:

        try:
            response = session.get(f'https://quotes.toscrape.com/page/{page_number}')
            soup = BeautifulSoup(response.text, 'lxml')
            next_page = soup.find('li', class_='next')
            
            if next_page:
                page_number += 1
            else:
                break

        except RequestException as e:
            raise RequestException(f"Помилка під час HTTP-запиту: {e}")
    return page_number


def get_author_info(url):
    authors_info_dict = {}

    try:
        headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"}
        response = session.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')

        
        author_born_date = soup.find('span', class_='author-born-date').text
        author_born_location = soup.find('span', class_='author-born-location').text
        author_description = soup.find('div', class_='author-description').text.strip().replace('\n', '')
        
        authors_info_dict['born_date'] = author_born_date
        authors_info_dict['born_location'] = author_born_location
        authors_info_dict['description'] = author_description

        return authors_info_dict
    
    except RequestException as e:
        raise RequestException(f"Помилка під час HTTP-запиту: {e}")


def get_data_from_pages():
    authors_data_dict = {}

    total_pages = get_total_pages_count()
    if total_pages > 0:
        try:
            for page_number in range(1, total_pages + 1):
                headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"}
                response = session.get(f'https://quotes.toscrape.com/page/{page_number}', headers=headers)
                soup = BeautifulSoup(response.text, 'lxml')

                quotes = soup.find_all('div', class_='quote')

                for quote in quotes:
                    quote_text = quote.select_one('span.text').text.replace('“', '').replace('”', '')
                    author_name = quote.select_one('span small.author').text
                    author_info_url = 'http://quotes.toscrape.com' + quote.select_one('span a').get('href')
                    
                    if author_name not in authors_data_dict:
                        authors_data_dict[author_name] = {'quotes': [], 'author_info': {}}
                        try:
                            author_info = get_author_info(author_info_url)
                            if author_info:
                                authors_data_dict[author_name]['author_info'] = author_info
                        except RequestException as e:
                            raise RequestException(f"Помилка під час HTTP-запиту: {e}")
                    authors_data_dict[author_name]['quotes'].append(quote_text)

            return authors_data_dict
        except RequestException as e:
            raise RequestException(f"Помилка під час HTTP-запиту: {e}")


def write_to_csv():
    parent_dir = Path(__file__).resolve().parent
    try:
        authors_data_dict = get_data_from_pages()
        if authors_data_dict:
            with open(parent_dir / 'authors_quotes.csv', 'w', newline='') as file:
                fieldnames = ['Author', 'Quotes', 'Born_Date', 'Born_Location', 'Description']
                writer = csv.DictWriter(file, fieldnames=fieldnames)

                writer.writeheader()

                for author_name, author_data in authors_data_dict.items():
                    row_data = {
                        'Author': author_name,
                        'Quotes': author_data['quotes'],
                        'Born_Date': author_data['author_info']['born_date'],
                        'Born_Location': author_data['author_info']['born_location'],
                        'Description': author_data['author_info']['description']
                    }
                    writer.writerow(row_data)
    except RequestException as e:
        print(e)


if __name__ == "__main__":
    write_to_csv()