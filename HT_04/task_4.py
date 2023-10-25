"""
Write a Python program that demonstrates exception chaining. Create a custom
exception class called CustomError and another called SpecificError.
In your program (could contain any logic you want), raise a SpecificError,
and then catch it in a try/except block, re-raise it as a CustomError with
the original exception as the cause. Display both the custom error message and
the original exception message.
"""


class CustomError(Exception):
    pass


class SpecificError(Exception):
    pass


try:
    print(1 / "1")
except TypeError as original_error:
    print("TypeError: дана операцій не підтримується")
    
    try:
        raise SpecificError("Specific error") from original_error
    except SpecificError as specific_error:
        print(specific_error)
        
        try:
            raise CustomError("Custom error") from specific_error
        except CustomError as custom_error:
            print(custom_error)