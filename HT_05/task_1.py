"""
Написати функцiю season, яка приймає один аргумент (номер мiсяця вiд 1 до 12) та яка
буде повертати пору року, якiй цей мiсяць належить (зима, весна, лiто або осiнь).
У випадку некоректного введеного значення - виводити відповідне повідомлення.
"""


def season(number):
    month_to_season = {
        (12, 1, 2): "зима",
        (3, 4, 5): "весна",
        (6, 7, 8): "літо",
        (9, 10, 11): "осінь"
    }

    try:
        if not (isinstance(number, int) and 1 <= number <= 12):
            raise ValueError("ValueError: не коректне значення для номеру місяця, введіть ціле число від 1 до 12")
        for key, value in month_to_season.items():
            if number in key:
                return value

    except ValueError as e:
        return e


print(season(4))