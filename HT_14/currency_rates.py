import requests
from requests.exceptions import RequestException


def get_current_exchange_rates():
    
    try:
        headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"}
        response = requests.get("https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5", headers=headers)
        data = response.json()

        currency_rates = {}

        for currency in data:
            currency_code = currency['ccy']
            buy_rate = float(currency['buy'])
            sell_rate = float(currency['sale'])
            
            currency_rates[currency_code] = {'buy': buy_rate, 'sell': sell_rate}

        return currency_rates
    
    except RequestException as e:
        raise RequestException(f"Помилка під час HTTP-запиту: {e}")


if __name__ == "__main__":
    print(get_current_exchange_rates())