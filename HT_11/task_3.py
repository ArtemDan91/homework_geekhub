"""
 Банкомат 2.0: переробіть программу з функціонального підходу програмування на використання 
 класів. Додайте шанс 10% отримати бонус на баланс (ДОДАВ бонус із ймовірністю 10% - 
 у розмірі 100 грн. при реєстрації нового користувача та 5 відсотків від суми поповнення рахунку).
"""

import sqlite3
import re
import json
import random
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


class DataBaseManager:
    
    def __init__(self, database_path=parent_dir / 'atm_database.db'):
        self.database_path = database_path
        self.conn = None
        self.cur = None

    def connect_to_database(self):
        try:
            self.conn = sqlite3.connect(self.database_path)
            self.cur = self.conn.cursor()
            return self.conn, self.cur
        except sqlite3.Error as e:
            raise e
    
    def close_database_connection(self):
        try:
            if self.conn:
                self.conn.close()
        except sqlite3.Error as e:
            print(f"Помилка при роботі з SQLite: {e}")

    def create_tables(self):
        try:
            self.connect_to_database()
            if self.conn:
                self.cur.executescript('''
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
                self.conn.commit()
        except sqlite3.Error as e:
            print(f"Помилка при роботі з SQLite: {e}")
        finally:
            self.close_database_connection()

    def register_atm_cashier(self):
        try:
            self.connect_to_database()
            if self.conn:
                self.cur.execute('INSERT INTO users (username, password, is_cashier) VALUES (?, ?, ?)', ('admin', 'admin', True))
                user_id = self.cur.lastrowid
                self.cur.execute("INSERT INTO user_balance (user_id, username, balance) VALUES (?, 'admin', 0)", (user_id,))
                self.conn.commit()
        except sqlite3.Error as e:
            print(f"Помилка при роботі з SQLite: {e}")
        finally:
            self.close_database_connection()

    def insert_atm_banknotes(self):
        denominations = [10, 20, 50, 100, 200, 500, 1000]
    
        try:
            self.connect_to_database()
            if self.conn:
                self.cur.execute('INSERT INTO atm (balance) VALUES (0)')
                atm_id = self.cur.lastrowid

                if atm_id is not None:
                    for denomination in denominations:
                        self.cur.execute('INSERT INTO atm_banknotes (denomination, count, atm_id) VALUES (?, 0, ?)', (denomination, atm_id))
                    self.conn.commit()
                    print("Дані для номіналів додано успішно.")
        except sqlite3.Error as e:
            print(f"Помилка при роботі з SQLite: {e}")
        finally:
            self.close_database_connection()


class UserValidation:

    @staticmethod
    def username_input_validation():
        username = input("Введіть ім'я користувача: ")
        username_pattern = r'^[a-zA-Z0-9]{3,50}$'
        if not re.match(username_pattern, username):
            raise UsernameValidationError("Ім'я має включати лише латинські літери, бути не меншим за 3 символа і не більшим за 50, забороняється використовувати спецсимволи!")
        return username

    @staticmethod
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


class UserManager(DataBaseManager, UserValidation):
    
    def __init__(self):
        super().__init__()

    def check_user_exists(self, username):
        try:
            self.connect_to_database()
            if self.conn:
                check_user = self.cur.execute('SELECT * FROM users WHERE username=?', (username,)).fetchone()
                if check_user and check_user[1] == username:
                    return True
                return False
        except sqlite3.Error as e:
            print(f"Помилка при роботі з SQLite: {e}")
        finally:
            self.close_database_connection()

    def register_new_user(self):
        while True:
            try:
                username = self.username_input_validation()

                if self.check_user_exists(username):
                    print("Користувач з даним ім'ям вже існує, придумайте нове ім'я")
                    continue

                password = self.password_input_validation()
                try:
                    self.connect_to_database()
                    if self.conn:

                        if random.random() <= 0.1:
                            bonus = 100
                            print(f"Вітаємо, ви отримали бонус 'Новий користувач' у розмірі 100 грн. на ваший рахунок!")
                        else:
                            bonus = 0

                        self.cur.execute('INSERT INTO users (username, password, is_cashier) VALUES (?, ?, ?)', (username, password, False))
                        user_id = self.cur.lastrowid
                        self.cur.execute('INSERT INTO user_balance (user_id, username, balance) VALUES (?, ?, ?)', (user_id, username, bonus))

                        self.conn.commit()
                except sqlite3.Error as e:
                    print(f"Помилка при роботі з SQLite: {e}")
                finally:
                    self.close_database_connection()

                print("Дані успішно додані. Тепер ви можете увійти у ваший обліковий запис")
                return username

            except (UsernameValidationError, PasswordValidationError, MaxAttemptsPassInputError) as error:
                print(error)

    def register_and_login_user(self):
        user_manager_instance = UserManager()
        atm_operations_instance = ATMOperations(user_manager_instance)

        while True:
            current_user = self.register_new_user()
            if current_user:
                print("Бажаєте увійти? (1 - так / 0 - ні): ")
                choice = input()
                if choice == '1':
                    atm_operations_instance.atm_operations(current_user)
                    break
                elif choice == '0':
                    print(f"До наступної зустрічі!")
                    break
                else:
                    print("Ви зробили неправильний вибір, повторіть операцію")

    def login_user(self):
        while True:
            try:
                username = input("Введіть ім'я користувача: ")
                password = input("Введіть пароль: ")
                self.connect_to_database()
                if self.conn:
                    user = self.cur.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()
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
                self.close_database_connection()


class ATMOperations:

    def __init__(self, user_manager):
        self.user_manager = user_manager

    def display_user_balance(self, current_user):
        try:
            self.user_manager.connect_to_database()
            if self.user_manager.conn:
                user_data = self.user_manager.cur.execute('SELECT balance FROM user_balance WHERE username = ?', (current_user,)).fetchone()
                print(f"Баланс користувача {current_user} складає: {user_data[0]} грн.")
        except sqlite3.Error as e:
            print(f"Помилка при роботі з SQLite: {e}")
        finally:
            self.user_manager.close_database_connection()

    @staticmethod
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

    def update_transactions_file(self, current_user, operation, amount):
        transaction_details = {
            "type": operation,
            "amount": amount,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        transaction_details_json = json.dumps(transaction_details, default=str)
        try:
            self.user_manager.connect_to_database()
            if self.user_manager.conn:
                user_id = self.user_manager.cur.execute('SELECT user_id FROM users WHERE username = ?', (current_user,)).fetchone()[0]
                self.user_manager.cur.execute('INSERT INTO user_transactions (user_id, username, transaction_details) VALUES (?, ?, ?)', (user_id, current_user, transaction_details_json))
                self.user_manager.conn.commit()

        except sqlite3.Error as e:
            print(f"Помилка при роботі з SQLite: {e}")
        finally:
            self.user_manager.close_database_connection()

    def make_deposit(self, current_user):
        try:
            input_value = input("Введіть суму для поповнення: ")
            amount = self.check_input_value(input_value)

            self.user_manager.connect_to_database()
            if self.user_manager.conn:
                atm_id = self.user_manager.cur.execute('SELECT atm_id, balance FROM atm').fetchone()[0]
                min_denomination = self.user_manager.cur.execute('SELECT MIN(denomination) from atm_banknotes WHERE atm_id = ?', (atm_id,)).fetchone()[0]

                deposit_amount = amount - amount % min_denomination

                if random.random() <= 0.1:
                    bonus = int(0.05 * deposit_amount)
                    print(f"Вітаємо, ви отримали бонус '5% від суми поповнення' на ваший рахунок!")
                else:
                    bonus = 0

                deposit_amount += bonus
                self.user_manager.cur.execute('UPDATE user_balance SET balance = balance + ? WHERE username = ?', (deposit_amount, current_user))
                self.user_manager.conn.commit()
                self.update_transactions_file(current_user, 'deposit',deposit_amount)

                print(f"Баланс користувача {current_user} поповнено на {deposit_amount} грн..")
                if amount % min_denomination != 0:
                    print(f"Решта від виконання операції: {amount - deposit_amount}")
        except NegativeInputAmountError as error:
            print(error)
        except sqlite3.Error as e:
            print(f"Помилка при роботі з SQLite: {e}")
        finally:
            self.user_manager.close_database_connection()

    @staticmethod
    def is_cash_out_posible(amount, denominations):
        for denomination, count in denominations:
            if amount % denomination == 0 and count > 0:
                return True
        return False

    def cash_out(self, current_user):
        try:
            input_value = input("Введіть суму для зняття: ")
            amount = self.check_input_value(input_value)

            self.user_manager.connect_to_database()
            if self.user_manager.conn:
                current_atm_balance = \
                self.user_manager.cur.execute('SELECT balance FROM atm').fetchone()[0]
                if amount > current_atm_balance:
                    raise NegativeAtmBalanceError("Недостатньо коштів у банкоматі для видачі суми.")

                current_user_balance = self.user_manager.cur.execute('SELECT balance FROM user_balance WHERE username = ?', (current_user,)).fetchone()[0]
                if amount > current_user_balance:
                    raise NegativeUserBalanceError("Недостатньо коштів на рахунку для видачі суми.")

                atm_denominations = self.user_manager.cur.execute('SELECT denomination, count FROM atm_banknotes').fetchall()
                atm_available_denominations = [item[0] for item in atm_denominations if item[1] > 0]
                if self.is_cash_out_posible(amount, atm_denominations):
                    self.user_manager.cur.execute('UPDATE user_balance SET balance = balance - ? WHERE username = ?', (amount, current_user))
                    self.user_manager.conn.commit()
                    print(f"Знято {amount} грн. з рахунку {current_user}.")
                else:
                    raise WithdrawalNotPossibleError(f"Операція знаття не доступна, вкажіть суму, враховуючи доступні номінали: {atm_available_denominations}")

                self.update_transactions_file(current_user, 'cash_out', amount)

        except (NegativeInputAmountError, NegativeAtmBalanceError, NegativeUserBalanceError, WithdrawalNotPossibleError) as error:
            print(error)
        except sqlite3.Error as e:
            print(f"Помилка при роботі з SQLite: {e}")
        finally:
            self.user_manager.close_database_connection()

    def view_transactions(self, current_user):
        try:
            self.user_manager.connect_to_database()
            if self.user_manager.conn:
                user_transactions = self.user_manager.cur.execute('SELECT transaction_details FROM user_transactions WHERE username = ?', (current_user,)).fetchall()
                for transaction in user_transactions:
                    print(transaction)
        except sqlite3.Error as e:
            print(f"Помилка при роботі з SQLite: {e}")
        finally:
            self.user_manager.close_database_connection()

    def exit_operation(self, current_user):
        print(f"До наступної зустрічі, {current_user}!")

    def display_atm_balance(self):
        try:
            self.user_manager.connect_to_database()
            if self.user_manager.conn:
                atm_balance = self.user_manager.cur.execute('SELECT balance FROM atm').fetchone()
                print(f"Доступний залишок в банкоматі: {atm_balance[0]} грн.")
        except sqlite3.Error as e:
            print(f"Помилка при роботі з SQLite: {e}")
        finally:
            self.user_manager.close_database_connection()

    def view_banknotes_balance(self):
        try:
            self.user_manager.connect_to_database()
            if self.user_manager.conn:
                atm_banknotes = self.user_manager.cur.execute('SELECT denomination, count FROM atm_banknotes').fetchall()

                print("Залишок купюр в банкоматі:")
                for num, row in enumerate(atm_banknotes, 1):
                    print(
                        f"{num}. Номінал: {row[0]} грн., кількість: {row[1]} шт.")

        except sqlite3.Error as e:
            print(f"Помилка при роботі з SQLite: {e}")
        finally:
            self.user_manager.close_database_connection()

    @staticmethod
    def ask_user_to_continue(message):
        while True:
            user_input = input(message)
            if user_input == '1':
                return True
            elif user_input == '0':
                return False
            else:
                print("Невірна відповідь. Спробуйте ще раз.")

    def update_banknotes_quantity(self):
        print("Доступні номінали: 10, 20, 50, 100, 200, 500, 1000")
        while True:
            try:
                denomination = int(input("Введіть номінал банкноти: "))
                if denomination not in [10, 20, 50, 100, 200, 500, 1000]:
                    raise InvalidDenominationError("Обраний невірний номінал купюри")

                change_quantity = int(input(
                    "Введіть зміну кількості купюр (значення з '-' зменшить кількість): "))

                self.user_manager.connect_to_database()
                if self.user_manager.conn:
                    current_quantity = self.user_manager.cur.execute('SELECT count FROM atm_banknotes WHERE denomination = ?', (denomination,)).fetchone()
                    result = current_quantity[0] + change_quantity
                    if result < 0:
                        raise NegativeBanknotesQuantityError("Кількість банкнот не може бути від'ємним числом")

                    self.user_manager.cur.execute('UPDATE atm_banknotes SET count = ? WHERE denomination = ?', (result, denomination))
                    self.user_manager.conn.commit()
                    new_balance = self.user_manager.cur.execute('SELECT SUM(denomination * count) AS atm_balance FROM atm_banknotes').fetchone()[0]
                    self.user_manager.cur.execute("UPDATE atm SET balance = ?", (new_balance,))
                    self.user_manager.conn.commit()
                    print("Дані у таблиці успішно внесені.")

                    if not self.ask_user_to_continue("Бажаєте продовжити вносити зміни у кількість доступних курюр? (1 - так / 0 - ні): "):
                        break

            except sqlite3.Error as e:
                print(f"Помилка при роботі з SQLite: {e}")
            except ValueError:
                print("Введене значення повинне бути цілим числом")
            except (
            InvalidDenominationError, NegativeBanknotesQuantityError) as e:
                print(e)
            finally:
                self.user_manager.close_database_connection()

    def atm_operations(self, current_user):
        user_operations = {
            '1': {'title': 'Переглянути баланс рахунку', 'operation': self.display_user_balance},
            '2': {'title': 'Поповнити баланс рахунку', 'operation': self.make_deposit},
            '3': {'title': 'Зняти кошти з рахунку', 'operation': self.cash_out},
            '4': {'title': 'Переглянути транзакції по рахунку', 'operation': self.view_transactions},
            '5': {'title': 'Вихід', 'operation': self.exit_operation},
        }
        cashier_operations = {
            '6': {'title': 'Переглянути баланс банкомату', 'operation': self.display_atm_balance},
            '7': {'title': 'Переглянути залишок купюр в банкоматі', 'operation': self.view_banknotes_balance},
            '8': {'title': 'Змінити кількість купюр', 'operation': self.update_banknotes_quantity},
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
                    if operation not in (self.update_banknotes_quantity, self.view_banknotes_balance, self.display_atm_balance):
                        operation(current_user)
                    else:
                        operation()

                    if choice == '5' or not self.ask_user_to_continue("Бажаєте продовжити проводити операції з банкоматом? (1 - так / 0 - ні): "):
                        break

                else:
                    raise InvalidInputError(
                        "Ви зробили неправильний вибір, повторіть операцію")
            except InvalidInputError as error:
                print(error)

    def start(self):
        while True:
            try:
                print(
                    "Оберіть цифру із запропонованих для вибору необхідних дій: ")
                print("1. Увійти")
                print("2. Зареєструватися")
                print("3. Вихід")

                choice = input("Ваший вибір: ")
                if choice == '1':
                    current_user = self.user_manager.login_user()
                    if current_user:
                        self.atm_operations(current_user)
                elif choice == '2':
                    self.user_manager.register_and_login_user()
                elif choice == '3':
                    break
                else:
                    raise InvalidInputError("Ви зробили неправильний вибір, повторіть операцію")
            except InvalidInputError as error:
                print(error)


if __name__ == "__main__":
    usermanager = UserManager()
    atm_operations = ATMOperations(usermanager)
    atm_operations.start()