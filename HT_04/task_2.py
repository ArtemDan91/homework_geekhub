"""
Create a custom exception class called NegativeValueError. Write a Python program
that takes an integer as input and raises the NegativeValueError if the input is
negative. Handle this custom exception with a try/except block and display an error message.
"""


class NegativeValueError(Exception):
    pass


try:
    number = int(input("Enter an integer: "))
    if number < 0:
        raise NegativeValueError("NegativeValueError: the number is negative")
    print(f"You entered positive number {number}")
except ValueError:
    print("ValueError: enter an integer")
except NegativeValueError as e:
    print(e)

