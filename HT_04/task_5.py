"""
Create a Python program that repeatedly prompts the user for a number until
a valid integer is provided. Use a try/except block to handle any ValueError
exceptions, and keep asking for input until a valid integer is entered.
Display the final valid integer.
"""

valid_value = False
while not valid_value:
    input_value = input("Enter an integer: ")

    try:
        number = int(input_value)
        print(f"You entered valid integer: {number}")
        valid_value = True
    except ValueError:
        print("ValueError: invalid input value, enter an integer")