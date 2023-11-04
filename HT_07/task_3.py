"""
На основі попередньої функції (скопіюйте кусок коду) створити наступний скрипт:
   а) створити список із парами ім'я/пароль різноманітних видів (орієнтуйтесь
   по правилам своєї функції) - як валідні, так і ні;
   б) створити цикл, який пройдеться по цьому циклу і, користуючись валідатором,
   перевірить ці дані і надрукує для кожної пари значень відповідне повідомлення, наприклад:
      Name: vasya
      Password: wasd
      Status: password must have at least one digit
      -----
      Name: vasya
      Password: vasyapupkin2000
      Status: OK
   P.S. Не забудьте використати блок try/except ;)
"""

import re


class ValidationError(Exception):
    pass


def user_data_validation(username, password):
    username_pattern = r'^[a-zA-Z0-9]{3,50}$'
    password_pattern = r'^(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[!@#$%&*?])[\dA-Za-z!@#$%&*?]{8,}$'

    username_errors = []
    password_errors = []

    if not re.match(username_pattern, username):
        username_errors.append("Ім'я має включати лише латинські літери, бути не меншим за 3 символа і не більшим за 50, забороняється використовувати спецсимволи!")

    if not re.match(password_pattern, password):
        password_errors.append("Пароль повинен мати хоча б одну цифру, одну велику літеру, одну маленьку та один спецсимвол!")
    
    if  username_errors or password_errors:
        raise ValidationError("; ".join(username_errors + password_errors))
    else:
        return "OK"


def main():
    users_data = [
        ("john", "JohnJohn77!!"),
        ("m@ry", "Mary12345!"),
        ("david!!!", "davidpass"),
        ("michael", "Michael1991?"),
        ("emma", "1234567"),
    ]

    for username, password in users_data:
        print(f"Name: {username}")
        print(f"Password: {password}")
        status = None

        try:
            status = user_data_validation(username, password)
        except ValidationError as e:
            status = e
        
        print(f"Status: {status}")
        print("-----")


if __name__ == "__main__":
    main()

