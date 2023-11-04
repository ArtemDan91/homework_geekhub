"""
Створіть функцію, всередині якої будуть записано список із п'яти користувачів
(ім'я та пароль). Функція повинна приймати три аргументи: два - обов'язкових
(<username> та <password>) і третій - необов'язковий параметр <silent>
(значення за замовчуванням - <False>).
Логіка наступна:
    якщо введено коректну пару ім'я/пароль - вертається True;
    якщо введено неправильну пару ім'я/пароль:
        якщо silent == True - функція вертає False
        якщо silent == False -породжується виключення LoginException (його також треба створити =))
"""


class LoginException(Exception):
    pass


def user_authentication(username, password, silent=False):
    users = [
        {"username": "john", "password": "johnjohn77"},
        {"username": "mary", "password": "mary12345"},
        {"username": "david", "password": "davidpass"},
        {"username": "michael", "password": "1234qwer"},
        {"username": "emma", "password": "1234567"},
    ]

    for user in users:
        if username == user["username"] and password == user["password"]:
            return True

    if silent:
        return False
    else:
        raise LoginException("LoginException: Введено неправильну пару ім'я/пароль")


if __name__ == "__main__":
    username = input("Введіть ім'я користувача: ")
    password = input("Введіть пароль: ")

    try:
        result = user_authentication(username, password)
        print(result)
    except LoginException as e:
        print(e)