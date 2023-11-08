"""
Напишіть функцію,яка прймає рядок з декількох слів і повертає довжину 
найкоротшого слова. Реалізуйте обчислення за допомогою генератора.
"""


def shortest_word_length(input_string):
    return min(len(word) for word in input_string.split())


user_input = input("Введіть декілька слів через пробіл для визначення довжини найкоротшого: ")
print(shortest_word_length(user_input))
