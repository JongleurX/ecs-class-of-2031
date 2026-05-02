"""Maze Solver -- DFS step-by-step (Code.org-compatible, standard library only).

The program generates a random maze, then either:
  - Lets you watch a robot solve it using Depth-First Search (DFS), with
    a running explanation of every decision the robot makes.
  - Lets you solve the maze yourself by typing directions.

Maze symbols:
  🤖  the robot's current position
  01  a hex step number -- this was the Nth cell visited (01 = first cell)
    ×   a red cross mark -- visited and backtracked (dead end, no longer on the path)
  🚀  start position (always top-left)
  🏁  finish position (always bottom-right)
"""

import random
import shutil
import sys
import os

try:
    import termios
    import tty
    _HAVE_TERMIOS = True
except ImportError:
    _HAVE_TERMIOS = False

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
N, S, E, W = 0, 1, 2, 3
OPPOSITE = {N: S, S: N, E: W, W: E}
DR = {N: -1, S: 1, E: 0,  W: 0}
DC = {N: 0,  S: 0, E: 1,  W: -1}
DIR_NAME = {N: "North", S: "South", E: "East", W: "West"}
DIR_ARROW = {N: "↑", S: "↓", E: "→", W: "←"}

# Box-drawing junction lookup.
# Key = (has_north_arm, has_south_arm, has_east_arm, has_west_arm).
# At each interior crossing, determine which arms extend before choosing the char.
_JUNC = {
    (0,0,0,0): " ", (1,0,0,0): "╵", (0,1,0,0): "╷", (0,0,1,0): "╶", (0,0,0,1): "╴",
    (1,1,0,0): "│", (0,0,1,1): "─",
    (1,0,1,0): "└", (1,0,0,1): "┘", (0,1,1,0): "┌", (0,1,0,1): "┐",
    (1,1,1,0): "├", (1,1,0,1): "┤", (1,0,1,1): "┴", (0,1,1,1): "┬",
    (1,1,1,1): "┼",
}

ROBOT  = "🤖"   # 2-display-column wide emoji
_USE_ANSI = sys.stdout.isatty()
ANSI_RED = "\033[31m" if _USE_ANSI else ""
ANSI_CYAN = "\033[36m" if _USE_ANSI else ""
ANSI_YELLOW = "\033[33m" if _USE_ANSI else ""
ANSI_GREEN = "\033[32m" if _USE_ANSI else ""
ANSI_DIM = "\033[2m" if _USE_ANSI else ""
ANSI_BOLD = "\033[1m" if _USE_ANSI else ""
ANSI_RESET = "\033[0m" if _USE_ANSI else ""
ANSI_CLEAR = "\033[2J" if _USE_ANSI else ""
ANSI_HOME = "\033[H" if _USE_ANSI else ""
FADED  = f"{ANSI_RED}×{ANSI_RESET} "   # red multiplication sign + space = 2 display cols
EMPTY  = "  "   # 2 spaces = 2 display cols
START  = "🚀"   # 2-display-column wide emoji
FINISH = "🏁"   # 2-display-column wide emoji

SIZES = {
    "s": (5, 7,  "Small  (5 rows × 7 cols)"),
    "m": (9, 11, "Medium (9 rows × 11 cols)"),
    "l": (13, 15, "Large  (13 rows × 15 cols)"),
}


def _paint(text, color):
    return f"{color}{text}{ANSI_RESET}" if _USE_ANSI and color else text


def _section_header(text, color):
    return _paint(f"{ANSI_BOLD}{text}", color)


def _clear_screen():
    """Clear the terminal for a clean next frame in interactive sessions."""
    if not (sys.stdout.isatty() and sys.stdin.isatty()):
        return

    # Prefer the shell's clear command for broader terminal compatibility.
    cmd = "cls" if os.name == "nt" else "clear"
    rc = os.system(cmd)

    # Fallback when clear/cls is unavailable.
    if rc != 0 and _USE_ANSI:
        sys.stdout.write(ANSI_CLEAR + ANSI_HOME)
        sys.stdout.flush()


# ---------------------------------------------------------------------------
# Maze generation  (recursive backtracker -- always produces one solution)
# ---------------------------------------------------------------------------

def generate_maze(rows, cols, seed=None):
    """Return a grid of wall sets.

    grid[r][c] is a set of directions in which the wall has been REMOVED
    (i.e. passages that exist).  Start = (0,0), Finish = (rows-1, cols-1).
    """
    rng = random.Random(seed)
    grid = [[set() for _ in range(cols)] for _ in range(rows)]
    visited = [[False] * cols for _ in range(rows)]

    def carve(r, c):
        visited[r][c] = True
        dirs = [N, S, E, W]
        rng.shuffle(dirs)
        for d in dirs:
            nr, nc = r + DR[d], c + DC[d]
            if 0 <= nr < rows and 0 <= nc < cols and not visited[nr][nc]:
                grid[r][c].add(d)
                grid[nr][nc].add(OPPOSITE[d])
                carve(nr, nc)

    # Python's default recursion limit is 1000; a 13x15 maze has 195 cells,
    # so we're safely within limits.
    carve(0, 0)
    return grid


# ---------------------------------------------------------------------------
# Maze rendering
# ---------------------------------------------------------------------------

def _cell_str(r, c, rows, cols, robot_pos, step_map, faded_set, start, finish):
    """Return a 2-display-column string for the interior of cell (r, c)."""
    if (r, c) == robot_pos:
        return ROBOT
    if (r, c) == finish:
        return FINISH
    if (r, c) == start:
        return START
    if (r, c) in faded_set:
        return FADED
    if (r, c) in step_map:
        return f"{step_map[(r, c)]:02x}"
    return EMPTY


def render_maze(grid, rows, cols, robot_pos=None, step_map=None,
                faded_set=None, start=(0, 0), finish=None, show_axes=False):
    """Print the maze as ASCII art with box-drawing characters."""
    if finish is None:
        finish = (rows - 1, cols - 1)
    if step_map is None:
        step_map = {}
    if faded_set is None:
        faded_set = set()

    lines = []

    # Top border  (── = 2 display cols per cell, matching emoji width)
    top = "┌"
    for c in range(cols):
        top += "──"
        if c < cols - 1:
            s_arm = 0 if E in grid[0][c] else 1
            top += _JUNC[(0, s_arm, 1, 1)]
        else:
            top += "┐"
    lines.append(top)

    for r in range(rows):
        # Cell row: left border + cells + vertical walls
        cell_line = "│"
        for c in range(cols):
            cell_line += _cell_str(r, c, rows, cols, robot_pos,
                                   step_map, faded_set, start, finish)
            if c < cols - 1:
                # Wall between (r,c) and (r,c+1)
                cell_line += " " if E in grid[r][c] else "│"
            else:
                cell_line += "│"
        lines.append(cell_line)

        # Horizontal wall row between row r and row r+1
        if r < rows - 1:
            e_arm = 0 if S in grid[r][0] else 1
            wall_line = _JUNC[(1, 1, e_arm, 0)]
            for c in range(cols):
                wall_line += "  " if S in grid[r][c] else "──"
                if c < cols - 1:
                    n_arm = 0 if E in grid[r][c]     else 1
                    s_arm = 0 if E in grid[r + 1][c] else 1
                    w_arm = 0 if S in grid[r][c]     else 1
                    e_arm = 0 if S in grid[r][c + 1] else 1
                    wall_line += _JUNC[(n_arm, s_arm, e_arm, w_arm)]
                else:
                    w_arm = 0 if S in grid[r][cols - 1] else 1
                    wall_line += _JUNC[(1, 1, 0, w_arm)]
            lines.append(wall_line)

    # Bottom border
    bot = "└"
    for c in range(cols):
        bot += "──"
        if c < cols - 1:
            n_arm = 0 if E in grid[rows - 1][c] else 1
            bot += _JUNC[(n_arm, 0, 1, 1)]
        else:
            bot += "┘"
    lines.append(bot)

    print()
    if show_axes:
        col_hdr = "    "
        for c in range(cols):
            col_hdr += f"{c + 1:2d}"
            if c < cols - 1:
                col_hdr += " "
        print("  " + col_hdr)

        row_num = 1
        for i, line in enumerate(lines):
            if i % 2 == 1 and i < len(lines) - 1:
                label = f"{row_num:2d} "
                row_num += 1
            else:
                label = "   "
            print("  " + label + line)
    else:
        for line in lines:
            print("  " + line)
    print()


# ---------------------------------------------------------------------------
# DFS solver  (yields steps for animation)
# ---------------------------------------------------------------------------

class DFSSolver:
    """Step-by-step DFS maze solver.

    Call .step() to advance one decision.
    State is exposed as public attributes for the renderer/narrator.
    """

    def __init__(self, grid, rows, cols, start=(0, 0), finish=None):
        self.grid = grid
        self.rows = rows
        self.cols = cols
        self.start = start
        self.finish = finish if finish else (rows - 1, cols - 1)

        self.stack = [start]           # DFS stack of (r, c) positions
        self.visited = {start}         # all cells ever pushed
        self.faded = set()             # cells popped (backtracked)
        self.solved = False
        self.dead_end = False          # True during the step where we backtrack
        self.tried_this_step = []      # list of (dir, "wall"|"visited"|"ok")
        self.current = start
        self.push_count = 1            # start cell is push #1
        self.step_map = {start: 1}     # cell -> push order (hex step number)

    def step(self):
        """Advance one step.  Returns True if solving should continue."""
        if self.solved or not self.stack:
            return False

        self.current = self.stack[-1]
        self.dead_end = False
        self.tried_this_step = []

        if self.current == self.finish:
            self.solved = True
            return False

        # Try each direction in order W, N, E, S  (leftmost / "turn left" first)
        for d in [W, N, E, S]:
            nr, nc = self.current[0] + DR[d], self.current[1] + DC[d]
            if d not in self.grid[self.current[0]][self.current[1]]:
                self.tried_this_step.append((d, "wall"))
            elif (nr, nc) in self.visited:
                self.tried_this_step.append((d, "visited"))
            else:
                self.tried_this_step.append((d, "move"))
                self.visited.add((nr, nc))
                self.stack.append((nr, nc))
                self.push_count += 1
                self.step_map[(nr, nc)] = self.push_count
                return True

        # No unvisited neighbour -- backtrack
        self.dead_end = True
        self.faded.add(self.stack.pop())
        return True


# ---------------------------------------------------------------------------
# Narrator helpers
# ---------------------------------------------------------------------------

def _step_lines(solver):
    """Return human-readable explanation lines for the most recent DFS step."""
    r, c = solver.current
    cur_hex = f"{solver.step_map.get((r, c), 1):02x}"
    lines = []

    if solver.dead_end:
        return_to = solver.stack[-1] if solver.stack else None
        ret_str = ""
        if return_to:
            rr, rc = return_to
            ret_hex = f"{solver.step_map.get(return_to, 1):02x}"
            ret_str = f"  Returning to {ret_hex} (r{rr+1}c{rc+1})."
        lines.append(f"  Deciding from {cur_hex} (r{r+1}c{c+1})  "
                     f"[stack depth before pop: {len(solver.stack) + 1}]")
        lines.append("  ❌ Dead end -- no unvisited open neighbours.")
        lines.append("     Popping this cell off the stack." + ret_str)
    else:
        lines.append(f"  Deciding from {cur_hex} (r{r+1}c{c+1})  "
                     f"[stack depth: {len(solver.stack)}]")
        for d, reason in solver.tried_this_step:
            arrow = DIR_ARROW[d]
            name = DIR_NAME[d]
            if reason == "wall":
                lines.append(f"  {arrow} {name:5s}:  wall.")
            elif reason == "visited":
                lines.append(f"  {arrow} {name:5s}:  already visited -- skip.")
            else:
                nr, nc = r + DR[d], c + DC[d]
                new_hex = f"{solver.step_map.get((nr, nc), 0):02x}"
                lines.append(f"  {arrow} {name:5s}:  open!  "
                              f"Pushed {new_hex} (r{nr+1}c{nc+1}) onto stack.")

    return lines


def _narrate_start(rows, cols, start, finish):
    print("  The robot starts at 🚀 (top-left) and wants to reach 🏁 (bottom-right).")
    print()
    print("  HOW DEPTH-FIRST SEARCH WORKS:")
    print("  1. Push the start cell onto the stack.  Label it 01.")
    print("  2. Look at the top of the stack (current cell).")
    print("  3. Try each direction (W, N, E, S) in order -- leftmost first.")
    print("     - If there's a wall: skip.")
    print("     - If already visited: skip.")
    print("     - If open and unvisited: push it, label it with the next hex number.")
    print("  4. If NO direction works: BACKTRACK -- pop this cell, go to step 2.")
    print("  5. Repeat until the robot reaches 🏁.")
    print()
    print("  Each cell shows the hex number of when it was first visited (01, 02, ...).")
    print("  Numbers on the board = currently on the DFS stack (the active path).")
    print("  ×  red cross = visited and backtracked (dead end, no longer on the stack).")
    print()


# ---------------------------------------------------------------------------
# DFS board renderer (watch mode: hex step numbers + axis labels + stack)
# ---------------------------------------------------------------------------

def _build_dfs_board_lines(grid, rows, cols, solver):
    """Return maze lines and stack lines for watch mode."""
    finish = solver.finish
    stack_set = set(solver.stack)
    robot_pos = solver.stack[-1] if solver.stack and not solver.solved else None

    def cell_str(r, c):
        pos = (r, c)
        if pos == robot_pos:
            return ROBOT            # 🤖  (2-wide emoji)
        if pos == finish:
            return FINISH           # 🏁  (2-wide emoji)
        if pos in solver.faded:
            return FADED            # red × (backtracked dead end)
        if pos in stack_set:
            n = solver.step_map.get(pos, 0)
            return f"{n:02x}"         # e.g. 01, 0f, 1a  (2 ASCII chars)
        return "  "                 # empty cell

    # ── Column header (decimal, right-justified in 2 chars) ─────────────────
    col_hdr = "    "   # 3-char row-label area + 1 char for left │
    for c in range(cols):
        col_hdr += f"{c + 1:2d}"
        if c < cols - 1:
            col_hdr += " "          # 1-char gap, same width as wall char

    # ── Build maze lines as (row_label, content) pairs ──────────────────────
    maze_lines = []

    # Top border
    top = "┌"
    for c in range(cols):
        top += "──"
        if c < cols - 1:
            s_arm = 0 if E in grid[0][c] else 1
            top += _JUNC[(0, s_arm, 1, 1)]
        else:
            top += "┐"
    maze_lines.append(("   ", top))

    for r in range(rows):
        row_label = f"{r + 1:2d} "
        cell_line = "│"
        for c in range(cols):
            cell_line += cell_str(r, c)
            cell_line += " " if E in grid[r][c] else "│"
        maze_lines.append((row_label, cell_line))

        if r < rows - 1:
            e_arm = 0 if S in grid[r][0] else 1
            wall_line = _JUNC[(1, 1, e_arm, 0)]
            for c in range(cols):
                wall_line += "  " if S in grid[r][c] else "──"
                if c < cols - 1:
                    n_arm = 0 if E in grid[r][c]     else 1
                    s_arm = 0 if E in grid[r + 1][c] else 1
                    w_arm = 0 if S in grid[r][c]     else 1
                    e_arm = 0 if S in grid[r][c + 1] else 1
                    wall_line += _JUNC[(n_arm, s_arm, e_arm, w_arm)]
                else:
                    w_arm = 0 if S in grid[r][cols - 1] else 1
                    wall_line += _JUNC[(1, 1, 0, w_arm)]
            maze_lines.append(("   ", wall_line))

    # Bottom border
    bot = "└"
    for c in range(cols):
        bot += "──"
        if c < cols - 1:
            n_arm = 0 if E in grid[rows - 1][c] else 1
            bot += _JUNC[(n_arm, 0, 1, 1)]
        else:
            bot += "┘"
    maze_lines.append(("   ", bot))

    rendered_maze = []
    rendered_maze.append("  " + col_hdr)
    for label, content in maze_lines:
        rendered_maze.append("  " + label + content)

    # ── Stack display below maze ─────────────────────────────────────────────
    stack_lines = []
    if solver.stack:
        depth = len(solver.stack)
        entries = [f"{solver.step_map.get(cell, 1):02x}" for cell in solver.stack]
        robot_hex = entries[-1]
        header = f"Stack ({depth} deep, oldest\u2192newest):"
        joined = " \u2192 ".join(entries) + f"  [\U0001f916 = {robot_hex}]"
        if len(header) + 2 + len(joined) <= 78:
            stack_lines.append("  " + header + "  " + joined)
        else:
            stack_lines.append("  " + header)
            chunk = 8
            for i in range(0, len(entries), chunk):
                group = entries[i : i + chunk]
                suffix = " \u2192" if i + chunk < len(entries) else f"  [\U0001f916 = {robot_hex}]"
                stack_lines.append("    " + " \u2192 ".join(group) + suffix)
    else:
        stack_lines.append("  (stack empty)")

    return rendered_maze, stack_lines


def render_dfs_board(grid, rows, cols, solver):
    """Render watch board in standard flow (used by non-anchored contexts)."""
    maze_lines, stack_lines = _build_dfs_board_lines(grid, rows, cols, solver)
    print()
    for line in maze_lines:
        print(line)
    print()
    for line in stack_lines:
        print(line)
    print()


def _max_stack_rows(rows, cols):
    """Return max stack rows for this maze size with current stack formatting."""
    cells = rows * cols
    header = f"Stack ({cells} deep, oldest→newest):"
    entries = ["ff"] * cells
    joined = " → ".join(entries) + "  [🤖 = ff]"
    if len(header) + 2 + len(joined) <= 78:
        return 1
    chunk = 8
    return 1 + (cells + chunk - 1) // chunk


def _render_watch_frame(step_num, step_lines, maze_lines, stack_lines, max_stack_rows):
    """Render a frame with compact spacing between stack and maze."""
    step_header = _section_header(f"Step {step_num}", ANSI_CYAN)
    stack_header = _section_header("Stack", ANSI_YELLOW)
    prompt = _paint("[Press Enter to continue...]", ANSI_GREEN)
    step_body_rows = 5

    fixed_step_lines = list(step_lines[:step_body_rows])
    if len(fixed_step_lines) < step_body_rows:
        fixed_step_lines.extend([""] * (step_body_rows - len(fixed_step_lines)))

    padded_stack = list(stack_lines)
    desired_pad = max(0, max_stack_rows - len(padded_stack))

    top_lines = [f"  {step_header}"]
    top_lines.extend(fixed_step_lines)
    top_lines.append("")
    top_lines.append(f"  {stack_header}")
    top_lines.extend(padded_stack)

    bottom_lines = [""] + maze_lines + ["", f"  {prompt}"]

    if _USE_ANSI:
        term_rows = shutil.get_terminal_size((100, 40)).lines
        max_top = max(0, term_rows - len(bottom_lines) - 1)

        # Reserve stack space to keep maze position stable, but only if terminal
        # height allows it so step text remains visible.
        room_for_pad = max(0, max_top - len(top_lines))
        apply_pad = min(desired_pad, room_for_pad)
        if apply_pad:
            top_lines.extend([""] * apply_pad)

        shown_top = top_lines[-max_top:] if len(top_lines) > max_top else top_lines
        for line in shown_top:
            print(line)
        print()
        for line in bottom_lines:
            print(line)
    else:
        if desired_pad:
            top_lines.extend([""] * desired_pad)
        print()
        for line in top_lines:
            print(line)
        for line in bottom_lines:
            print(line)


# ---------------------------------------------------------------------------
# Watch-the-robot mode
# ---------------------------------------------------------------------------

def watch_dfs(grid, rows, cols, seed_label=""):
    start = (0, 0)
    finish = (rows - 1, cols - 1)

    print()
    print("=" * 50)
    size_str = f"{rows}×{cols}"
    label = f"  DFS MAZE SOLVER  ({size_str})"
    if seed_label:
        label += f"  seed: {seed_label}"
    print(label)
    print("=" * 50)
    print()
    _narrate_start(rows, cols, start, finish)

    input("  Press Enter to begin, then Enter after each step.\n  ")

    solver = DFSSolver(grid, rows, cols, start, finish)
    step_num = 0
    max_stack_rows = _max_stack_rows(rows, cols)

    while True:
        more = solver.step()
        step_num += 1
        step_lines = _step_lines(solver)
        maze_lines, stack_lines = _build_dfs_board_lines(grid, rows, cols, solver)
        _clear_screen()
        _render_watch_frame(step_num, step_lines, maze_lines, stack_lines, max_stack_rows)
        input()

        if not more:
            break

    if solver.solved:
        path_len = len(solver.stack) - 1  # edges = nodes - 1
        print(f"  🎉 SOLVED!  Path length: {path_len} steps.")
        print(f"  The hex numbers on the board trace the winning path from 🚀 to 🏁.")
    else:
        print("  (No solution found -- this should not happen!)")
    print()


# ---------------------------------------------------------------------------
# Single-keypress input  (arrow keys + letter fallback)
# ---------------------------------------------------------------------------

def _read_key():
    """Read one keypress without requiring Enter.

    Returns one of: N, S, E, W, 'u', 'q', or None (unknown key).
    Arrow keys are handled via their ANSI escape sequences.
    Falls back to a full input() line if termios is unavailable.
    """
    LETTER_MAP = {
        "w": N, "n": N,
        "s": S,
        "d": E, "e": E,
        "a": W,
        "u": "u",
        "q": "q",
    }
    ARROW_MAP = {
        "A": N,   # ESC [ A  = Up
        "B": S,   # ESC [ B  = Down
        "C": E,   # ESC [ C  = Right
        "D": W,   # ESC [ D  = Left
    }

    if not _HAVE_TERMIOS or not sys.stdin.isatty():
        # Fallback: read a whole line (Code.org / piped input)
        line = input().strip().lower()
        return LETTER_MAP.get(line[:1] if line else "", None)

    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
        if ch == "\x1b":                 # escape sequence (arrow key)
            ch2 = sys.stdin.read(1)
            if ch2 == "[":
                ch3 = sys.stdin.read(1)
                return ARROW_MAP.get(ch3, None)
            return None
        if ch == "\x03":                 # Ctrl-C
            raise KeyboardInterrupt
        if ch == "\r" or ch == "\n":     # Enter with no prior char
            return None
        return LETTER_MAP.get(ch.lower(), None)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)


# ---------------------------------------------------------------------------
# Play mode  (human solves the maze)
# ---------------------------------------------------------------------------

def _expected_dfs_action(grid, pos, visited):
    """Return expected DFS action from current state.

    Returns (kind, direction, tried)
      kind: "move" or "backtrack"
      direction: N/S/E/W when kind == "move", else None
      tried: list of (dir, reason) where reason in {"wall", "visited", "move"}
    """
    tried = []
    for d in [W, N, E, S]:
        nr, nc = pos[0] + DR[d], pos[1] + DC[d]
        if d not in grid[pos[0]][pos[1]]:
            tried.append((d, "wall"))
        elif (nr, nc) in visited:
            tried.append((d, "visited"))
        else:
            tried.append((d, "move"))
    for d, reason in tried:
        if reason == "move":
            return "move", d, tried
    return "backtrack", None, tried


def _coach_lines(pos, visited, expected_kind, expected_dir, tried):
    """Return algorithm-coach lines for interactive learning mode."""
    r, c = pos
    lines = []
    lines.append(f"  At {r + 1},{c + 1} we mark this cell as visited.")
    lines.append("  Try directions in absolute order: W, N, E, S.")
    for d, reason in tried:
        arrow = DIR_ARROW[d]
        name = DIR_NAME[d]
        if reason == "wall":
            lines.append(f"  {arrow} {name:5s}: wall")
        elif reason == "visited":
            lines.append(f"  {arrow} {name:5s}: already visited")
        elif d == expected_dir:
            lines.append(f"  {arrow} {name:5s}: open and unvisited  -> next DFS step")
        else:
            lines.append(f"  {arrow} {name:5s}: open and unvisited")

    if expected_kind == "backtrack":
        lines.append("  No unvisited exits remain, so DFS must backtrack one cell.")
    else:
        lines.append(f"  DFS expects: move {DIR_NAME[expected_dir]} now.")
    return lines


def _dfs_reference_stats(grid, rows, cols):
    """Return (moves_with_backtracking, final_path_steps) for DFS baseline."""
    solver = DFSSolver(grid, rows, cols)
    moves = 0
    while True:
        more = solver.step()
        if more:
            moves += 1
        else:
            break
    final_path_steps = len(solver.stack) - 1 if solver.solved else 0
    return moves, final_path_steps


def _matches_expected_dfs(key, expected_kind, expected_dir, pos, history, visited, grid):
    """Return (ok, explanation) for algorithm-learning mode input validation."""
    if expected_kind == "backtrack":
        if key == "u":
            return True, ""
        if key in (N, S, E, W) and len(history) > 1 and key in grid[pos[0]][pos[1]]:
            nr, nc = pos[0] + DR[key], pos[1] + DC[key]
            if (nr, nc) == history[-2]:
                return True, ""
        return False, "DFS would backtrack here: all open neighbors are already visited."

    # expected_kind == "move"
    if key == expected_dir:
        return True, ""
    if key == "u":
        return False, f"DFS moves {DIR_NAME[expected_dir]} here, not backtrack yet."
    if key in (N, S, E, W):
        if key not in grid[pos[0]][pos[1]]:
            return False, f"That is a wall. DFS still expects {DIR_NAME[expected_dir]}."
        nr, nc = pos[0] + DR[key], pos[1] + DC[key]
        if (nr, nc) in visited:
            return False, (
                f"DFS skips visited cells first, then takes {DIR_NAME[expected_dir]} "
                f"(W, N, E, S priority)."
            )
        return False, (
            f"That move is legal, but DFS chooses {DIR_NAME[expected_dir]} first "
            f"because of W, N, E, S priority."
        )
    return False, "Use movement keys or u/q."


def _gentle_nudge_lines(note):
    """Return exactly two display lines for gentle-nudge feedback."""
    indent = " " * len("Gentle nudge:  ")

    wall_prefix = "That is a wall. DFS still expects "
    if note.startswith(wall_prefix):
        direction = note[len(wall_prefix):].rstrip(".")
        return [
            "Gentle nudge:  That is a wall.",
            f"{indent}DFS still expects {direction}.",
        ]

    visited_prefix = "DFS skips visited cells first, then takes "
    if note.startswith(visited_prefix):
        suffix = note[len(visited_prefix):].rstrip(".")
        return [
            "Gentle nudge:  DFS skips visited cells first.",
            f"{indent}Then takes {suffix}.",
        ]

    if note.startswith("DFS would backtrack here"):
        return [
            "Gentle nudge:  DFS would backtrack here.",
            f"{indent}All open neighbors are already visited.",
        ]

    move_prefix = "That move is legal, but DFS chooses "
    if note.startswith(move_prefix):
        direction = note[len(move_prefix):].replace(
            " first because of W, N, E, S priority.", ""
        ).replace(" first", "")
        return [
            "Gentle nudge:  That move is legal.",
            f"{indent}DFS chooses {direction} first (W, N, E, S priority).",
        ]

    if note.startswith("DFS moves ") and note.endswith(" here, not backtrack yet."):
        direction = note.replace("DFS moves ", "").replace(" here, not backtrack yet.", "")
        return [
            f"Gentle nudge:  DFS moves {direction} here.",
            f"{indent}It is not a backtrack step yet.",
        ]

    return [
        f"Gentle nudge:  {note}",
        indent,
    ]

def play_maze(grid, rows, cols, mode="learn"):
    start = (0, 0)
    finish = (rows - 1, cols - 1)
    pos = start
    visited = {start}
    history = [start]     # for undo
    faded = set()         # cells backtracked out of
    moves = 0
    step_map = {start: 1}   # cell -> visit order (shown as hex step numbers)
    push_count = 1
    dfs_moves, dfs_path_steps = _dfs_reference_stats(grid, rows, cols)
    followed_dfs = True
    live_screen = sys.stdout.isatty() and sys.stdin.isatty()
    status_lines = []
    status_color = ""

    def _print_play_banner():
        print()
        if mode == "learn":
            print(_section_header("  ALGORITHM LEARNING MODE", ANSI_CYAN))
        else:
            print(_section_header("  FREE PLAY MODE", ANSI_CYAN))
        if _HAVE_TERMIOS and sys.stdin.isatty():
            print("  Arrow keys to move  |  u = undo  |  q = quit")
            print("  (w/a/s/d also work)")
        else:
            print("  Controls: w/n=North  s=South  d/e=East  a=West  u=undo  q=quit")
            print("  Press Enter after each command.")
        print()

    if not live_screen:
        _print_play_banner()

    while True:
        if live_screen:
            _clear_screen()
            _print_play_banner()

        expected_kind, expected_dir, tried = _expected_dfs_action(grid, pos, visited)

        if mode == "learn":
            print()
            print("  " + _section_header("Algorithm Coach", ANSI_YELLOW))
            for line in _coach_lines(pos, visited, expected_kind, expected_dir, tried):
                print(line)

        active_step_map = {cell: step_map[cell] for cell in history[:-1] if cell in step_map}
        render_maze(grid, rows, cols,
                    robot_pos=pos,
                    step_map=active_step_map,
                    faded_set=faded,
                    start=start, finish=finish,
                    show_axes=True)

        if status_lines:
            for line in status_lines:
                print("  " + _paint(line, status_color))
            print()
        else:
            print()
            print()
            print()

        if pos == finish:
            print(f"  🎉 You solved it in {moves} moves!")
            print(f"  DFS reference (same maze): {dfs_moves} moves, final path {dfs_path_steps} steps.")
            if followed_dfs:
                print(_paint("  🏅 Medal: You followed the DFS algorithm consistently!", ANSI_GREEN))
            else:
                print(_paint("  Nice! You solved it your own way (not strict DFS).", ANSI_GREEN))
            print()
            return

        if _HAVE_TERMIOS and sys.stdin.isatty():
            print("  Move: ", end="", flush=True)
        else:
            print("  Move (w/n/s/d/e/a  u=undo  q=quit): ", end="", flush=True)

        key = _read_key()

        if key == "q":
            print("\n  Quitting play mode.")
            return
        if key == "u":
            if len(history) > 1:
                faded.add(pos)
                history.pop()
                pos = history[-1]
                moves += 1
                status_lines = ["Undid last move."]
                status_color = ANSI_GREEN
            else:
                status_lines = ["Already at the start!"]
                status_color = ANSI_YELLOW
            continue
        if key is None:
            status_lines = ["Unknown command. Use w/n/s/d/e/a, u, or q."]
            status_color = ANSI_YELLOW
            continue

        if mode == "learn":
            ok, note = _matches_expected_dfs(key, expected_kind, expected_dir, pos, history, visited, grid)
            if not ok:
                status_lines = _gentle_nudge_lines(note)
                status_color = ANSI_YELLOW
                continue
        else:
            ok, _ = _matches_expected_dfs(key, expected_kind, expected_dir, pos, history, visited, grid)
            if not ok:
                followed_dfs = False

        # key is one of N, S, E, W
        d = key
        if d not in grid[pos[0]][pos[1]]:
            status_lines = [f"There's a wall to the {DIR_NAME[d]}!"]
            status_color = ANSI_YELLOW
            continue

        nr, nc = pos[0] + DR[d], pos[1] + DC[d]
        next_pos = (nr, nc)

        # Directional move into parent cell counts as DFS backtracking.
        if len(history) > 1 and next_pos == history[-2]:
            faded.add(pos)
            history.pop()
            pos = next_pos
            moves += 1
            status_lines = []
            status_color = ""
            if _HAVE_TERMIOS and sys.stdin.isatty():
                print()  # newline after the inline "Move: " prompt
            continue

        pos = next_pos
        faded.discard(pos)
        if pos not in visited:
            push_count += 1
            step_map[pos] = push_count
        visited.add(pos)
        history.append(pos)
        moves += 1
        status_lines = []
        status_color = ""
        if _HAVE_TERMIOS and sys.stdin.isatty():
            print()  # newline after the inline "Move: " prompt


# ---------------------------------------------------------------------------
# Menu
# ---------------------------------------------------------------------------

def choose_config():
    """Return (grid, rows, cols, seed) based on user choices."""
    print()
    print("=" * 50)
    print("          MAZE SOLVER")
    print("=" * 50)
    print()
    print("  Choose maze size:")
    for key, (r, c, label) in SIZES.items():
        print(f"    {key} -- {label}")
    print()
    while True:
        sz = input("  Size (s, m, or l): ").strip().lower()
        if sz in SIZES:
            break
        print("  Please type s, m, or l.")

    rows, cols, _ = SIZES[sz]

    print()
    seed_input = input("  Maze seed (Enter for random): ").strip()
    if seed_input == "":
        seed = random.randint(1, 9999)
    else:
        try:
            seed = int(seed_input)
        except ValueError:
            seed = hash(seed_input) % 9999

    grid = generate_maze(rows, cols, seed=seed)
    return grid, rows, cols, seed


def main():
    print("\nWelcome to Maze Solver!")

    while True:
        grid, rows, cols, seed = choose_config()

        print()
        print("  What would you like to do?")
        print("    w -- Watch the robot solve the maze (DFS, step by step)")
        print("    a -- Algorithm-learning mode (DFS coach + feedback)")
        print("    f -- Free-play mode (no coach; DFS comparison at the end)")
        print()
        while True:
            choice = input("  Choice (w, a, or f): ").strip().lower()
            if choice in ("w", "a", "f"):
                break
            print("  Please type w, a, or f.")

        if choice == "w":
            watch_dfs(grid, rows, cols, seed_label=str(seed))
        elif choice == "a":
            play_maze(grid, rows, cols, mode="learn")
        else:
            play_maze(grid, rows, cols, mode="free")

        print()
        again = input("  Play again or try a new maze? (y/n): ").strip().lower()
        if again != "y":
            print("  Thanks for playing!")
            break


if __name__ == "__main__":
    main()
