"""
main.py -- Misere Nim (Code.org compatible, standard library only)

How to play:
  - You and the computer take turns taking 1 or 2 sticks.
  - MISERE RULE: The player who takes the LAST stick LOSES.
  - Your turn shows binary hints and the mod 3 pattern.
  - Pick a difficulty and try to beat the computer!
"""

import random
from strategies import BasicStrategy, AdvancedStrategy, EliteStrategy
from game import play_round


DIFFICULTIES = {
    "1": ("Easy",    BasicStrategy(),    "plays randomly"),
    "2": ("Medium",  AdvancedStrategy(), "mostly random but tries to control mod 3"),
    "3": ("Hard",    EliteStrategy(),    "always leaves you at a losing position (mod 3 = 1)"),
}


def pick_difficulty():
    print("\n  Select difficulty:")
    for key, (name, _, desc) in DIFFICULTIES.items():
        print(f"    {key}. {name} -- {desc}")
    while True:
        choice = input("  Enter 1, 2, or 3: ").strip()
        if choice in DIFFICULTIES:
            return DIFFICULTIES[choice]
        print("  Please enter 1, 2, or 3.")


def main():
    print("=" * 40)
    print("     MISERE NIM")
    print("=" * 40)
    print("  Take 1 or 2 sticks each turn.")
    print("  AVOID taking the LAST stick (you lose if you do)!")

    wins = 0
    losses = 0

    while True:
        name, strategy, _ = pick_difficulty()
        player_first = random.choice([True, False])
        who = "You go first!" if player_first else "Computer goes first!"
        print(f"\n  Difficulty: {name}. {who}")

        won = play_round(strategy, player_goes_first=player_first)
        if won:
            wins += 1
        else:
            losses += 1

        print(f"\n  Score -- You: {wins}  Computer: {losses}")
        again = input("  Play again? (y/n): ").strip().lower()
        if again != "y":
            break

    print("\n  Thanks for playing!")
    print(f"  Final score -- You: {wins}  Computer: {losses}")


main()
