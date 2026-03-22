#!/usr/bin/env python3

"""Exercise 03: Number Guessing Game with Limited Tries

Task A (Play the game):
1. Run: ./03_guess_age.py
2. Guess a number between 1 and 100. You have 7 tries.
3. Use feedback (too high/too low) to narrow down.
4. Can you win?

Task B (Programming Challenge):
1. Look for the helper_hint() function below (marked with TODO).
2. Run with: ./03_guess_age.py --helper
3. Implement helper_hint() to show:
   - How many numbers are still possible in the remaining range
   - What the middle number is to guess next
4. Example output: "50 numbers left. Try 50 next!"
5. Hint: This teaches "binary search" -- a smart guessing strategy!
"""

import sys
import random
import math

# Game settings
MIN_NUMBER = 1
MAX_NUMBER = 100
SECRET_NUMBER = random.randint(MIN_NUMBER, MAX_NUMBER)
# Calculate optimal guesses for binary search: ceil(log2(range))
MAX_GUESSES = math.ceil(math.log2(MAX_NUMBER - MIN_NUMBER + 1))


def helper_hint(low, high):
    """
    TODO: Make this function useful for a younger player.
    
    Parameters:
    - low: The smallest possible number
    - high: The largest possible number
    
    Return a helpful string hint that shows:
    1. How many numbers are still possible (high - low + 1)
    2. What the middle (best guess) number is (halfway between low and high)
    
    Example: "42 numbers left. Middle = 50. Guess next?"
    """
    count = high - low + 1
    middle = (low + high) // 2
    return f"Our number is between {low} and {high}, with {count} possible numbers left. Try {middle} next!"


def play_game(show_helper=False):
    guesses_made = 0
    low = MIN_NUMBER
    high = MAX_NUMBER
    
    print(f"🎮 Guess the secret number between {MIN_NUMBER} and {MAX_NUMBER}!")
    print(f"📊 You have {MAX_GUESSES} guesses.\n")
    
    while guesses_made < MAX_GUESSES:
        tries_left = MAX_GUESSES - guesses_made
        prompt = f"Guess #{guesses_made + 1} ({tries_left} left): "
        
        try:
            guess = int(input(prompt).strip())
        except ValueError:
            print("   ⚠️  Please enter a valid number.")
            continue
        
        guesses_made += 1
        
        if guess == SECRET_NUMBER:
            print(f"\n🎉 Correct! You got it in {guesses_made} guesses!")
            return
        elif guess < SECRET_NUMBER:
            low = guess + 1
            print(f"   📈 Too low! The secret is higher.")
        else:
            high = guess - 1
            print(f"   📉 Too high! The secret is lower.")
        
        if show_helper and guesses_made < MAX_GUESSES:
            hint = helper_hint(low, high)
            if hint:
                print(f"   💡 {hint}")
    
    print(f"\n❌ Game Over! The secret number was {SECRET_NUMBER}.")
    print(f"💡 Tip: Try guessing the middle number of the range each time!")


# Main
if "--helper" in sys.argv:
    play_game(show_helper=True)
else:
    play_game(show_helper=False)
