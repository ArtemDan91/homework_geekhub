"""
Write a script which accepts a <number> from user and then <number> times asks 
user for string input. At the end script must print out result of concatenating 
all <number> strings.
"""

number = int(input("Please, enter a number: "))
result = ''

if number <= 0:
    print("Sorry, please enter positive number")
else:
    for i in range(1, number + 1):
        string_input = input(f"Please, enter a string number {i}: ")
        result += string_input

    print(f"Result of concatenating all {number} strings is: {result}")