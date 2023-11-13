"""
Програма-світлофор.
   Створити програму-емулятор світлофора для авто і пішоходів. Після запуска
   програми на екран виводиться в лівій половині - колір автомобільного, а в правій -
   пішохідного світлофора. Кожну 1 секунду виводиться поточні кольори. Через декілька
   ітерацій - відбувається зміна кольорів - логіка така сама як і в звичайних
   світлофорах (пішоходам зелений тільки коли автомобілям червоний).
   Приблизний результат роботи наступний:
      Red        Green
      Red        Green
      Red        Green
      Red        Green
      Yellow     Red
      Yellow     Red
      Green      Red
      Green      Red
      Green      Red
      Green      Red
      Yellow     Red
      Yellow     Red
      Red        Green
"""

import time


def car_color_generator():
    color_counts = [
        {"color": "Red", "count": 4},
        {"color": "Yellow", "count": 2},
        {"color": "Green", "count": 4},
        {"color": "Yellow", "count": 2}
    ]

    while True:
        for color_count in color_counts:
            for i in range(color_count["count"]):
                yield color_count["color"]


def traffic_light_simulator():
    car_color_iter = car_color_generator()

    while True:
        car_color = next(car_color_iter)
        pedestrian_color = "Green" if car_color == "Red" else "Red"

        print(f"{car_color:^7}{pedestrian_color:^7}")
        time.sleep(1)


if __name__ == "__main__":
    traffic_light_simulator()