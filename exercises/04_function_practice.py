#!/usr/bin/env python3

"""Exercise 04: Write your own function

Task:
1. Implement `greet_user(name)` so it returns a friendly greeting using the name.
2. Implement `is_even(number)` returning True or False.
3. Do not change driver code below, only fill the function bodies.
"""

def greet_user(name):
    # TODO: return a string like "Hello, Sophie!"
    return ""


def is_even(number):
    # TODO: return True when number is even, False when odd
    return False


# Driver code (do not edit for this exercise)
user_name = input("Enter your name: ").strip()
print(greet_user(user_name))

n = int(input("Enter a number: ").strip())
if is_even(n):
    print(n, "is even")
else:
    print(n, "is odd")
