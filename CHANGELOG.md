# Changelog

Notable changes to this project. Format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Dates are used instead of version numbers.

## [Unreleased]

---

## [2026-05-02]

### Added
- Games: maze solver, Tower of Hanoi, and Nim.
- Code.org-friendly exercise variants and launchers.
- Warmup launchers and printable tracing materials.
- MIDI lab patch picker support for local GarageBand patches.
### Added
- `exercises/syntax/` folder for printable Python syntax materials
  - `PRINTABLE_Python_Reference.html`
  - `PRINTABLE_Syntax_Challenges.html`
  - `PRINTABLE_Syntax_Challenges_TEACHER.html`
  - `challenge_11_magic8ball.py` through `challenge_20_compliment_machine.py`
  - `challenge_14b_caesar_decoder.py`
  - `main.py` menu launcher
- `day1/main.py` launcher for Day 1.
- `day3/main.py` launcher for Day 3.

### Fixed
- Maze backtracking behavior and coach display consistency.
- `.DS_Store` ignore pattern.

### Changed
- Maze menu simplified.
- MIDI GUI startup improvements on macOS.
- Added generated lab data path to `.gitignore`.
- `labs/` reorganized with MIDI files moved into `labs/midi/`.
- `run_gui.sh` updated for the new MIDI lab path.
- Replaced `day2/main.py` with a recursive day launcher that discovers and runs
  Python files in `day2/` and all subfolders.
- Replaced `day4/main.py` with a recursive day launcher that discovers and runs
  Python files in `day4/` and all subfolders.
- Updated `README.md` for the current `day1`-`day4` structure and launcher usage.
- Updated `ACTIVITY_INVENTORY.md` to reflect the current folder layout and
  activities after the folder moves.

---

## [2026-04-12]

### Added
- MIDI lab scripts and GUI.
- GarageBand instrument control support.
- Example MIDI songs.
- Warmup tracing exercises and teacher guide.

---

## [2026-03-22]

### Added
- Initial beginner exercises.
- Early README and `.gitignore`.
