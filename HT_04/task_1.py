"""
Написати скрипт, який приймає від користувача два числа (int або float) і 
робить наступне:
a. Кожне введене значення спочатку пробує перевести в int. У разі помилки - 
пробує перевести в float, а якщо і там ловить помилку - пропонує ввести значення 
ще раз (зручніше на даному етапі навчання для цього використати цикл while)
b. Виводить результат ділення першого на друге. Якщо при цьому виникає помилка - 
оброблює її і виводить відповідне повідомлення
"""

while True:

    try:
        value_1 = input("Введіть перше число (int або float): ")
        try:
            number_1 = int(value_1)
        except ValueError:

            try:
                number_1 = float(value_1)
            except ValueError:
                print("ValueError: Введене значення не є числом. Повторіть спробу ще раз")
                continue

        valid_value_2 = False
        while not valid_value_2:
            value_2 = input("Введіть друге число (int або float): ")

            try:
                number_2 = int(value_2)
                valid_value_2 = True
            except ValueError:

                try:
                    number_2 = float(value_2)
                    valid_value_2 = True
                except ValueError:
                    print("ValueError: Введене значення не є числом. Повторіть спробу ще раз")
        
        result = number_1 / number_2

    except ZeroDivisionError:
        print("ZeroDivisionError: На нуль ділити не можна. Введіть дані повторно")
    except Exception as error:
        print(f"Невідома помилка при діленні одного числа на інше: {error}")
    
    else:
        print(f"Результат від ділення першого числа на друге: {result}")
        break