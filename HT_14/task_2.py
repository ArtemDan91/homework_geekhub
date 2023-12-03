"""
2. Створіть програму для отримання курсу валют за певний період. 
- отримати від користувача дату (це може бути як один день так і інтервал - 
початкова і кінцева дати, продумайте механізм реалізації) і назву валюти
- вивести курс по відношенню до гривні на момент вказаної дати 
(або за кожен день у вказаному інтервалі)
- не забудьте перевірку на валідність введених даних
"""

import requests
import re
import json
from datetime import datetime
from pandas import date_range
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from requests.exceptions import RequestException


class MissingDataError(Exception):
    pass 


class DateIntervalValidationError(Exception):
    pass


class InvalidInputError(Exception):
    pass


def create_rate_data(date, currency_code):
    try:
        url = f"https://api.privatbank.ua/p24api/exchange_rates?json&date={date}"
        headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"}

        response = requests.get(url, headers=headers)
        rates_data = response.json()

        exchange_rates = rates_data['exchangeRate']
        if not exchange_rates:
            raise MissingDataError(f"Для дати {date} та коду валюти {currency_code} відсутні дані")

        for rate in exchange_rates:
            if rate['currency'] == currency_code:
                return float(rate['purchaseRate']), float(rate['saleRate'])
    except RequestException as e:
        raise RequestException(f"Помилка під час HTTP-запиту: {e}")


def get_available_currency_dict():
    driver = None
    try:
        url = f"https://api.privatbank.ua/#p24/exchangeArchive"
        driver = webdriver.Chrome()
        driver.get(url)
        html_code = driver.page_source
        

        soup = BeautifulSoup(html_code, 'lxml')
        currencies_table = soup.select_one('div.api-description table')

        currencies_dict = {}

        for index, data in enumerate(currencies_table.find_all('tr')[1:5], 1):
            currency_data = data.find_all('td')
            currency_code = currency_data[0].text.strip()
            currency_name = currency_data[1].text.strip()
            currencies_dict[index] = {'currency_code': currency_code, 'currency_name': currency_name}
        
        with open('HT_14/available_currencies.json', 'w', encoding='utf-8') as json_file:
            json.dump(currencies_dict, json_file, ensure_ascii=False, indent=4)
    except WebDriverException as e:
        print(f"Виникла помилка WebDriver: {e}")
    finally:
        if driver is not None:
            driver.close()


def date_input_validation(input_value):
    try:
        datetime.strptime(input_value, '%d.%m.%Y')
        return True
    except ValueError as e:
        raise ValueError(f"Не вірний формат дати: {e}")


def display_currency_list():
    print("Список доступних валют:")
    try:
        with open('HT_14/available_currencies.json') as json_file:
            currencies = json.load(json_file)
        for num, currency in currencies.items():
            print(f"{num}. {currency['currency_name']} - {currency['currency_code']}")
        return currencies
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Виникла помилка при роботі з файлом: {e}")


def get_currency_code():
    while True:
        try:
            currencies = display_currency_list()
            if currencies:
                num = input("Оберіть код валюти: ")
                if num in currencies:
                    return currencies[num]['currency_code']
                else:
                    raise InvalidInputError("Ви зробили неправильний вибір, повторіть операцію")
        except FileNotFoundError as e:
            raise e
        

def get_privatbank_exchange_rate_for_date():
    date = input("Введіть дату (у форматі DD.MM.YYYY): ")
    try:
        currency_code = get_currency_code()
        if currency_code:
            try:
            
                if date_input_validation(date):
                    try:
                        purchase_rate, sale_rate = create_rate_data(date, currency_code)

                        if purchase_rate is not None and sale_rate is not None:
                            print(f'Курс валюти {currency_code} на {date}:')
                            print(f'Покупка: {purchase_rate}')
                            print(f'Продаж: {sale_rate}')
                    except (RequestException, MissingDataError) as e:
                        raise e
            except ValueError as e:
                raise e
    except (FileNotFoundError, InvalidInputError) as e:
        raise e


def date_interval_validation(start_date_input, end_date_input):
    try:
        if date_input_validation(start_date_input) and date_input_validation(end_date_input):
            start_date_obj = datetime.strptime(start_date_input, '%d.%m.%Y')
            end_date_obj = datetime.strptime(end_date_input, '%d.%m.%Y')

            if start_date_obj > end_date_obj:
                raise DateIntervalValidationError("Початкова дата повинна бути меншою або рівною кінцевій даті.")
            
            return True
    except ValueError as e:
        raise e

      
def create_date_range(start_date, end_date):
    start_date_obj = datetime.strptime(start_date, '%d.%m.%Y')
    end_date_obj = datetime.strptime(end_date, '%d.%m.%Y')

    created_date_range = date_range(start=start_date_obj, end=end_date_obj)

    return created_date_range


def get_privatbank_exchange_rate_for_date_interval():
    date_interval = input("Введіть діапазон дат (у форматі DD.MM.YYYY-DD.MM.YYYY): ")
    
    try:
        currency_code = get_currency_code()
        if currency_code:
            try:
                if '-' in date_interval:
                    start_date, end_date = date_interval.split("-")
                    if date_interval_validation(start_date, end_date):
                        
                        date_range = create_date_range(start_date, end_date)
                        
                        for date in date_range:
                            api_date = date.strftime('%d.%m.%Y')
                            try:
                                purchase_rate, sale_rate = create_rate_data(api_date, currency_code)

                                if purchase_rate is not None and sale_rate is not None:
                                    print(f'Курс валюти {currency_code} на {api_date}:')
                                    print(f'Покупка: {purchase_rate}')
                                    print(f'Продаж: {sale_rate}')
                            except MissingDataError as e:
                                print(e)
                                continue
                            except RequestException as e:
                                raise e
                else:
                    raise DateIntervalValidationError("Невірний формат інтервалу дати. Використовуйте формат DD.MM.YYYY-DD.MM.YYYY")
            
            except ValueError as e:
                raise e
    except FileNotFoundError as e:
        raise e
            

def handle_exchange_rate_function(func):
    while True:
        try:
            func()
            return True
        except (FileNotFoundError, ValueError, MissingDataError, InvalidInputError, RequestException, DateIntervalValidationError) as e:
            print(e)
            continue    

            

def main():
    menu_options = {
        '1': get_privatbank_exchange_rate_for_date,
        '2': get_privatbank_exchange_rate_for_date_interval
    }
    while True:
        try:
            print("Оберіть цифру із запропонованих для вибору необхідних дій: ")
            print("1. Отримати курс валют на певну дату")
            print("2. Отримати курс валют за певний період")

            choice = input("Ваший вибір: ")
            if choice == '1' or choice == '2':
                selected_function = menu_options[choice]
                if selected_function:
                    if handle_exchange_rate_function(selected_function):
                        break
            
            else:
                raise InvalidInputError("Ви зробили неправильний вибір, повторіть операцію")
        except (FileNotFoundError, ValueError, MissingDataError, InvalidInputError, RequestException, DateIntervalValidationError) as error:
            print(error)
            
            

if __name__ == "__main__":
    main()