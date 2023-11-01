"""
Написати функцію <fibonacci>, яка приймає один аргумент і виводить всі
числа Фібоначчі, що не перевищують його.
"""


class InvalidFibonacciNumberError(Exception):
    pass


def check_input_value(value_input):
    while True:

        try:
            number = int(value_input)
            if number <= 0:
                raise InvalidFibonacciNumberError("InvalidFibonacciNumberError: Введене число повинне бути більше 0")
            return number
        except ValueError:
            print("ValueError: Введене значення не є цілим числом.")
        except InvalidFibonacciNumberError as e:
            print(e)
            
        value_input = input("Спробуйте ще раз ввести дані: ")


def fibonacci(number):
    fibonacci_numbers = []
    num_1 = 0
    num_2 = 1

    while num_1 <= number:
        fibonacci_numbers.append(num_1)
        num_1, num_2 = num_2, num_1 + num_2

    return fibonacci_numbers


input_number = check_input_value(input("Введіть значення для знаходження чисел Фібоначчі: "))
print(fibonacci(input_number))