"""
Написати функцию <is_prime>, яка прийматиме 1 аргумент - число від 0 до 1000,
и яка вертатиме True, якщо це число просте і False - якщо ні.
"""


class InvalidInputError(Exception):
    pass


def check_input_value(value_input):
    while True:
        try:
            number = int(value_input)
            if not (0 <= number <= 1000):
                raise InvalidInputError("InvalidInputError: Введене число не відповідає умові (від 0 до 1000)")
            return number
        except InvalidInputError as e:
            print(e)
        except ValueError:
            print("ValueError: Введене значення повинно бути цілим числом")

        value_input = input("Спробуйте ще раз ввести значення для числа: ")


def is_prime(number):
    if number <= 1:
        return False
    divisor = 2
    while divisor < number:
        if number % divisor == 0:
            return False
        divisor += 1
    return True


input_number = check_input_value(input("Введіть число у діапазоні від 0 до 1000: "))
print(is_prime(input_number))
