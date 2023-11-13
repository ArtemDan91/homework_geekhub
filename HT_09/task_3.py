"""
Програма-банкомат.
   Використувуючи функції створити програму з наступним функціоналом:
      - підтримка 3-4 користувачів, які валідуються парою ім'я/пароль (файл <users.CSV>);
      - кожен з користувачів має свій поточний баланс (файл <{username}_balance.TXT>) та 
      історію транзакцій (файл <{username_transactions.JSON>);
      - є можливість як вносити гроші, так і знімати їх. Обов'язкова перевірка 
      введених даних (введено цифри; знімається не більше, ніж є на рахунку і т.д.).
   Особливості реалізації:
      - файл з балансом - оновлюється кожен раз при зміні балансу (містить просто цифру з балансом);
      - файл - транзакціями - кожна транзакція у вигляді JSON рядка додається в кінець файла;
      - файл з користувачами: тільки читається. Але якщо захочете реалізувати функціонал 
      додавання нового користувача - не стримуйте себе :)
   Особливості функціонала:
      - за кожен функціонал відповідає окрема функція;
      - основна функція - <start()> - буде в собі містити весь workflow банкомата:
      - на початку роботи - логін користувача (програма запитує ім'я/пароль). Якщо вони 
      неправильні - вивести повідомлення про це і закінчити роботу (хочете - зробіть 3 спроби, 
      а потім вже закінчити роботу - все на ентузіазмі :))
      - потім - елементарне меню типн:
        Введіть дію:
           1. Продивитись баланс
           2. Поповнити баланс
           3. Вихід
      - далі - фантазія і креатив, можете розширювати функціонал, але основне 
      завдання має бути повністю реалізоване :)
    P.S. Увага! Файли мають бути саме вказаних форматів (csv, txt, json відповідно)
    P.S.S. Добре продумайте структуру програми та функцій (edited) 
"""

import csv
import json
import re
from datetime import datetime
from pathlib import Path

parent_dir = Path(__file__).resolve().parent


class UsernameValidationError(Exception):
    pass


class PasswordValidationError(Exception):
    pass


class MaxAttemptsLoginError(Exception):
    pass


class MaxAttemptsPassInputError(Exception):
    pass


class InvalidInputError(Exception):
    pass


class NegativeInputAmountError(Exception):
    pass


class NegativeBalanceError(Exception):
    pass


def username_validation(username):
    username_pattern = r'^[a-zA-Z0-9]{3,50}$'

    if not re.match(username_pattern, username):
        raise UsernameValidationError("Ім'я має включати лише латинські літери, бути не меншим за 3 символа і не більшим за 50, забороняється використовувати спецсимволи!")
    return True


def password_validation(password):
    password_pattern = r'^(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[!@#$%&*?])[\dA-Za-z!@#$%&*?]{8,}$'

    if not re.match(password_pattern, password):
        raise PasswordValidationError("Пароль повинен бути довжиною мінімум 8 символів,мати хоча б одну цифру, одну велику літеру, одну маленьку та один спецсимвол!")
    return True


def create_user_files(username, parent_dir):
    balance_file_path = parent_dir / "users_balances" / f"{username}_balance.txt"
    transactions_file_path = parent_dir / "users_transactions" / f"{username}_transactions.json"

    if not balance_file_path.exists():
        balance_file_path.write_text("0")
    if not transactions_file_path.exists():
        transactions_file_path.write_text("[]")


def create_users(parent_dir):
    users = [
        {"username": "john", "password": "JohnJohn77!!"},
        {"username": "mary", "password": "Mary12345!"},
        {"username": "david", "password": "D@vidp@ss1"},
        {"username": "michael", "password": "Michael1991?"},
    ]
    file_name = "users.csv"
    
    try:
        with open(parent_dir / file_name, 'w') as file:
            fieldnames = ["username", "password"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for user in users:
                if username_validation(user["username"]) and password_validation(user["password"]):
                    writer.writerow(user)
                    create_user_files(user["username"], parent_dir)
    except (UsernameValidationError, PasswordValidationError) as error:
        print(error)


def username_input():
    username = input("Введіть ім'я користувача: ")
    if not username_validation(username):
        raise UsernameValidationError("Ім'я має включати лише латинські літери, бути не меншим за 3 символа і не більшим за 50, забороняється використовувати спецсимволи!")
    return username


def password_input():
    max_attempts = 3
    pass_attempt = 0

    while pass_attempt < max_attempts:
        password = input("Введіть пароль: ")
        
        try:
            if not password_validation(password):
                raise PasswordValidationError("Пароль повинен бути довжиною мінімум 8 символів,мати хоча б одну цифру, одну велику літеру, одну маленьку та один спецсимвол!")
            else:
                return password            
        except PasswordValidationError as error:
            print(error)

        pass_attempt += 1
        pass_attempts_left = max_attempts - pass_attempt
        if pass_attempts_left > 0:
            print(f"Введено не правильний пароль, залишилось спроб: {pass_attempts_left}")
    if pass_attempt == max_attempts:
        raise MaxAttemptsPassInputError("Досягнуто максимальну кількість спроб для введення паролю")
    

def login_user(parent_dir):
    max_attempts = 3
    cur_log_attempt = 0
    try:
        while cur_log_attempt < max_attempts:
            try:
                username = username_input()
                password = password_input()
                
                users_file_name = "users.csv"                 
                with open(parent_dir / users_file_name, 'r') as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        if row["username"] == username and row["password"] == password:
                            print("Успішний вхід")
                            return username
                
            except (UsernameValidationError, MaxAttemptsPassInputError) as error:
                print(error)
            except FileNotFoundError:
                print((f"Файл {users_file_name} не знайдено"))
            except Exception as error:
                print(f"Невідома помилка при виконанні операції: {error}")

            cur_log_attempt += 1
            attempts_left = max_attempts - cur_log_attempt
            if attempts_left > 0:
                print(f"Залишилося спроб для входу: {attempts_left}")

        if cur_log_attempt == max_attempts:
            raise MaxAttemptsLoginError("Досягнуто максимальну кількість спроб для входу")
    except MaxAttemptsLoginError as error:
        print(error)        


def check_user_exists(username, parent_dir):
    users_file_name = "users.csv"
    try:             
        with open(parent_dir / users_file_name, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["username"] == username:
                    return True
    except FileNotFoundError:
        print((f"Файл {users_file_name} не знайдено"))                
    return False


def register_new_user(parent_dir):
    while True:
        try:
            username = username_input()
            
            if check_user_exists(username, parent_dir):
                print("Користувач з даним ім'ям вже існує, придумайте нове ім'я")
                continue

            password = password_input()
            users_file_name = "users.csv"          
            with open(parent_dir / users_file_name, 'a') as file:
                fieldnames = ["username", "password"]
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writerow({"username": username, "password": password})
                create_user_files(username, parent_dir)
                print("Дані успішно додані. Тепер ви можете увійти у ваший обліковий запис")
                return username
        
        except (UsernameValidationError, PasswordValidationError, MaxAttemptsPassInputError) as error:
            print(error)
        except FileNotFoundError:
            print((f"Файл {users_file_name} не знайдено"))   


def register_and_login_user():
    while True:
        current_user = register_new_user(parent_dir)
        if current_user:
            print("Бажаєте увійти? (так/ні): ")
            choice = input().lower()
            if choice == 'так':
                atm_operations(current_user)
                break
            elif choice == 'ні':
                print(f"До наступної зустрічі!")
                break
            else:
                print("Ви зробили неправильний вибір, повторіть операцію")


def display_balance(current_user, parent_dir):
    balance_file_name = f"users_balances/{current_user}_balance.txt"
    try:
        with open(parent_dir / balance_file_name, 'r') as file:
            balance = float(file.read())
            print(f"Баланс користувача {current_user} складає: {balance} грн.")
    except FileNotFoundError:
        print(f"Файл {balance_file_name} не знайдено")
    

def check_input_value(input_value):
    while True:
        try:
            amount = float(input_value)
            if amount < 0:
                raise NegativeInputAmountError("Значення введеної суми не може бути від'ємним числом")
            return amount
        except ValueError:
            print("Значення введеної суми повинне бути числом")
        
        input_value = input("Введіть суму для поповнення повторно: ")


def update_transactions_file(parent_dir, transactions_file_name, transaction):
    try:
        with open(parent_dir / transactions_file_name, 'r') as file:
            transactions = json.load(file)
        
        transactions.append(transaction)

        with open(parent_dir / transactions_file_name, 'w') as file:
            json.dump(transactions, file, indent=4, default=str)
        
    except FileNotFoundError:
        print(f"Файл {transactions_file_name} не знайдено")


def make_deposit(current_user, parent_dir):
    try:
        input_value = input("Введіть суму для поповнення: ")
        amount = check_input_value(input_value)
        
        balance_file_name = f"users_balances/{current_user}_balance.txt"
        transactions_file_name = f"users_transactions/{current_user}_transactions.json"

        try:
            with open(parent_dir / balance_file_name, 'r') as file:
                data = file.read()
                current_balance = float(data) if data.strip() else 0.0
        
            new_balance = current_balance + amount

            with open(parent_dir / balance_file_name, 'w') as file:
                file.write(str(new_balance))
        except FileNotFoundError:
            print(f"Файл {balance_file_name} не знайдено")

        transaction = {
            "type": "deposit",
            "amount": amount,
            "time": datetime.now()
        }

        update_transactions_file(parent_dir, transactions_file_name, transaction)
        print("Операцій поповнення балансу проведена успішно")

    except NegativeInputAmountError as error:
        print(error)


def cash_out(current_user, parent_dir):
    try:
        input_value = input("Введіть суму для зняття: ")
        amount = check_input_value(input_value)

        balance_file_name = f"users_balances/{current_user}_balance.txt"
        transactions_file_name = f"users_transactions/{current_user}_transactions.json"
        
        try:
            with open(parent_dir / balance_file_name, 'r') as file:
                data = file.read()
                current_balance = float(data) if data.strip() else 0.0
            
            if amount > current_balance:
                raise NegativeBalanceError("Недостатньо коштів на рахунку.")

            new_balance = current_balance - amount

            with open(parent_dir / balance_file_name, 'w') as file:
                file.write(str(new_balance))
               
        except FileNotFoundError:
            print(f"Файл {balance_file_name} не знайдено")

        transaction = {
            "type": "cash_out",
            "amount": amount,
            "time": datetime.now()
        }

        update_transactions_file(parent_dir, transactions_file_name, transaction)
        print("Операцій зняття коштів проведена успішно")

    except NegativeInputAmountError as error:
        print(error)
    except NegativeBalanceError as error:
        print(error)
    
   
def view_transactions(current_user, parent_dir):
    transactions_file_name = f"users_transactions/{current_user}_transactions.json"
    
    try:
        with open(parent_dir / transactions_file_name, 'r') as file:
            transactions = json.load(file)
            
            if not transactions:
                print("Історія транзакцій порожня.")
            else:
                print("Історія транзакцій:")
                for transaction in transactions:
                    print(transaction)
    
    except FileNotFoundError:
        print(f"Файл {transactions_file_name} не знайдено")


def exit_operation(current_user):
    print(f"До наступної зустрічі, {current_user}!")


def ask_user_to_continue(current_user):
    while True:
        user_input = input("Бажаєте продовжити? (так/ні): ")
        if user_input.lower() == 'так':
            return True
        elif user_input.lower() == 'ні':
            print(f"До наступної зустрічі, {current_user}!")
            return False
        else:
            print("Невірна відповідь. Спробуйте ще раз.")


def atm_operations(current_user):
    operations = {
        '1': {'title': 'Переглянути баланс', 'operation': display_balance},
        '2': {'title': 'Поповнити баланс', 'operation': make_deposit},
        '3': {'title': 'Зняти кошти', 'operation': cash_out},
        '4': {'title': 'Переглянути транзакції', 'operation': view_transactions},
        '5': {'title': 'Вихід', 'operation': exit_operation},
    }
    while True:
        try:
            print("Оберіть номер операції")
            for key, value in operations.items():
                print(f"{key}.{value['title']}")

            choice = input("Ваший вибір: ")
            if choice in operations:
                operation = operations[choice]['operation']
                if operation != exit_operation:
                    operation(current_user, parent_dir)
                else:
                    operation(current_user)
                
                if choice == '5' or not ask_user_to_continue(current_user):
                    break

            else:
                raise InvalidInputError("Ви зробили неправильний вибір, повторіть операцію")
        except InvalidInputError as error:
            print(error)


def start():
    while True:
        try:
            print("Оберіть цифру із запропонованих для вибору необхідних дій: ")
            print("1. Увійти")
            print("2. Зареєструватися")
            print("3. Вихід")

            choice = input("Ваший вибір: ")
            if choice == '1':
                current_user = login_user(parent_dir)
                if current_user:
                    atm_operations(current_user)
            elif choice == '2':
                register_and_login_user()
            elif choice == '3':
                print(f"До наступної зустрічі!")
                break
            else:
                raise InvalidInputError("Ви зробили неправильний вибір, повторіть операцію")
        except InvalidInputError as error:
            print(error)


if __name__ == "__main__":
    start()