"""
Написати функцію, яка буде реалізувати логіку циклічного зсуву елементів в списку.
Тобто функція приймає два аргументи: список і величину зсуву (якщо ця величина
додатня - пересуваємо з кінця на початок, якщо від'ємна - навпаки - пересуваємо
елементи з початку списку в його кінець).
   Наприклад:
   fnc([1, 2, 3, 4, 5], shift=1) --> [5, 1, 2, 3, 4]
   fnc([1, 2, 3, 4, 5], shift=-2) --> [3, 4, 5, 1, 2]
"""

def cyclic_shift(my_list, shift=0):
    if not my_list:
        return my_list

    shift = shift % len(my_list)
    if shift == 0:
        return my_list

    if shift < 0:
        return my_list[shift:] + my_list[:shift]
    else:
        return my_list[-shift:] + my_list[:-shift]


print(cyclic_shift([1, 2, 3, 4, 5], shift=1))