""""
Write a script which accepts a <number> from user and print out a sum 
of the first <number> positive integers.
"""

number = int(input("Enter a number: "))
sum_of_integers = 0

if number <= 0:
    print("Sorry, please enter positive number")
else:
    for i in range(1, number + 1):
        sum_of_integers += i

    print(f"Sum of the first {number} positive integers is {sum_of_integers}")