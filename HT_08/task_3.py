"""
Всі ви знаєте таку функцію як <range>. Напишіть свою реалізацію цієї функції.
Тобто щоб її можна було використати у вигляді:
    for i in my_range(1, 10, 2):
        print(i)
    1
    3
    5
    7
    9
   P.S. Повинен вертатись генератор.
   P.P.S. Для повного розуміння цієї функції - можна почитати документацію по
   ній: https://docs.python.org/3/library/stdtypes.html#range
   P.P.P.S Не забудьте обробляти невалідні ситуації (аналог range(1, -10, 5)).
   Подивіться як веде себе стандартний range в таких випадках.
"""


def user_range(start, stop=None, step=1):
    try:
        if not isinstance(start, int):
            raise TypeError("Значення аргументу start повинне бути цілим числом")
        if stop is not None and not isinstance(stop, int):
            raise TypeError("Значення аргументу stop повинне бути цілим числом")
        if not isinstance(step, int):
            raise TypeError("Значення аргументу step повинне бути цілим числом")
        if step == 0:
            raise ValueError("Значення аргументу step не може дорівнювати 0")
    
        if stop is None:
            stop = start
            start = 0

        if (start > stop and step > 0) or (start < stop and step < 0):
            for elem in []:
                yield elem
        else:
            if step > 0:
                while start < stop:
                    yield start
                    start += step
            else:
                while start > stop:
                    yield start
                    start += step

    except (TypeError, ValueError) as e:
        print(e)

    
for i in user_range(1, 10, 2):
    print(i)
