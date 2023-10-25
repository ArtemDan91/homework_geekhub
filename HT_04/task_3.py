"""
Create a Python script that takes an age as input. If the age is less than 18 or
 greater than 120, raise a custom exception called InvalidAgeError. Handle the
 InvalidAgeError by displaying an appropriate error message.
"""


class InvalidAgeError(Exception):
    pass


try:
    age = int(input("Enter your age: "))
    if age < 18 or age > 120:
        raise InvalidAgeError("InvalidAgeError: age must be from 18 to 120")
    print(f"Your entered age {age} is valid")
except ValueError:
    print("ValueError: entered value must be an integer")
except InvalidAgeError as e:
    print(e)
