"""Challenge 20: Compliment Machine
Enter your name and get a randomly generated, over-the-top compliment.
"""

import random

adjectives = [
    "absolutely radiant",
    "cosmically brilliant",
    "unreasonably talented",
    "suspiciously awesome",
    "dangerously charming",
    "legendarily cool",
    "scientifically impressive",
]

nouns = [
    "human being",
    "force of nature",
    "problem solver",
    "creative genius",
    "future legend",
]

extras = [
    "Scientists are baffled.",
    "Historians will write about this.",
    "Even robots are jealous.",
    "The stars aligned for this moment.",
    "This is not a drill.",
]

name = input("Enter your name: ").strip()
adj  = random.choice(adjectives)
noun = random.choice(nouns)
extra = random.choice(extras)

print(f"\n{name}, you are the most {adj} {noun} in the room.\n{extra} 🌟")
