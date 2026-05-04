# ECS G7 Spring Computational Thinking Block Curriculum

This repository contains Python teaching materials and printable resources for
the ECS Spring 2026 computational thinking block. These activities are designed to help introduce 11-12 year old students transition from Scratch programming into Python programming for the first time. There is a companion teacher's guide at [G7 ECS CS Lesson Plans 2025-2026](https://docs.google.com/document/d/1eqvwf6xUf6dYRwR7-1Oa6eNIcvG8NE2ppLJUQMMULEo/edit?usp=sharing).

Everything in this repo is pure Python, without the need for pip or extra libraries. One primary reason for this is that student Chromebooks do not have any native tools for running Python. Doing so would require installing Linux, which was too burdensome for a volunteer-led class with no IT staff.

The launcher system is designed to make it easy and efficient to create Code.org Python Lab "console output"-style projects that can easily be imported from GitHub to boostrap "remixable" environments. This is an efficient means of getting foundational code onto a learner's screen and avoiding them needing to type anything, and avoiding complexity in having school administrators grant access to GitHub or other external sites beyond Code.org.

## Current Layout

- `day1/`:
  - Intro HTML activities and handouts.
- `day2/`:
  - Starter Python activities in `day2/starters/`.
  - Challenge Python activities in `day2/challenges/`.
  - `signal_solver/` HTML/CSS/Markdown materials.
  - `main.py` launches all Day 2 Python scripts recursively.
- `day3/`:
  - `caesar_cipher/` scripts.
  - `signal_solver_demo/` scripts, including puzzle generator and solvers.
  - `main.py` launches all Day 3 Python scripts recursively.
- `day4/`:
  - Games and strategy projects in `hanoi/`, `maze/`, and `nim/`.
  - `main.py` launches all Day 4 Python scripts recursively.
- `bonus/`:
  - Extra astronomy-themed scripts and data, per Ms. Alison's request.
- `abandoned/`:
  - Archived or retired materials and earlier folder structures.

## Running Day Menus

From the repo root, run any day launcher:

```bash
python3 day2/main.py
python3 day3/main.py
python3 day4/main.py
```

There is no committed code for day 1, because we'll be mostly tracing things on paper and typing in some simple programs from scratch into the Code.org editor.

Each day launcher:
- Finds Python files in that day folder and all subfolders.
- Shows a numbered menu.
- Runs the selected script and returns to the menu afterward.

## Notes

- Some scripts are designed as importable support modules (for example, game
  helper files). They are still listed because the launcher is file-based.
- If a script requires local relative imports, the launcher temporarily changes
  working directory and `sys.path` so those imports still work.
