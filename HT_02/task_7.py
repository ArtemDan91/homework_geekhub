"""
Write a script to concatenate all elements in a list into a string and print it. 
List must be include both strings and integers and must be hardcoded.
"""

my_list = ["Hello", 1, "world", 2, False]
concatenate_string = ''.join([str(i) for i in my_list])

print(concatenate_string)