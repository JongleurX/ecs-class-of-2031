"""Syntax Challenges — main launcher
Run this file to pick and play any challenge.
Press Ctrl-C during a challenge to return to the menu early.
"""

import os
import runpy

# Directory this file lives in
HERE = os.path.dirname(os.path.abspath(__file__))

CHALLENGES = [
    ("11",  "🎱  Magic 8-Ball",               "challenge_11_magic8ball.py"),
    ("12",  "🐾  Virtual Pet Mood Tracker",    "challenge_12_virtual_pet.py"),
    ("13",  "🎨  Color Mixer",                 "challenge_13_color_mixer.py"),
    ("14a", "🔐  Secret Message Encoder",      "challenge_14a_caesar_cipher.py"),
    ("14b", "🔓  Secret Message Decoder",      "challenge_14b_caesar_decoder.py"),
    ("15",  "🎲  Dice Duel",                   "challenge_15_dice_duel.py"),
    ("16",  "🌦️  Mood-Based Suggester",        "challenge_16_mood_suggester.py"),
    ("17",  "🍕  Pizza Order Builder",          "challenge_17_pizza_builder.py"),
    ("18",  "🧠  Trivia Quiz",                  "challenge_18_trivia_quiz.py"),
    ("19",  "🐍  Name Scrambler",               "challenge_19_name_scrambler.py"),
    ("20",  "🌈  Compliment Machine",           "challenge_20_compliment_machine.py"),
]

# Build a lookup: number string → file path
LOOKUP = {num: os.path.join(HERE, filename) for num, _, filename in CHALLENGES}


def show_menu():
    print("\n" + "=" * 44)
    print("   Python Creative Challenges — Menu")
    print("=" * 44)
    for num, title, _ in CHALLENGES:
        print(f"  {num:>3}.  {title}")
    print("-" * 44)
    print("   q    Quit")
    print("=" * 44)


def run_challenge(num):
    path = LOOKUP[num]
    print(f"\n{'─' * 44}")
    try:
        runpy.run_path(path, run_name="__main__")
    except KeyboardInterrupt:
        print("\n\n(Returned to menu)")
    print(f"{'─' * 44}")
    input("Press Enter to return to the menu...")


def main():
    valid = set(LOOKUP.keys())
    while True:
        show_menu()
        choice = input("Enter a challenge number: ").strip().lower()
        if choice in ("q", "quit", "exit"):
            print("Bye! 👋")
            break
        elif choice in valid:
            run_challenge(choice)
        else:
            print(f"  ✗ '{choice}' isn't on the list. Try again.")


if __name__ == "__main__":
    main()
