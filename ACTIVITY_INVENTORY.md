# ECS 2026 Spring - Activity Inventory

Last updated: 2026-05-04

This inventory reflects the current post-reorganization layout in this repo.
It is organized by day folder and then by activity group.

## Launchers

Each day folder except day1 now has a `main.py` launcher:
- `day2/main.py`
- `day3/main.py`
- `day4/main.py`

Behavior:
- Each launcher recursively discovers `.py` files under its own day folder.
- The launcher shows a numeric menu and runs the selected script.
- After a script exits, control returns to the launcher menu.
- `day2/main.py`: Day 2 menu launcher for all Day 2 Python activities and subfolders.
- `day3/main.py`: Day 3 menu launcher for Caesar cipher and signal-solver demo scripts.
- `day4/main.py`: Day 4 menu launcher for the games and strategy activities.

## Day 1

Primary focus:
- HTML handouts and introductory browser-based materials.

## Day 2

### Starters

Folder: `day2/starters/`

Python files:
- `flag_painter.py`: Builds terminal flag patterns to practice abstraction with reusable drawing functions.
- `functions.py`: Has students write simple functions and return values with built-in test code.
- `guessing_game.py`: Uses a guessing game to practice reasoning about helper logic and binary-search-style hints.
- `hello_world.py`: Introduces variables and printing by having students personalize a simple program.
- `japanese_tutor.py`: Quizzes students on Japanese characters while tracking streaks and progress.
- `list_tricks.py`: Practices list editing and loops by changing and printing a small collection of items.
- `main.py`: Starter-activity launcher menu for the Day 2 starter scripts.
- `typo_calculator.py`: Debugging exercise where students fix a typo and then test calculator operations.

### Challenges

Folder: `day2/challenges/`

Python files:
- `color_mixer.py`: Combines two color names and returns a playful mixed-color result.
- `compliment_machine.py`: Generates random compliments by recombining words from several lists.
- `dice_duel.py`: Runs a short dice game against the computer with score accumulation across rounds.
- `magic8ball.py`: Answers yes-or-no questions with random Magic 8-Ball style responses.
- `main.py`: Challenge-activity launcher menu for the Day 2 challenge scripts.
- `mood_suggester.py`: Suggests an activity by matching mood words in the user's response.
- `name_scrambler.py`: Shuffles the letters of a user's name to create silly new versions.
- `pixel_art.py`: Draws ANSI-colored text art from a compact code-based picture format.
- `pizza_builder.py`: Collects a pizza order, chosen toppings, and total cost from the user.
- `trivia_quiz.py`: Runs a small quiz, tracks score, and gives a title based on performance.
- `virtual_pet.py`: Changes a pet's mood based on how many times it has been fed.

### Other Day 2 Materials

Folder: `day2/signal_solver/`

Non-Python instructional/support files:
- `signal_solver.html`: Print-friendly HTML version of the signal-solver lesson materials.
- `signal_solver.md`: Teacher-facing facilitation script for the signal-solver lesson.
- `signal-solver.css`: Stylesheet for the printable HTML signal-solver materials.
- `chalkboard_layout.drawio`: Chalkboard layout diagram for planning the in-class board setup.
- `export_chalkboard_markdown.sh`: Helper script for exporting the lesson Markdown into printable HTML.

## Day 3

### Caesar Cipher

Folder: `day3/caesar_cipher/`

Python files:
- `caesar_decoder.py`: Decodes Caesar-cipher messages by shifting letters backward three places.
- `caesar_encoder.py`: Encodes secret messages by shifting letters forward three places.

### Signal Solver Demo

Folder: `day3/signal_solver_demo/`

Python files:
- `lambda_demo.py`: Explains and demonstrates the lambda syntax used in the signal-solver code.
- `puzzle_generator.py`: Generates new signal puzzles that satisfy the lesson's rule structure.
- `signal_solver.py`: Compares brute-force and optimized approaches for solving constrained signal IDs.
- `solve_10digit.py`: Shows how a 10-digit brute-force search quickly becomes too large to be practical.
- `solve_3digit.py`: Small warm-up solver that demonstrates the brute-force method on a simpler puzzle.
- `solve_5digit.py`: Mid-sized solver that scales the same idea up to a more complex puzzle.
- `solve_7digit.py`: Larger signal solver that extends the constraint-solving pattern further.

### Day 3 Launcher

Python file:
- `day3/main.py`: Day 3 launcher that discovers and runs all Day 3 Python scripts.

## Day 4

### Hanoi

Folder: `day4/hanoi/`

Python files:
- `main.py`: Playable Tower of Hanoi game with move validation and optional teaching modes.

### Maze

Folder: `day4/maze/`

Python files:
- `main.py`: Generates mazes and lets students watch or interact with a depth-first-search solver.

Support docs:
- `REQUIREMENTS.md`: Design notes and technical requirements for the maze project.

### Nim

Folder: `day4/nim/`

Python files:
- `game.py`: Core Misere Nim round logic, stick display, and win/loss handling.
- `main.py`: Menu-driven Misere Nim game with difficulty selection and score tracking.
- `strategies.py`: Computer strategies for easy, medium, and optimal Nim play.

Support docs:
- `README.txt`: Teacher or student reference explaining the Nim rules and strategy.

### Day 4 Launcher

Python file:
- `day4/main.py`: Day 4 launcher that discovers and runs all Day 4 Python scripts.

### Treasure Hunter Unplugged

This is a CS unplugged actvity. I have included separate files for convenience because certain parts of the original PDF needed to be printed different numbers of times.

Folder: `day4/treasure-hunter-unplugged/`

Files:
- `treasure-hunt-fsa-demo.pdf`: Simple three-island diagram for demonstration purposes before the full treasure-hunt finite-state-automaton activity.
- `treasure-hunt-fsa-full.pdf`: Full, seven-island map for the treasure-hunt unplugged activity for the students acting as pirates.
- `treasure-island-finite_state_automata.pdf`: Full teacher's guide and instructions from CS Unplugged containing all the instructions and educational relevance.

## Bonus

Folder: `bonus/`

Files:
- `planets.json`: Data file containing planet facts used by the bonus astronomy activity.
- `planets.py`: Interactive astronomy script for exploring planet data and simple space visualizations.
- `stars.json`: Data file containing star and constellation facts for astronomy extensions.

## Abandoned / Archived

Folder: `abandoned/`

Contains archived materials from previous structures, including:
- legacy MIDI and lab folders
- legacy tracing/syntax paper materials
- previous standalone files and scripts

These are intentionally retained for reference/history and are not part of the current day-by-day student flow.
