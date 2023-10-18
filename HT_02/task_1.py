"""
Write a script which accepts a sequence of comma-separated numbers from 
user and generate a list and a tuple with those numbers.
"""

numbers = input("Write a sequence of comma-separated numbers: ")
numbers_list = [int(i) for i in numbers.replace(" ", "").split(",")]
numbers_tuple = tuple(numbers_list)
print(numbers_list, numbers_tuple, sep='\n')