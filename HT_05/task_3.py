"""
Користувач вводить змiннi "x" та "y" з довiльними цифровими значеннями.
Створiть просту умовну конструкцiю (звiсно вона повинна бути в тiлi ф-цiї),
пiд час виконання якої буде перевiрятися рiвнiсть змiнних "x" та "y" та у випадку
нервіності - виводити ще і різницю.
    Повиннi опрацювати такi умови (x, y, z заміність на відповідні числа):
    x > y;       вiдповiдь - "х бiльше нiж у на z"
    x < y;       вiдповiдь - "у бiльше нiж х на z"
    x == y.      вiдповiдь - "х дорiвнює y"
"""


def check_equal(x, y):
    if x > y:
        z = x - y
        print(f'x більше ніж y на {z}')
    elif x < y:
        z = y - x
        print(f'y більше ніж x на {z}')
    else:
        print('x дорівнює y')


def get_valid_value(value_input):
    while True:
        try:
            number = int(value_input)
            return number
        except ValueError:
            try:
                number = float(value_input)
                return number
            except ValueError:
                print("ValueError: Введено не коректні дані")
                value_input = input("Спробуйте ще раз ввести дані для цієї змінної: ")


x = get_valid_value(input("Введіть числове значення для змінної x: "))
y = get_valid_value(input("Введіть числове значення для змінної y: "))

check_equal(x, y)