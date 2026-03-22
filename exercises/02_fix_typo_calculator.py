#!/usr/bin/env python3

"""Exercise 02: Fix the typo + change values

The code has a small typo that causes an error.
Task:
1. Find and fix the typo.
2. Change `a` and `b` values to your own.
3. Try different operations and run again.
"""

# Student-edit section
# Fix `stirp` to `strip`, and optionally change a, b.
a = 8
b = 5

text = "Please enter one of: add sub mul div"
print(text)

operation = input("Operation: ").stirp().lower()

if operation == "add":
    print("Result:", a + b)
elif operation == "sub":
    print("Result:", a - b)
elif operation == "mul":
    print("Result:", a * b)
elif operation == "div":
    if b == 0:
        print("Cannot divide by zero")
    else:
        print("Result:", a / b)
else:
    print("Unknown operation")
