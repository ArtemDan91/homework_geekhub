"""
Write a script to get the maximum and minimum value in a dictionary.
"""

# значення - числа
my_dict = {1: 1, 2: 40, 3: 23, 4: 44, 5: 2, 6: 34, 7: 90}

print(f"Maximum value in a dictionary: {max(my_dict.values())}")
print(f"Minimum value in a dictionary: {min(my_dict.values())}")


# значення - строки
# my_dict_1 = {1: "123", 2: "{bd", 3: "sfg", 4: "afg", 5: "QWE", 6: "HRB", 7: "!@#"}
# my_dict_2 = {1: "a", 2: "as", 3: "asd", 4: "asdf", 5: "asdfg", 6: "asdfgh", 7: "asdfghj"}

# print(f"Maximum value in a dictionary: {max(my_dict_1.values())}")
# print(f"Minimum value in a dictionary: {min(my_dict_1.values())}")


# значення - списки (кортежі - по аналогії)
# my_dict_1 = {1: [], 2: [1], 3: [1, 2], 4: [2, 1], 5: [2], 6: [2, 1, 0], 7: [2, 0, 1]}
# my_dict_2 = {1: [1], 2: [2], 3: [8], 4: [3], 5: [233], 6: [19], 7: [4]}

# print(f"Maximum value in a dictionary: {max(my_dict_1.values())}")
# print(f"Minimum value in a dictionary: {min(my_dict_1.values())}")


# значення - множини
# my_dict = {1: {100}, 2: {2}, 3: {5, 2, 3, 4}, 4: {1, 2, 3, 5}, 5: {2, 3, 19, 1}, 6: {19, 1}, 7: {4}}

# max_value = max(my_dict.values(), key=lambda x: max(x))
# min_value = min(my_dict.values(), key=lambda x: min(x))

# print(f"Maximum value in a dictionary: {max_value}")
# print(f"Minimum value in a dictionary: {min_value}")


# значення - словники
# my_dict = {
#     1: {'v': 10},
#     2: {'e': 55},
#     3: {'y': 15},
#     4: {'a': 31},
#     5: {'n': 12}
# }

# max_value = max(my_dict.values(), key=lambda x: list(x.values()))
# min_value = min(my_dict.values(), key=lambda x: list(x.values()))

# print(f"Maximum value in a dictionary: {max_value}")
# print(f"Minimum value in a dictionary: {min_value}")