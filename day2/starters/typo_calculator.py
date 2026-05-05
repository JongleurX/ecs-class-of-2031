# ─────────────────────────────────────────────────────────────
#  Exercise 02 — Fix the typo calculator
#
#  Task:
#    1. Find the ONE method name that has a typo and fix it so
#       the program can run without crashing.
#    2. Change a and b to your own values and try different
#       operations: add, sub, mul, div
# ─────────────────────────────────────────────────────────────

def exercise_02():
    a = 8
    b = 5

    print("Please enter one of: add sub mul div")
    operation = input("Operation: ").stirp().lower()   # ← there is a typo here!

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


if __name__ == "__main__":
    exercise_02()
