# ECS 2026 Spring - Activity Inventory

Last updated: 2026-05-03

This inventory reflects the current post-reorganization layout in this repo.
It is organized by day folder and then by activity group.

## Launchers

Each day folder now has a `main.py` launcher:
- `day1/main.py`
- `day2/main.py`
- `day3/main.py`
- `day4/main.py`

Behavior:
- Each launcher recursively discovers `.py` files under its own day folder.
- The launcher shows a numeric menu and runs the selected script.
- After a script exits, control returns to the launcher menu.

## Day 1

Primary focus:
- HTML handouts and introductory browser-based materials.

Python activities currently present:
- `day1/main.py` (launcher)

## Day 2

### Starters

Folder: `day2/starters/`

Python files:
- `flag_painter.py`
- `functions.py`
- `guessing_game.py`
- `hello_world.py`
- `japanese_tutor.py`
- `list_tricks.py`
- `main.py`
- `typo_calculator.py`

### Challenges

Folder: `day2/challenges/`

Python files:
- `color_mixer.py`
- `compliment_machine.py`
- `dice_duel.py`
- `magic8ball.py`
- `main.py`
- `mood_suggester.py`
- `name_scrambler.py`
- `pixel_art.py`
- `pizza_builder.py`
- `trivia_quiz.py`
- `virtual_pet.py`

### Other Day 2 Materials

Folder: `day2/signal_solver/`

Non-Python instructional/support files:
- `signal_solver.html`
- `signal_solver.md`
- `signal-solver.css`
- `chalkboard_layout.drawio`
- `export_chalkboard_markdown.sh`

## Day 3

### Caesar Cipher

Folder: `day3/caesar_cipher/`

Python files:
- `caesar_decoder.py`
- `caesar_encoder.py`

### Signal Solver Demo

Folder: `day3/signal_solver_demo/`

Python files:
- `lambda_demo.py`
- `puzzle_generator.py`
- `signal_solver.py`
- `solve_10digit.py`
- `solve_3digit.py`
- `solve_5digit.py`
- `solve_7digit.py`

### Day 3 Launcher

Python file:
- `day3/main.py`

## Day 4

### Hanoi

Folder: `day4/hanoi/`

Python files:
- `main.py`

### Maze

Folder: `day4/maze/`

Python files:
- `main.py`

Support docs:
- `REQUIREMENTS.md`

### Nim

Folder: `day4/nim/`

Python files:
- `game.py`
- `main.py`
- `strategies.py`

Support docs:
- `README.txt`

### Day 4 Launcher

Python file:
- `day4/main.py`

## Bonus

Folder: `bonus/`

Files:
- `planets.json`
- `planets.py`
- `stars.json`

## Abandoned / Archived

Folder: `abandoned/`

Contains archived materials from previous structures, including:
- legacy MIDI and lab folders
- legacy tracing/syntax paper materials
- previous standalone files and scripts

These are intentionally retained for reference/history and are not part of the
current day-by-day student flow.
