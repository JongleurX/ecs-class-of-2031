# Maze Solver – Requirements

## Overview

A terminal program that generates a random maze and lets the user either watch a robot solve it using Depth-First Search (DFS), or solve it themselves. Designed as a teaching tool for understanding DFS.

## Maze Generation

- Mazes are generated with the **recursive backtracker** algorithm, which always produces a perfect maze (exactly one path between any two cells).
- Three sizes: Small (5×7), Medium (9×11), Large (13×15).
- The user may supply an integer seed for a reproducible maze, or press Enter for a random seed.
- Start is always **top-left** (🚀); finish is always **bottom-right** (🏁).

## Display

- The maze is drawn with box-drawing characters and Unicode emoji.
- Each cell is 2 display columns wide (matching emoji width).
- Column and row axes are shown in interactive modes.
- Cell content:
  - 🤖 – current position
  - 🚀 – start (when not occupied)
  - 🏁 – finish (when not occupied)
  - `01`–`ff` – hex visit order (cells on the current DFS stack)
  - `×` (red) – visited and backtracked (dead end, no longer on path)

## Modes

### w – Watch mode
- The robot solves the maze automatically with DFS.
- Each step shows: the decision logic (wall / visited / open), the current DFS stack, and the maze.
- User presses Enter to advance each step.
- At the end, the solution path length is reported.

### a – Algorithm-learning mode
- The user controls the robot, but must follow DFS rules exactly.
- An **Algorithm Coach** panel is shown above the maze at each step.
  - Always shows exactly 7 lines (2 header + 4 direction lines + 1 conclusion).
  - Lists all four directions (W, N, E, S) with their status: wall / already visited / open and unvisited.
  - Marks the DFS-expected direction with `-> next DFS step`.
  - When backtracking is required, says so explicitly.
- Invalid moves show a two-line **gentle nudge** explaining the correct DFS action.
- Only moves consistent with DFS are accepted.

### f – Free-play mode
- The user controls the robot freely, no DFS restrictions.
- No coach panel is shown.
- Three blank lines are always printed after the maze (before the Move prompt) so the prompt position is stable regardless of previous feedback.
- At the end, the user's move count is compared to the DFS reference, and a medal is awarded if the user matched DFS exactly.

## Controls

| Key | Action |
|-----|--------|
| Arrow keys (or w/a/s/d) | Move North/West/South/East |
| `u` | Undo last move |
| `q` | Quit |
| Enter | Advance step (watch mode) |

In environments without raw terminal input, full-line input is used (type a letter then Enter).

## Backtracking Semantics

- **Visited** cells are tracked in a permanent set (`visited`) that is never cleared by undo.
- Undoing a move returns to the previous cell but does not un-visit any cell.
- The DFS coach uses the full `visited` set, so it will never direct the user back to a dead-end cell that has already been visited, even after an undo.
- The user may backtrack either by pressing `u` or by navigating directionally back to the parent cell.

## Menu Flow

```
Choose size  →  Choose seed  →  Choose mode (w / a / f)  →  Play again? (y/n)
```

All three modes are available directly from a single menu with no sub-options.

## Design Decisions

- `visited` is the single source of truth for "has this cell been seen by DFS". It is only ever added to, never shrunk.
- `history` tracks the current path (the DFS stack equivalent for the human player). Undo pops from `history` but not from `visited`.
- `faded` tracks cells that are visited but no longer on the active path (backtracked dead ends). These are displayed with a red `×`.
- The Algorithm Coach always shows all four directions so its line count is constant (7 lines), preventing the maze from shifting on screen between steps.
