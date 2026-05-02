# Changelog

Notable changes to this project. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Dates are used instead of version numbers.

## [Unreleased]

---

## [2026-05-02]

Big session — added games, a second exercise format for Code.org, and a bunch of MIDI lab improvements.

### Added
- **Games** — maze solver with DFS step-by-step walkthrough (watch mode, algorithm-coach mode, free play), Tower of Hanoi, and Nim
- **`exercises/ex##_*.py`** — cleaner versions of the 7 exercises designed for Code.org's single-file workflow, with a `main.py` driver that runs and checks each one
- **Warmup `main.py`** — single-file runner for all 10 warmups; students predict output first, then unlock answers with a class password
- Printable HTML trace templates for the loop warmups (blank + filled-out teacher example)
- Printable HTML flag reference sheet for Exercise 07
- GarageBand patch picker in the MIDI lab GUI — searches your locally installed patches instead of guessing from GM names

### Fixed
- Maze: backtracking bug where the algorithm coach would send you back to a dead end you'd already visited
- Maze: algorithm coach line count was variable (causing the maze to jump around on screen); now always 7 lines
- `.DS_Store` was in `.gitignore` with a trailing `/` so it only matched directories — fixed to match files

### Changed
- Maze menu simplified from two levels (w/p then a/f) to a single prompt (w/a/f)
- MIDI lab GUI startup fixed on macOS by setting Qt plugin paths before importing PySide6
- `labs/data/` added to `.gitignore` — it's machine-specific generated data, rebuilt at runtime

---

## [2026-04-12]

### Added
- MIDI lab (`labs/`) — send notes, chords, and rhythms to a MIDI port using a simple text notation
- QML GUI for the MIDI lab
- GarageBand instrument control via AppleScript (by name or GM program number)
- Example songs: Heart and Soul, Firefly, Maya's Favorite
- 10 warmup exercises for hand-tracing practice, with a teacher guide

---

## [2026-03-22]

### Added
- Initial exercises 01–07: hello world, fix-the-typo, guessing game, functions, lists, Japanese tutor, flag painter
- README and `.gitignore`
