"""Challenge 11: Magic 8-Ball
Ask it a yes/no question and get a random mystical answer.
"""

import random

responses = [
    "It is certain.",
    "Without a doubt.",
    "Ask again later.",
    "Don't count on it.",
    "My sources say no.",
    "Outlook not so good.",
    "Signs point to yes.",
    "Very doubtful.",
]

question = input("Ask the Magic 8-Ball a question: ")
print("🎱", random.choice(responses))
