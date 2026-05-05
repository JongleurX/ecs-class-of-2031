# ─────────────────────────────────────────────────────────────
#  Exercise 04 — Write your own functions
#
#  Task:
#    1. Implement greet_user(name) so it returns a friendly
#       greeting that includes the name.
#       Example: greet_user("Sophie") → "Hello, Sophie!"
#
#    2. Implement is_even(number) so it returns True when the
#       number is even, and False when it is odd.
#
#  Do NOT change the driver code in exercise_04() below.
# ─────────────────────────────────────────────────────────────

def greet_user(name):
    # TODO: return a string like "Hello, Sophie!"
    return ""


def is_even(number):
    # TODO: return True if number is even, False if odd
    return False


def exercise_04():
    """Runs your two functions with real user input."""
    user_name = input("Enter your name: ").strip()
    print(greet_user(user_name))

    n = int(input("Enter a number: ").strip())
    if is_even(n):
        print(n, "is even")
    else:
        print(n, "is odd")


if __name__ == "__main__":
    exercise_04()
