"""
Створіть функцію для валідації пари ім'я/пароль за наступними правилами:
   - ім'я повинно бути не меншим за 3 символа і не більшим за 50;
   - пароль повинен бути не меншим за 8 символів і повинен мати хоча б одну
   цифру;

   - якесь власне додаткове правило (заборона використання спецсимволів у імені, а
   пароль повинен мати хоча б 1 велику літеру, 1 малу та 1 спецсимвол) Дані правила внесені
   за рахунок оновлення паттерну для валідації імені та пароля.

   Якщо якийсь із параментів не відповідає вимогам - породити виключення із відповідним текстом.
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
        return "Валідація пари ім'я/пароль успішна"


if __name__ == "__main__":
    username = input("Введіть ім'я користувача: ")
    password = input("Введіть пароль: ")
    
    try:
        result = user_data_validation(username, password)
        print(result)
    except ValidationError as e:
        print(e)
