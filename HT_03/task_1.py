"""
Write a script that will run through a list of tuples and replace the last value 
for each tuple. The list of tuples can be hardcoded. The "replacement" value is 
entered by user. The number of elements in the tuples must be different.
"""

list_of_tuples = [(1, 2, 3), (4, 5, 6, 7), (8, 9, 10, 11, 12)]
replacement_value = input("Enter the replacement value: ")

print([i[:-1] + (replacement_value,) for i in list_of_tuples])


# через обробку вводу користувача
# list_of_tuples = [(1, 2, 3), (4, 5, 6, 7), (8, 9, 10, 11, 12)]
# replacement_value = input("Please, enter an integer: ")

# try:
#     replacement_value = int(replacement_value)
#     print([i[:-1] + (replacement_value,) for i in list_of_tuples])

# except ValueError:
#     print("Please, enter a valid replacement value.")