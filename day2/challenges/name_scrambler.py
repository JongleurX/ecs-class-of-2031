"""Challenge 19: Name Scrambler
Enter your name and get a silly scrambled version back every time.
"""

import random

name = input("Enter your name: ").strip()
letters = list(name)
random.shuffle(letters)
scrambled = "".join(letters)

print("Your scrambled name is:", scrambled)
print("(Run it again for a different scramble!)")
