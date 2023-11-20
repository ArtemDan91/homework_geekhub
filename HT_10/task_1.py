"""
HT #10
Банкомат 2.0
    - усі дані зберігаються тільки в sqlite3 базі даних. Більше ніяких файлів. 
    Якщо в попередньому завданні ви добре продумали структуру програми то у вас 
    не виникне проблем швидко адаптувати її до нових вимог.
    - на старті додати можливість залогінитися або створити новго користувача 
    (при створенні новго користувача, перевіряється відповідність логіну і паролю 
    мінімальним вимогам. Для перевірки створіть окремі функції)
    - в таблиці (базі) з користувачами має бути створений унікальний користувач-
    інкасатор, який матиме розширені можливості (домовимось, що логін/пароль 
    будуть admin/admin щоб нам було простіше перевіряти)
    - банкомат має власний баланс
    - кількість купюр в банкоматі обмежена. Номінали купюр - 10, 20, 50, 100, 200, 500, 1000
    - змінювати вручну кількість купюр або подивитися їх залишок в банкоматі може лише інкасатор
    - користувач через банкомат може покласти на рахунок лише сумму кратну мінімальному 
    номіналу що підтримує банкомат. В іншому випадку - повернути "здачу" (наприклад при 
    поклажі 1005 --> повернути 5). Але це не має впливати на баланс/кількість купюр банкомату, 
    лише збільшуєтсья баланс користувача (моделюємо наявність двох незалежних касет в банкоматі 
    - одна на прийом, інша на видачу)
    - зняти можна лише в межах власного балансу, але не більше ніж є всього в банкоматі.
    - при неможливості виконання якоїсь операції - вивести повідомлення з причиною (не вірний
     логін/пароль, недостатньо коштів на раунку, неможливо видати суму наявними купюрами тощо.)
"""

import sqlite3
import re
import json
from datetime import datetime
from pathlib import Path

parent_dir = Path(__file__).resolve().parent


class UsernameValidationError(Exception):
    pass


class PasswordValidationError(Exception):
    pass


class MaxAttemptsPassInputError(Exception):
    pass


class InvalidInputError(Exception):
    pass


class InvalidLoginError(Exception):
    pass


class InvalidDenominationError(Exception):
    pass


class NegativeBanknotesQuantityError(Exception):
    pass


class NegativeInputAmountError(Exception):
    pass


class NegativeAtmBalanceError(Exception):
    pass


class NegativeUserBalanceError(Exception):
    pass


class WithdrawalNotPossibleError(Exception):
    pass


def connect_to_database(database_path=parent_dir / 'atm_database.db'):
    conn = None
    try:
        conn = sqlite3.connect(database_path)
        cur = conn.cursor()
        return conn, cur
    except sqlite3.Error as e:
        raise e


def close_database_connection(conn):
    try:
        if conn:
            conn.close()
    except sqlite3.Error as e:
        print(f"Помилка при роботі з SQLite: {e}")


def create_tables():
    conn = None
    try:
        conn, cur = connect_to_database()
        if conn:
            cur.executescript('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    password TEXT NOT NULL,
                    is_cashier BOOLEAN NOT NULL
                );
                                
                CREATE TABLE IF NOT EXISTS user_balance (
                    user_id INTEGER,
                    username TEXT NOT NULL,
                    balance INTEGER NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                );
                
                CREATE TABLE IF NOT EXISTS user_transactions (
                    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    username TEXT NOT NULL,
                    transaction_details TEXT,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                );
                               
                CREATE TABLE IF NOT EXISTS atm (
                    atm_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    balance INTEGER DEFAULT 0
                );

                CREATE TABLE IF NOT EXISTS atm_banknotes (
                    banknote_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    denomination INTEGER NOT NULL,
                    count INTEGER DEFAULT 0,
                    atm_id INTEGER,
                    FOREIGN KEY (atm_id) REFERENCES atm(atm_id)
                );               
            ''')
            conn.commit()
    except sqlite3.Error as e:
        print(f"Помилка при роботі з SQLite: {e}")
    finally:
        close_database_connection(conn) 


def register_atm_cashier():
    conn = None
    try:
        conn, cur = connect_to_database()
        if conn:
            cur.execute('INSERT INTO users (username, password, is_cashier) VALUES (?, ?, ?)', ('admin', 'admin', True))
            user_id = cur.lastrowid
            cur.execute("INSERT INTO user_balance (user_id, username, balance) VALUES (?, 'admin', 0)", (user_id,))
            conn.commit()
    except sqlite3.Error as e:
        print(f"Помилка при роботі з SQLite: {e}")
    finally:
        close_database_connection(conn)


def insert_atm_banknotes():
    denominations = [10, 20, 50, 100, 200, 500, 1000]
    conn = None
    try:
        conn, cur = connect_to_database()
        if conn:
            cur.execute('INSERT INTO atm (balance) VALUES (0)')
            atm_id = cur.lastrowid

            if atm_id is not None:
                for denomination in denominations:
                    cur.execute('INSERT INTO atm_banknotes (denomination, count, atm_id) VALUES (?, 0, ?)', (denomination, atm_id))
                conn.commit()
                print("Дані для номіналів додано успішно.")         
    except sqlite3.Error as e:
        print(f"Помилка при роботі з SQLite: {e}")
    finally:
        close_database_connection(conn)


def username_input_validation():
    username = input("Введіть ім'я користувача: ")
    username_pattern = r'^[a-zA-Z0-9]{3,50}$'
    if not re.match(username_pattern, username):
        raise UsernameValidationError("Ім'я має включати лише латинські літери, бути не меншим за 3 символа і не більшим за 50, забороняється використовувати спецсимволи!")
    return username


def password_input_validation():
    max_attempts = 3
    pass_attempt = 0

    while pass_attempt < max_attempts:
        password = input("Введіть пароль: ")
        password_pattern = r'^(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[!@#$%&*?])[\dA-Za-z!@#$%&*?]{8,}$'

        try:
            if not re.match(password_pattern, password):
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


def check_user_exists(username):
    conn = None
    try:
        conn, cur = connect_to_database()

        if conn:
            check_user = cur.execute('SELECT * FROM users WHERE username=?', (username,)).fetchone()
            if check_user and check_user[1] == username:
                return True
            return False
    except sqlite3.Error as e:
        print(f"Помилка при роботі з SQLite: {e}")
    finally:
        close_database_connection(conn)
    

def register_new_user():
    conn = None
    while True:
        try:
            username = username_input_validation()
            
            if check_user_exists(username):
                print("Користувач з даним ім'ям вже існує, придумайте нове ім'я")
                continue

            password = password_input_validation()
            try:
                conn, cur = connect_to_database()

                if conn:
                    cur.execute('INSERT INTO users (username, password, is_cashier) VALUES (?, ?, ?)', (username, password, False))
                    user_id = cur.lastrowid
                    cur.execute('INSERT INTO user_balance (user_id, username, balance) VALUES (?, ?, 0)', (user_id, username))

                    conn.commit()
            except sqlite3.Error as e:
                print(f"Помилка при роботі з SQLite: {e}")
            finally:
                close_database_connection(conn) 
            
            print("Дані успішно додані. Тепер ви можете увійти у ваший обліковий запис")
            return username
        
        except (UsernameValidationError, PasswordValidationError, MaxAttemptsPassInputError) as error:
            print(error)


def register_and_login_user():
    while True:
        current_user = register_new_user()
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


def login_user():
    conn = None
    while True:
        try:
            username = input("Введіть ім'я користувача: ")
            password = input("Введіть пароль: ")
            conn, cur = connect_to_database()
            if conn:
                user = cur.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()
                if user:
                    print("Успішний вхід")
                    return username
                else:
                    raise InvalidLoginError("Введений неправильний логін або пароль, повторіть спробу")  

        except (UsernameValidationError, MaxAttemptsPassInputError, InvalidLoginError) as error:
            print(error)
        except sqlite3.Error as e:
            print(f"Помилка при роботі з SQLite: {e}")
        finally:
            close_database_connection(conn)


def display_user_balance(current_user):
    conn = None
    try:
        conn, cur = connect_to_database()
        if conn:
            user_data = cur.execute('SELECT balance FROM user_balance WHERE username = ?', (current_user,)).fetchone()
            print(f"Баланс користувача {current_user} складає: {user_data[0]} грн.")
    except sqlite3.Error as e:
        print(f"Помилка при роботі з SQLite: {e}")
    finally:
        close_database_connection(conn)


def check_input_value(input_value):
    while True:
        try:
            amount = int(input_value)
            if amount < 0:
                raise NegativeInputAmountError("Значення введеної суми не може бути від'ємним числом")
            return amount
        except ValueError:
            print("Значення введеної суми повинне бути цілим числом")

        input_value = input("Введіть суму для поповнення повторно: ")


def update_transactions_file(current_user, operation, amount):
    conn = None
    transaction_details = {
        "type": operation,
        "amount": amount,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    transaction_details_json = json.dumps(transaction_details, default=str)
    try:
        conn, cur = connect_to_database()
        if conn:
            user_id = cur.execute('SELECT user_id FROM users WHERE username = ?', (current_user,)).fetchone()[0]
            cur.execute('INSERT INTO user_transactions (user_id, username, transaction_details) VALUES (?, ?, ?)', (user_id, current_user, transaction_details_json))
            conn.commit()
            
    except sqlite3.Error as e:
        print(f"Помилка при роботі з SQLite: {e}")
    finally:
        close_database_connection(conn)


def make_deposit(current_user):
    conn = None
    try:
        input_value = input("Введіть суму для поповнення: ")
        amount = check_input_value(input_value)

        conn, cur = connect_to_database()
        if conn:
            atm_id = cur.execute('SELECT atm_id, balance FROM atm').fetchone()[0]
            min_denomination = cur.execute('SELECT MIN(denomination) from atm_banknotes WHERE atm_id = ?', (atm_id,)).fetchone()[0]

            deposit_amount =  amount - amount % min_denomination
            cur.execute('UPDATE user_balance SET balance = balance + ? WHERE username = ?', (deposit_amount, current_user))
            conn.commit()
            update_transactions_file(current_user, 'deposit', deposit_amount)

            print(f"Баланс користувача {current_user} поповнено на {deposit_amount} грн..")
            if amount % min_denomination != 0:
                print(f"Решта від виконання операції: {amount - deposit_amount}")
    except NegativeInputAmountError as error:
        print(error)
    except sqlite3.Error as e:
        print(f"Помилка при роботі з SQLite: {e}")
    finally:
        close_database_connection(conn)
          

def is_cash_out_posible(amount, denominations):
    for denomination, count in denominations:
        if amount % denomination == 0 and count > 0:
            return True
    return False


def cash_out(current_user):
    conn = None
    try:
        input_value = input("Введіть суму для зняття: ")
        amount = check_input_value(input_value)

        conn, cur = connect_to_database()
        if conn:
            current_atm_balance = cur.execute('SELECT balance FROM atm').fetchone()[0]
            if amount > current_atm_balance:
                raise NegativeAtmBalanceError("Недостатньо коштів у банкоматі для видачі суми.")

            current_user_balance = cur.execute('SELECT balance FROM user_balance WHERE username = ?', (current_user,)).fetchone()[0]
            if amount > current_user_balance:
                raise NegativeUserBalanceError("Недостатньо коштів на рахунку для видачі суми.")
            
            atm_denominations = cur.execute('SELECT denomination, count FROM atm_banknotes').fetchall()
            atm_available_denominations = [item[0] for item in atm_denominations if item[1] > 0]
            if is_cash_out_posible(amount, atm_denominations):
                cur.execute('UPDATE user_balance SET balance = balance - ? WHERE username = ?', (amount, current_user))
                conn.commit()
                print(f"Знято {amount} грн. з рахунку {current_user}.")
            else:
                raise WithdrawalNotPossibleError(f"Операція знаття не доступна, вкажіть суму, враховуючи доступні номінали: {atm_available_denominations}")              

            update_transactions_file(current_user, 'cash_out', amount)

    except (NegativeInputAmountError, NegativeAtmBalanceError, NegativeUserBalanceError, WithdrawalNotPossibleError) as error:
        print(error)
    except sqlite3.Error as e:
        print(f"Помилка при роботі з SQLite: {e}")
    finally:
        close_database_connection(conn)


def view_transactions(current_user):
    conn = None
    try:
        conn, cur = connect_to_database()
        if conn:
            user_transactions = cur.execute('SELECT transaction_details FROM user_transactions WHERE username = ?', (current_user,)).fetchall()
            for transaction in user_transactions:
                print(transaction)
    except sqlite3.Error as e:
        print(f"Помилка при роботі з SQLite: {e}")
    finally:
        close_database_connection(conn)


def exit_operation(current_user):
    print(f"До наступної зустрічі, {current_user}!")


def calculate_atm_balance():
    conn = None
    try:
        conn, cur = connect_to_database()
        if conn:
            result = cur.execute('SELECT SUM(denomination * count) AS atm_balance FROM atm_banknotes').fetchone()
            return result[0]
    except sqlite3.Error as e:
        print(f"Помилка при роботі з SQLite: {e}")
    finally:
        close_database_connection(conn) 

def display_atm_balance():
    conn = None
    try:
        conn, cur = connect_to_database()
        if conn:
            atm_balance = cur.execute('SELECT balance FROM atm').fetchone()
            print(f"Доступний залишок в банкоматі: {atm_balance[0]} грн.")
    except sqlite3.Error as e:
        print(f"Помилка при роботі з SQLite: {e}")
    finally:
        close_database_connection(conn)


def view_banknotes_balance():
    conn = None
    try:
        conn, cur = connect_to_database()
        if conn:
            atm_banknotes = cur.execute('SELECT denomination, count FROM atm_banknotes').fetchall()

            print("Залишок купюр в банкоматі:")
            for num, row in enumerate(atm_banknotes, 1):
                print(f"{num}. Номінал: {row[0]} грн., кількість: {row[1]} шт.")

    except sqlite3.Error as e:
        print(f"Помилка при роботі з SQLite: {e}")
    finally:
        close_database_connection(conn) 


def ask_user_to_continue(message):
    while True:
        user_input = input(message)
        if user_input == '1':
            return True
        elif user_input == '0':
            return False
        else:
            print("Невірна відповідь. Спробуйте ще раз.")


def update_banknotes_quantity():
    print("Доступні номінали: 10, 20, 50, 100, 200, 500, 1000")
    conn = None
    while True:
        try:
            denomination = int(input("Введіть номінал банкноти: "))
            if denomination not in [10, 20, 50, 100, 200, 500, 1000]:
                raise InvalidDenominationError("Обраний невірний номінал купюри")

            change_quantity = int(input("Введіть зміну кількості купюр (значення з '-' зменшить кількість): "))

            conn, cur = connect_to_database()
            if conn:
                current_quantity = cur.execute('SELECT count FROM atm_banknotes WHERE denomination = ?', (denomination,)).fetchone()
                result = current_quantity[0] + change_quantity
                if result < 0:
                    raise NegativeBanknotesQuantityError("Кількість банкнот не може бути від'ємним числом")
                
                cur.execute('UPDATE atm_banknotes SET count = ? WHERE denomination = ?', (result, denomination))
                conn.commit()
                new_balance = calculate_atm_balance()
                cur.execute("UPDATE atm SET balance = ?", (new_balance,))
                conn.commit()
                print("Дані у таблиці успішно внесені.")
                
                if not ask_user_to_continue("Бажаєте продовжити вносити зміни у кількість доступних курюр? (1 - так / 0 - ні): "):
                    break
                
        except sqlite3.Error as e:
            print(f"Помилка при роботі з SQLite: {e}")
        except ValueError:
            print("Введене значення повинне бути цілим числом")
        except (InvalidDenominationError, NegativeBanknotesQuantityError) as e:
            print(e)
        finally:
            close_database_connection(conn) 


def atm_operations(current_user):
    user_operations = {
        '1': {'title': 'Переглянути баланс рахунку', 'operation': display_user_balance},
        '2': {'title': 'Поповнити баланс рахунку', 'operation': make_deposit},
        '3': {'title': 'Зняти кошти з рахунку', 'operation': cash_out},
        '4': {'title': 'Переглянути транзакції по рахунку', 'operation': view_transactions},
        '5': {'title': 'Вихід', 'operation': exit_operation},
    }    
    cashier_operations = {
        '6': {'title': 'Переглянути баланс банкомату', 'operation': display_atm_balance},
        '7': {'title': 'Переглянути залишок купюр в банкоматі', 'operation': view_banknotes_balance},    
        '8': {'title': 'Змінити кількість купюр', 'operation': update_banknotes_quantity},       
    }
 
    while True:
        try:
            print("Оберіть номер операції")
            if current_user == 'admin':
                operations = user_operations | cashier_operations
            else:
                operations = user_operations

            for key, value in operations.items():
                print(f"{key}.{value['title']}")

            choice = input("Ваший вибір: ")
            if choice in operations:
                operation = operations[choice]['operation']
                if operation not in (update_banknotes_quantity, view_banknotes_balance, display_atm_balance):
                    operation(current_user)
                else:
                    operation()

                if choice == '5' or not ask_user_to_continue("Бажаєте продовжити проводити операції з банкоматом? (1 - так / 0 - ні): "):
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
                current_user = login_user()
                if current_user:
                    atm_operations(current_user)
            elif choice == '2':
                register_and_login_user()
            elif choice == '3':
                break
            else:
                raise InvalidInputError("Ви зробили неправильний вибір, повторіть операцію")
        except InvalidInputError as error:
            print(error)


if __name__ == "__main__":
    start()