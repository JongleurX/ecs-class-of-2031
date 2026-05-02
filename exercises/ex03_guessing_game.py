# ─────────────────────────────────────────────────────────────
#  Exercise 03 — Number guessing game — fix helper_hint()
#
#  Task:
#    Fix the two FIXME lines inside helper_hint() so the function
#    returns the correct count and best-guess (middle) value.
#
#    count  should be: high - low + 1
#    middle should be: (low + high) // 2
#
#    Example: helper_hint(1, 100)  →  "… 100 numbers left. Try 50 next!"
# ─────────────────────────────────────────────────────────────

import math
import random


def helper_hint(low, high):
    count  = high   # FIXME: should be  high - low + 1
    middle = low    # FIXME: should be  (low + high) // 2
    return (
        f"Between {low} and {high} — {count} numbers left.  "
        f"Try {middle} next!"
    )


def exercise_03():
    """Play the guessing game — your fixed helper_hint() gives clues!"""
    secret    = random.randint(1, 100)
    max_guess = math.ceil(math.log2(100))
    low, high = 1, 100
    guesses   = 0

    print(f"\nGuess the secret number between 1 and 100.")
    print(f"You have {max_guess} tries.\n")

    while guesses < max_guess:
        print(f"  Hint: {helper_hint(low, high)}")
        try:
            guess = int(input(f"  Guess #{guesses + 1}: ").strip())
        except ValueError:
            print("  Please enter a whole number.")
            continue
        guesses += 1
        if guess == secret:
            print(f"\nCorrect!  You got it in {guesses} guesses!")
            return
        elif guess < secret:
            low = guess + 1
            print("  Too low!")
        else:
            high = guess - 1
            print("  Too high!")
    print(f"\nGame over!  The number was {secret}.")
