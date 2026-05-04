"""Challenge 15: Dice Duel
You vs. the computer. Roll dice 5 rounds, highest total wins.
"""

import random

player_total = 0
computer_total = 0

print("🎲 Dice Duel — 5 rounds!\n")

for round_num in range(1, 6):
    input(f"Round {round_num} — press Enter to roll...")
    player_roll   = random.randint(1, 6)
    computer_roll = random.randint(1, 6)
    player_total   += player_roll
    computer_total += computer_roll

    if player_roll > computer_roll:
        result = "You win the round!"
    elif computer_roll > player_roll:
        result = "Computer wins the round."
    else:
        result = "Tie!"

    print(f"  You rolled {player_roll}, Computer rolled {computer_roll} — {result}")

print(f"\nFinal score — You: {player_total}  Computer: {computer_total}")

if player_total > computer_total:
    print("🏆 You win the duel!")
elif computer_total > player_total:
    print("💻 Computer wins the duel. Better luck next time!")
else:
    print("🤝 It's a tie!")
