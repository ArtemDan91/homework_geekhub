"""
Наприклад маємо рядок --> "f98neroi4nr0c3n30irn03ien3c0rfe  kdno400wenwkowe00koijn35pijnp46ij7k5j78p3kj546p4 65jnpoj35po6j345" -> просто потицяв по клавi =)
   Створіть ф-цiю, яка буде отримувати рядки на зразок цього та яка оброблює наступні випадки:
-  якщо довжина рядка в діапазонi 30-50 (включно) -> прiнтує довжину рядка, кiлькiсть букв та цифр
-  якщо довжина менше 30 -> прiнтує суму всiх чисел та окремо рядок без цифр лише з буквами (без пробілів)
-  якщо довжина більше 50 -> щось вигадайте самі, проявіть фантазію 
        (НАПРИКЛАД, прінтує символ, який зустрічається найбільшу кількість разів та виводить цю кількість)
"""

import re
from collections import Counter


def text_processing(input_value):
    if 30 <= len(input_value) <= 50:
        letters = len(re.findall(r'[A-Za-z]', input_value))
        digits = len(re.findall(r'\d', input_value))
        
        print(f"Довжина рядка: {len(input_value)}, кількість букв: {letters}, кількість цифр: {digits}")
    
    elif len(input_value) < 30:
        sum_of_numbers = sum([int(elem) for elem in re.findall(r'\d+', input_value)])
        letters_string = ''.join(re.findall(r'[A-Za-z]', input_value))
        
        print(f"Сума всіх чисел: {sum_of_numbers}, рядок без цифр та пробілів: {letters_string}")
    
    else:
        text = input_value.replace(" ", "")
        char_count_dict = Counter(text)
        most_popular_char = max(char_count_dict, key=char_count_dict.get)
        max_char_count = char_count_dict[most_popular_char]

        print(f"Найбільшу кількість разів ({max_char_count}) зустрічається символ {most_popular_char}")


input_string = input("Напишіть приклад рядка для проведення обробки: ")
text_processing(input_string)