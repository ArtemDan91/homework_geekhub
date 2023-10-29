"""
Ну і традиційно - калькулятор :slightly_smiling_face: Повинна бути 1 ф-цiя, яка б
приймала 3 аргументи - один з яких операцiя, яку зробити! Аргументи брати від юзера
(можна по одному - 2, окремо +, окремо 2; можна всі разом - типу 1 + 2).
Операції що мають бути присутні: +, -, *, /, %, //, **. Не забудьте протестувати
з різними значеннями на предмет помилок!
"""


def calculator(value_1, operation, value_2):
    operations = {
        '+': lambda a, b: a + b,
        '-': lambda a, b: a - b,
        '*': lambda a, b: a * b,
        '/': lambda a, b: a / b,
        '%': lambda a, b: a % b,
        '//': lambda a, b: a // b,
        '**': lambda a, b: a ** b,
    }
    result = None
    
    try:
        num_1 = None
        num_2 = None

        try:
            num_1 = int(value_1)
        except ValueError:
            try:
                num_1 = float(value_1)
            except ValueError:
                print(f"ValueError: Введено не коректні дані для першого числа.")

        try:
            num_2 = int(value_2)
        except ValueError:
            try:
                num_2 = float(value_2)
            except ValueError:
                print(f"ValueError: Введено не коректні дані для другого числа.")

        if num_1 is not None and num_2 is not None:
            if operation not in operations:
                raise KeyError(f"KeyError: Операція '{operation}' не підтримується калькулятором.")
            else:
                result = operations[operation](num_1, num_2)

    except ZeroDivisionError:
        print("ZeroDivisionError: На нуль ділити не можна.")
    except KeyError as e:
        print(e)
    except Exception as error:
        print(f"Невідома помилка при виконанні операції: {error}")
    else:
        if result is not None:
            print(f"Результат виконання операції: {result}")


while True:
    number_1 = input("Введіть перше число: ")
    operation = input("Введіть операційю із (+, -, *, /, %, //, **): ")
    number_2 = input("Введіть друге число: ")

    calculator(number_1, operation, number_2)

    try_again = input("Бажаєте виконати ще одну операцію? (Так/Ні): ")
    if try_again.lower() != "так":
        break