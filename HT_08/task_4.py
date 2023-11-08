"""
Реалізуйте генератор, який приймає на вхід будь-яку ітерабельну послідовність
(рядок, список, кортеж) і повертає генератор, який буде вертати значення з цієї послідовності,
при цьому, якщо було повернено останній елемент із послідовності - ітерація починається знову.
   Приклад (якщо запустили його у себе - натисніть Ctrl+C ;) ):
   for elem in generator([1, 2, 3]):
       print(elem)
   1
   2
   3
   1
   2
   3
   1
   .......
"""


class EmptyIterableSequenceError(Exception):
    pass


def generator(iterable_sequence):

    try:
        if not isinstance(iterable_sequence, (str, list, tuple)):
            raise TypeError("Генератор повинен приймати на вхід лише ітерабельну послідовність (рядок, список, кортеж)")

        if not iterable_sequence:
            raise EmptyIterableSequenceError("Послідовність повинна бути не пустою")

        while True:
            for elem in iterable_sequence:
                yield elem

    except (TypeError, EmptyIterableSequenceError) as e:
        print(e)


for elem in generator([1, 2, 3]):
    print(elem)
