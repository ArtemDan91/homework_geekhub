"""
4. Create 'list'-like object, but index starts from 1 and index of 0 raises error.
Тобто це повинен бути клас, який буде поводити себе так, як list (маючи основні методи),
але індексація повинна починатись із 1.
"""


class UserList:

    def __init__(self, *args):
        self.my_list = list(args)

    def __getitem__(self, index):
        if index < 1:
            raise IndexError("Значення індексу повинне бути більше 0")
        return self.my_list[index - 1]

    def __setitem__(self, index, value):
        if index < 1:
            raise IndexError("Значення індексу повинне бути більше 0")
        self.my_list[index - 1] = value

    def __delitem__(self, index):
        if index < 1:
            raise IndexError("Значення індексу повинне бути більше 0")
        del self.my_list[index - 1]

    def append(self, value):
        self.my_list.append(value)

    def pop(self, index=None):
        if index is not None and index < 1:
            raise IndexError("Значення індексу повинне бути більше 0")
        return self.my_list.pop(index - 1) if index is not None else self.my_list.pop()

    def insert(self, index, value):
        if index < 1:
            raise IndexError("Значення індексу повинне бути більше 0")
        self.my_list.insert(index - 1, value)

    def remove(self, value):
        self.my_list.remove(value)

    def __len__(self):
        return len(self.my_list)

    def __str__(self):
        return str(self.my_list)


user_list = UserList(1, 2, 3)
user_list.append(4)
user_list.remove(3)
user_list.pop()
user_list.insert(1, 10)
print(user_list)
print(user_list[1])