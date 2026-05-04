MISERE NIM
==========

RULES
  - A pile of sticks sits between you and the computer.
  - On your turn, take 1 or 2 sticks.
  - The player who takes the LAST stick LOSES (Misere variant).
  - Your goal: FORCE the computer to take the last stick!

HOW TO RUN
  Open main.py and click Run.

FILES
  main.py        -- Start here. Menu and score tracking.
  game.py        -- Game loop, stick display, binary hints.
  strategies.py  -- Computer AI (Easy / Medium / Hard).

HINTS (shown during your turn)
  - Sticks in BINARY: The binary representation of the stick count.
  - Sticks MOD 3: The remainder when divided by 3.
    * If MOD 3 = 1 (e.g., 1, 4, 7, 10, ...): YOU'RE IN A LOSING POSITION.
    * Otherwise: try to leave the opponent at a MOD 3 = 1 number.

THE STRATEGY (Misere with max take = 2)
  Winning insight: Losing positions are 1, 4, 7, 10, 13, ...
  Pattern: sticks % 3 == 1
  So: After each of your moves, leave the opponent with a "mod 3 = 1" count.
  This forces them to leave you with "mod 3 != 1", and the cycle repeats.
  Eventually, you leave them with exactly 1 stick -- they must take it and lose!

DIFFICULTY LEVELS
  Easy   -- Computer picks randomly. Good for learning the rules.
  Medium -- Computer usually plays randomly but tries to control mod 3.
  Hard   -- Computer always plays optimally, leaving you in losing positions.
