"""
Створiть 3 рiзних функцiї (на ваш вибiр). Кожна з цих функцiй повинна повертати
якийсь результат (напр. інпут від юзера, результат математичної операції тощо).
Також створiть четверту ф-цiю, яка всередині викликає 3 попереднi,
обробляє їх результат та також повертає результат своєї роботи. Таким чином ми
будемо викликати одну (четверту) функцiю, а вона в своєму тiлi - ще 3.
"""


def add_numbers(a, b):
    return a + b


def sub_numbers(a, b):
    return a - b


def mul_numbers(a, b):
    return a * b


def math_operations(a, b):
    add_result = add_numbers(a, b)
    sub_result = sub_numbers(a, b)
    mul_result = mul_numbers(a, b)

    return f"Результат операції додавання: {add_result}, віднімання: {sub_result}, множення: {mul_result}"


print(math_operations(1, 2))
