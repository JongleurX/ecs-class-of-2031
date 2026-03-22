#!/usr/bin/env python3

"""Exercise 05: Lists and loops

Task:
1. Add a new animal name to the list `animals`.
2. Add a 2nd loop that prints animals in uppercase.
3. Optional: add a new function `count_vowels(word)` and use it.
"""

animals = ["cat", "dog", "rabbit"]

print("Animals in the list:")
for animal in animals:
    print("-", animal)

print("Total animals:", len(animals))

# TODO: Add a second loop here that prints animals in uppercase
# Hint: Use .upper() on each animal name

# Optional function for extension
def count_vowels(word):
    # TODO: Count how many vowels (a, e, i, o, u) are in the word
    # Return the count
    pass

# TODO: Add a loop here that uses count_vowels() to show vowel counts
# Example output: "cat has 1 vowels"
