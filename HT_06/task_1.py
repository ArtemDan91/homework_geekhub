"""
Написати функцію <square>, яка прийматиме один аргумент - сторону квадрата, і вертатиме
3 значення у вигляді кортежа: периметр квадрата, площа квадрата та його діагональ.
"""

from math import sqrt


class InvalidSideSizeError(Exception):
    pass


def check_input_value(value_input):
    while True:

        try:
            side = int(value_input)
            if side <= 0:
                raise InvalidSideSizeError("InvalidSideSizeError: Введене число повинне бути більше 0")
            return side
        except ValueError:
            
            try:
                side = float(value_input)
                if side <= 0:
                    raise InvalidSideSizeError("InvalidSideSizeError: Введене число повинне бути більше 0")
                return side
            except ValueError:
                print("ValueError: Введене значення не є числом.")
                
        except InvalidSideSizeError as e:
            print(e)
            
        value_input = input("Спробуйте ще раз ввести дані для сторони квадрату (тип int або float): ")


def square(square_side):

    perimeter = 4 * square_side
    area = round(square_side ** 2, 2)
    diagonal = round((square_side * sqrt(2)), 2)

    return perimeter, area, diagonal
    

square_side = check_input_value(input("Введіть числове значення для сторони квадрату: "))
print(square(square_side))