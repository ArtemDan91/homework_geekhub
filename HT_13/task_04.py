"""
4. Create 'list'-like object, but index starts from 1 and index of 0 raises error.
Тобто це повинен бути клас, який буде поводити себе так, як list (маючи основні методи),
але індексація повинна починатись із 1.
"""


class UserList:

    def __init__(self, *args):
        self.my_list = list(args)

    def index_logic(self, index):
        if isinstance(index, int):
            if index > 0:
                return index - 1
            elif index < 0:
                if abs(index) <= len(self.my_list):
                    return len(self.my_list) + index
                else:
                    raise IndexError("Індекс списку поза діапазоном")
            else:
                raise IndexError("Значення індексу не повинне дорівнювати 0")
        else:
            raise TypeError("Індекс повинен бути цілим числом")
        
    def __getitem__(self, index):
        try:
            return self.my_list[self.index_logic(index)]
        except IndexError as e:
            raise IndexError(f"Помилка доступу за індексом: {e}")

    def __setitem__(self, index, value):
        try:
            self.my_list[self.index_logic(index)] = value
        except IndexError as e:
            raise IndexError(f"Помилка встановлення значення по індексу: {e}")
        
    def __delitem__(self, index):
        try:
            del self.my_list[self.index_logic(index)]
        except IndexError as e:
            raise IndexError(f"Помилка видалення за індексом: {e}")

    def append(self, value):
        self.my_list.append(value)

    def pop(self, index=None):
        try:
            return self.my_list.pop(self.index_logic(index)) if index is not None else self.my_list.pop()
        except IndexError as e:
            raise IndexError(f"Помилка видалення за індексом: {e}")
        
    def insert(self, index, value):
        try:
            if 0 <= self.index_logic(index) <= len(self.my_list):
                self.my_list.insert(self.index_logic(index), value)
            else:
                raise IndexError("Недопустимий індекс для вставки")
        except IndexError as e:
            raise IndexError(f"Помилка вставки за індексом: {e}")

    def remove(self, value):
        try:
            self.my_list.remove(value)
        except ValueError as e:
            raise ValueError(f"Помилка видалення значення: {e}")

    def __len__(self):
        return len(self.my_list)

    def __str__(self):
        return str(self.my_list)


user_list = UserList(1, 2, 3)
user_list.append(4)
user_list.remove(3)
user_list.pop()
user_list.insert(1, 10)
print(user_list[-1])

