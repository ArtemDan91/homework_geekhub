"""
Створити клас Calc, який буде мати атребут last_result та 4 методи. Методи повинні
виконувати математичні операції з 2-ма числами, а саме додавання, віднімання, множення, ділення.
- Якщо під час створення екземпляру класу звернутися до атребута last_result
він повинен повернути пусте значення.
- Якщо використати один з методів - last_result повенен повернути
результат виконання ПОПЕРЕДНЬОГО методу.
    Example:
    last_result --> None
    1 + 1
    last_result --> None
    2 * 3
    last_result --> 2
    3 * 4
    last_result --> 6
    ...
"""


class Calc:
    """
    Клас для виконання математичних операцій з 2-ма числами та повернення результату виконання попереднього методу.

    Attributes
    ----------
    last_result int | float | None
        Зберігає останній результат обчислення. Ініціалізується значенням None

    Methods
    -------
    __init__():
        Ініціалізує об'єкт класу Calc з атрибутом last_result зі значенням None
    add(a: int | float, b: int | float) -> int | float:
        Виконує операцію додавання двох чисел a та b.
    sub(a: int | float, b: int | float) -> int | float:
        Виконує операцію віднімання числа b від числа а.
    mul(a: int | float, b: int | float) -> int | float:
        Виконує операцію множення числа a на число b.
    div(a: int | float, b: int | float) -> int | float | None:
        Виконує операцію ділення числа a на число b. При діленні на нуль виводить помилку

    """

    def __init__(self):
        """
        Parameters
        ----------
        last_result: None
            Зберігає останній результат обчислення. Ініціалізується значенням None
        """
        self.last_result = None

    def add(self, a, b):
        """
        Виконує операцію додавання двох чисел a та b

        Parameters
        ----------
        a: int | float
            Перше число
        b: int | float
            Друге число

        Returns
        -------
        result: int | float
            Повертає результат виконання операції додавання двох чисел a та b
        """
        result = a + b
        print(f"{a} + {b}\nlast_result --> {self.last_result}")
        self.last_result = result
        return result

    def sub(self, a, b):
        """
        Виконує операцію віднімання числа b від числа а

        Parameters
        ----------
        a: int | float
            Перше число
        b: int | float
            Друге число

        Returns
        -------
        result: int | float
            Повертає результат виконання операції віднімання числа b від числа а
        """
        result = a - b
        print(f"{a} - {b}\nlast_result --> {self.last_result}")
        self.last_result = result
        return result

    def mul(self, a, b):
        """
        Виконує операцію множення числа a на число b

        Parameters
        ----------
        a: int | float
            Перше число
        b: int | float
            Друге число

        Returns
        -------
        result: int | float
            Повертає результат виконання операції множення числа a на число b
        """
        result = a * b
        print(f"{a} * {b}\nlast_result --> {self.last_result}")
        self.last_result = result
        return result

    def div(self, a, b):
        """
        Виконує операцію ділення числа a на число b. При діленні на нуль виводить помилку

        Parameters
        ----------
        a: int | float
            Перше число
        b: int | float
            Друге число

        Raises
        ------
        ZeroDivisionError
            Виникає помилка при виконанні операції ділення на нуль

        Returns
        -------
        result: int | float
            Повертає результат виконання операції ділення числа a на число b
        """
        try:
            result = a / b
            print(f"{a} / {b}\nlast_result --> {self.last_result}")
            self.last_result = result
            return result
        except ZeroDivisionError:
            print("На нуль ділити не можна")


if __name__ == "__main__":
    calc = Calc()
    print(f"last_result --> {calc.last_result}")
    calc.div(1, 1)
    calc.add(2, 3)
    calc.mul(3, 4)
    calc.sub(10, 4)






