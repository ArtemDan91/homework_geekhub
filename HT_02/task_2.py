"""
Write a script which accepts two sequences of comma-separated colors 
from user. Then print out a set containing all the colors from 
color_list_1 which are not present in color_list_2.
"""

color_list_1 = input("Write first sequence of colors: ").replace(" ", "").split(",")
color_list_2 = input("Write second sequence of colors: ").replace(" ", "").split(",")

print(set(color_list_1).difference(set(color_list_2)))