"""
Написати функцію <prime_list>, яка прийматиме 2 аргументи - початок і кінець діапазона,
і вертатиме список простих чисел всередині цього діапазона. Не забудьте про перевірку
на валідність введених даних та у випадку невідповідності - виведіть повідомлення.
"""


def check_input_value(value_input):
    while True:
        try:
            number = int(value_input)
            return number
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



def prime_list(start, end):
    if start > end:
        print("Значення початку діапазону чисел повинне бути меншим за значення кінця діапазону.")
        return f"Cписок простих чисел всередині визначеного діапазону чисел: {[]}"

    prime_numbers_list = []
    for number in range(start, end + 1):
        if is_prime(number):
            prime_numbers_list.append(number)

    if not prime_numbers_list:
        print("У заданому діапазоні немає простих чисел")

    return f"Cписок простих чисел всередині визначеного діапазону чисел: {prime_numbers_list}"


start = check_input_value(input("Введіть значення для початку діапазону чисел: "))
end = check_input_value(input("Введіть значення для кінця діапазону чисел: "))

print(prime_list(start, end))
