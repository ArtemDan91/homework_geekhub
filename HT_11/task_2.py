"""
Створити клас Person, в якому буде присутнім метод __init__ який буде приймати
якісь аргументи, які зберігатиме в відповідні змінні.
- Методи, які повинні бути в класі Person - show_age, print_name, show_all_information.
- Створіть 2 екземпляри класу Person та в кожному з екземплярів створіть атребут
profession (його не має інсувати під час ініціалізації).
"""


class Person:

    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.profession = None

    def show_age(self):
        print(f"The person is {self.age} years old")

    def print_name(self):
        print(f"The person`s name is {self.name}")

    def show_all_information(self):
        print(f"Person`s name: {self.name}, age: {self.age}, profession: {self.profession}")


if __name__ == "__main__":
    person_1 = Person('Jane', 25)
    person_1.profession = 'teacher'
    person_1.show_all_information()

    person_2 = Person('John', 20)
    person_2.profession = 'doctor'
    person_2.show_all_information()