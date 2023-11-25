def cash_out_with_min_bills(bills, total_amount, bill_counts):
    """
    Виконує видачу заданої суми грошей за допомогою мінімальної кількості банкнот, враховуючи їх обмежену кількість.

    Parameters
    ----------
    bills: list
        Список номіналів наявних банкнот
    total_amount: int
        Сума коштів, яку необхідно видати.
    bill_counts: list
        Кількість банкнот кожного номіналу

    Returns
    -------
    result: dict
        Повертає словник номіналів банкнот, необхідних для видачі заданої суми. При неможливості видати суму доступними у банкоматі номіналами - 
        повертає пустий словник
    """

    min_bills_list = [0] + [10**6] * total_amount
    """
    min_bills_list містить список, де кожен елемент показує мінімальну кількість банкнот, необхідну для видачі конкретної суми від 0 до total_amount.
    Кожному едементу списку призначаємо якесь велике значення 10**6, що показує, що мінімальна кількість банкнот ще не визначена.
    Проходячи циклом по total_amount - 10**6 буде перезаписуватися на мінімальну кількість банкнот, якщо ми можемо видати дану суму.
    Кількість банкнот для total_amount буде значенням min_bills_list[total_amount], якщо це значення буде дорівнювати 10**6 - то дану суму видати наявними банкнотами
    та їхньою кількістю - не можна.
    """

    used_bills = {current_amount: None for current_amount in range(total_amount + 1)}
    """
    used_bills - словник, де ключ - сума коштів, значення (спочатку None) - номінал банкноти, який був використаний для видачі даної суми.
    Якщо номінал банкноти використаний - далі переходимо до наступного ключа (новий ключ розраховується як різниця між поточним і сумою використаного номіналу) і т.д.
    """

    """
    Алгоритм полягає у перевірці кожного номіналу купюр по правилу: min_bills_list[amount] = min_bills_list[amount - bill] + 1, 
    де 1 - показує, що вже використали одну купюру даного номіналу. Далі проводимо розрахунку для суми amount - bill, враховуючи використані номінали.
    Із всих розрахунків для кожного номіналу - нам необхідно обрати мінімальне значення
    """

    # Обчислення мінімальної кількості банкнот для кожної можливої суми, враховуючи обмеженість банкнот у кількості
    for i, bill in enumerate(bills):
        for count in range(1, bill_counts[i] + 1):
            for amount in range(total_amount, -1, -1):

                # Перевірка 1: на можливість використання номіналу для видачі суми
                # Перевірка 2: чи кількість купюр, які ми використовуємо для amount - bill є меншою, ніж для amount
                if amount - bill >= 0 and min_bills_list[amount - bill] + 1 < min_bills_list[amount]:
                    # Оновлення мінімальної кількості банкнот для суми amount за умови використовуючи номіналу bill
                    min_bills_list[amount] = min_bills_list[amount - bill] + 1
                    # Включення у словник used_bills для даної суми коштів - за умови доцільності використання даної банкноти
                    used_bills[amount] = bill

    # Перевірка можливості видачі заданої суми
    if min_bills_list[total_amount] == 10**6:
        return {}
    else:
        # Побудова результату з використанням словника used_bills використаних банкнот
        result = {}

        while total_amount > 0:
            bill = used_bills[total_amount]
            result[bill] = result.get(bill, 0) + 1
            total_amount -= bill

        # for i, j in enumerate(min_bills_list):
        #     print(i, j)
        # print(used_bills)

        return result


if __name__ == "__main__":
    banknotes = [10, 20, 50, 200, 500, 1000]
    banknote_counts = [5, 1, 1, 4, 1, 5]
    cash_out_amount = 1170

    # banknotes = [20, 50, 100, 200]
    # banknote_counts = [6, 4, 1, 1]
    # cash_out_amount = 110

    # banknotes = [20, 50, 100]
    # banknote_counts = [10, 10, 10]
    # cash_out_amount = 160

  
    print(cash_out_with_min_bills(banknotes, cash_out_amount, banknote_counts))
