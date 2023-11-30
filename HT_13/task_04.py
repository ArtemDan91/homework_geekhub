"""
4. Create 'list'-like object, but index starts from 1 and index of 0 raises error.
Тобто це повинен бути клас, який буде поводити себе так, як list (маючи основні методи),
але індексація повинна починатись із 1.
"""


class UserList:

    def __init__(self, *args):
        self.my_list = list(args)

    def index_logic(self, index):
        if index > 0:
            return index - 1
        elif index < 0:
            return len(self.my_list) + index
        else:
            raise IndexError("Значення індексу не повинне дорівнювати 0")

    def __getitem__(self, index):
        return self.my_list[self.index_logic(index)]

    def __setitem__(self, index, value):
        self.my_list[self.index_logic(index)] = value

    def __delitem__(self, index):
        del self.my_list[self.index_logic(index)]

    def append(self, value):
        self.my_list.append(value)

    def pop(self, index=None):
        return self.my_list.pop(self.index_logic(index)) if index is not None else self.my_list.pop()

    def insert(self, index, value):
        self.my_list.insert(self.index_logic(index), value)

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
print(user_list[-1])