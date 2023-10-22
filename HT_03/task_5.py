"""
Write a script to remove values duplicates from dictionary. Feel free to 
hardcode your dictionary.
"""

my_dict = {'a': 1, 'b': 2, 'c': 1, 'd': 1, 'e': 3, 'f': 4, 'g': 4}

new_dict = {}

for key, value in my_dict.items():
    if value not in new_dict.values():
        new_dict[key] = value

print(new_dict)
