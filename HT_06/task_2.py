"""
Написати функцію <bank>, яка працює за наступною логікою: користувач робить
вклад у розмірі <a> одиниць строком на <years> років під <percents> відсотків
(кожен рік сума вкладу збільшується на цей відсоток, ці гроші додаються до суми
вкладу і в наступному році на них також нараховуються відсотки). Параметр <percents>
є необов'язковим і має значення по замовчуванню <10> (10%). Функція повинна
принтануть суму, яка буде на рахунку, а також її повернути (але округлену до копійок).
"""


class InvalidValueError(Exception):
    pass


def is_valid_value(value, error_massage, types):
    if not (isinstance(value, types) and value >= 0):
        raise InvalidValueError(error_massage)


def bank(a, years, percents=10):
    try:
        is_valid_value(a, "Сума вкладу має бути додатнім числом", (int, float))
        is_valid_value(years, "Кількість років має бути цілим додатнім числом", int)
        is_valid_value(percents, "Сума відсотків має бути додатнім числом", (int, float))

        for year in range(years):
            a += a * percents / 100

    except InvalidValueError as e:
        return e
    except Exception as e:
        return f"Невідома помилка при виконанні операції: {e}"
    else:
        print(f"Сума депозиту через {years} роки(-ів) становитиме {a:.2f} одиниць")
        return round(a, 2)


print(bank(5000, 3, percents=11.5))