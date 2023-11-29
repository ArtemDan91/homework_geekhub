"""
1. Напишіть програму, де клас «геометричні фігури» (Figure) містить властивість color
з початковим значенням white і метод для зміни кольору фігури, а його підкласи «овал» (Oval)
і «квадрат» (Square) містять методи __init__ для завдання початкових розмірів об'єктів при їх створенні.
"""


class Figure:

    def __init__(self):
        self.color = 'white'

    def set_color(self, color):
        self.color = color


class Oval(Figure):

    def __init__(self, major_axis, minor_axis):
        super().__init__()
        self.major_axis = major_axis
        self.minor_axis = minor_axis

    def __str__(self):
        return f"Овал - колір: {self.color}, головна вісь: {self.major_axis}, побічна вісь: {self.minor_axis}"


class Square(Figure):

    def __init__(self, side_length):
        super().__init__()
        self.side_length = side_length

    def __str__(self):
        return f"Квадрат - колір: {self.color}, довжина сторони: {self.side_length}"


oval = Oval(15, 10)
oval.set_color('red')

square = Square(10)
square.set_color('black')

print(oval, square, sep='\n')