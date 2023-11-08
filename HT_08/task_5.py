"""
Напишіть функцію,яка приймає на вхід рядок та повертає кількість окремих
регістро-незалежних букв та цифр, які зустрічаються в рядку більше ніж 1 раз.
Рядок буде складатися лише з цифр та букв (великих і малих). Реалізуйте
обчислення за допомогою генератора.
    Example (input string -> result):
    "abcde" -> 0            # немає символів, що повторюються
    "aabbcde" -> 2          # 'a' та 'b'
    "aabBcde" -> 2          # 'a' присутнє двічі і 'b' двічі (`b` та `B`)
    "indivisibility" -> 1   # 'i' присутнє 6 разів
    "Indivisibilities" -> 2 # 'i' присутнє 7 разів та 's' двічі
    "aA11" -> 2             # 'a' і '1'
    "ABBA" -> 2             # 'A' і 'B' кожна двічі
"""

from collections import Counter


def count_repeating_chars(input_string):
    chars_count_dict = Counter(input_string.lower())
    
    return sum(1 for value in chars_count_dict.values() if value > 1)


print(count_repeating_chars("aabBcde"))