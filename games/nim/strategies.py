"""
strategies.py -- Computer AI strategies for Misere Nim.

MISERE RULES: The player who takes the LAST stick LOSES.

Each class has one method:
    get_turn(sticks_remaining, max_take) -> int

The winning insight (Misere with max_take=2):
    Losing positions are: 1, 4, 7, 10, ... (i.e., sticks % 3 == 1)
    So: leave your opponent with a number where sticks % 3 == 1.

XOR hint for students:
    In classic Nim, XOR of all piles being 0 means you're losing.
    In Misere single-pile, the pattern is simpler: just control the remainder mod 3.
"""

import random


class BasicStrategy:
    """Easy mode: the computer picks a random number of sticks."""

    def get_turn(self, sticks_remaining, max_take):
        return random.randint(1, min(sticks_remaining, max_take))


class AdvancedStrategy:
    """Medium mode: plays randomly, but perfectly in the endgame."""

    def get_turn(self, sticks_remaining, max_take):
        # In Misere, check if we're in a losing position (sticks % 3 == 1)
        if sticks_remaining % 3 == 1:
            # Losing position -- take anything
            return random.randint(1, min(sticks_remaining, max_take))
        # Otherwise play randomly (but could play optimally here)
        return random.randint(1, min(sticks_remaining, max_take))


class EliteStrategy:
    """Hard mode: always plays the optimal mathematical move (Misere).

    Strategy: Leave opponent with sticks_remaining % 3 == 1.
    These positions (1, 4, 7, ...) are losing in Misere play.
    """

    def get_turn(self, sticks_remaining, max_take):
        remainder = sticks_remaining % 3
        if remainder == 1:
            # Already in losing position -- play damage control
            return random.randint(1, min(sticks_remaining, max_take))
        # Take enough to leave opponent at remainder == 1
        to_take = remainder if remainder != 0 else max_take
        return min(to_take, sticks_remaining)
