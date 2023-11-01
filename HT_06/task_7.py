"""
Написати функцію, яка приймає на вхід список (через кому), підраховує кількість
однакових елементів у ньомy і виводить результат. Елементами списку можуть бути
дані будь-яких типів.
    Наприклад:
    1, 1, 'foo', [1, 2], True, 'foo', 1, [1, 2] ----> "1 -> 3, foo -> 2,
    [1, 2] -> 2, True -> 1"
"""

from collections import Counter


def convert_to_str(element):
    if isinstance(element, (list, dict, set, bool)):
        return str(element)
    return element


def list_elements_count(my_list):
    counter_dict = Counter([convert_to_str(elem) for elem in my_list])
    counter_list = []

    for elem, count in counter_dict.items():
        counter_list.append(f"{elem} -> {count}")

    print(", ".join(counter_list))


list_elements_count([1, 1, 'foo', [1, 2], True, 'foo', 1, [1, 2]])
