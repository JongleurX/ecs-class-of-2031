"""
game.py -- Core Game of Misere Nim logic (no external libraries).

Rules:
  - A pile of sticks starts with a random amount (20-30).
  - Players alternate taking 1 or 2 sticks.
  - The player who takes the LAST stick LOSES (Misere).
  - Hint: Watch the mod 3 pattern to discover the winning strategy.
"""

import random

MAX_TAKE = 3
MIN_STICKS = 20
MAX_STICKS = 30


def draw_sticks(count, is_player_turn=False):
    """Print a visual row of sticks, 10 per line.
    Add a border if it's the player's turn using box-drawing characters.
    """
    inner_width = 28

    def box_line(text):
        print(f"  │ {text:<{inner_width}} │")

    print()
    if is_player_turn:
        print("  ┌" + ("─" * (inner_width + 2)) + "┐")
    # Print in rows of 10 for readability
    row_size = 10
    for i in range(0, count, row_size):
        row = count - i
        n = min(row_size, row)
        sticks_line = "I " * n
        if is_player_turn:
            box_line(sticks_line)
        else:
            print(f"  {sticks_line}")
    if is_player_turn:
        remaining_text = f"({count} stick{'s' if count != 1 else ''} remaining)"
        box_line(remaining_text)
        print("  └" + ("─" * (inner_width + 2)) + "┘")
    else:
        print(f"  ({count} stick{'s' if count != 1 else ''} remaining)")
    print()


def show_hint(sticks_remaining):
    """Display modulo 3 strategy hint."""
    remainder = sticks_remaining % 3
    print(f"  Sticks mod 3: {remainder}")
    if remainder == 1:
        print(f"    ^ This is a LOSING position! (1, 4, 7, 10, ...)")
    else:
        target = sticks_remaining - remainder + 1
        print(f"    ^ HINT: Try to leave opponent with {target} (mod 3 = 1)")
    print()


def get_player_move(sticks_remaining):
    """Prompt the human player for a valid move."""
    show_hint(sticks_remaining)
    while True:
        try:
            take = int(input(f"Your turn! Take between 1 to {MAX_TAKE} sticks: "))
            if 1 <= take <= min(MAX_TAKE, sticks_remaining):
                return take
            print(f"  Choose between 1 and {min(MAX_TAKE, sticks_remaining)}.")
        except ValueError:
            print("  Enter a number.")


def play_round(strategy, player_goes_first=True):
    """Play one full game. Returns True if the human won (did NOT take the last stick)."""
    sticks = random.randint(MIN_STICKS, MAX_STICKS)
    player_turn = player_goes_first

    print("\n" + "=" * 40)
    print(f"  Game start! {sticks} sticks in the pile.")
    print("  MISERE RULES: Taking the LAST stick = you LOSE!")
    print("=" * 40)

    while sticks > 0:
        draw_sticks(sticks, is_player_turn=player_turn)

        if player_turn:
            take = get_player_move(sticks)
            print(f"  You took {take}.")
        else:
            take = strategy.get_turn(sticks, MAX_TAKE)
            take = max(1, min(take, min(MAX_TAKE, sticks)))  # clamp for safety
            print(f"  Computer takes {take}.")

        sticks -= take

        if sticks == 0:
            draw_sticks(0, is_player_turn=player_turn)
            if player_turn:
                print("  You took the last stick -- YOU LOSE! (Computer wins)")
                return False
            else:
                print("  Computer took the last stick -- COMPUTER LOSES! (You win!)")
                return True

        player_turn = not player_turn
