"""Text Tower of Hanoi (Code.org-compatible, standard library only).

Commands:
  - Type two digits like 13 to move the top disk from pillar 1 to pillar 3.
  - Type h for help, q to quit.
  - At the start menu, type t to enter Teach Me mode.

Goal:
  - Move all disks from pillar 1 to pillar 3.
  - Never place a larger disk on top of a smaller one.
"""

# Each disk size maps to a letter: size 1 = A (smallest), 2 = B, etc.
DISK_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def min_moves_for(n):
    return (2 ** n) - 1


def make_disk(size, col_width):
    """Disk of size N uses letter N of alphabet (1=A, 2=B, ...), centered."""
    letter = DISK_LETTERS[size - 1]
    disk = letter * (2 * size + 1)
    return disk.center(col_width)


def make_rod(col_width):
    return "|".center(col_width)


def render_board(towers, disk_count, title="TOWER OF HANOI"):
    """Draw the three towers from top to bottom with an optional title."""
    col_width = (2 * disk_count + 1) + 2
    gap = "   "
    full_width = col_width * 3 + len(gap) * 2

    print()
    print("=" * full_width)
    print(title.center(full_width))
    print("=" * full_width)

    for row in range(disk_count - 1, -1, -1):
        parts = []
        for tower in towers:
            if row < len(tower):
                parts.append(make_disk(tower[row], col_width))
            else:
                parts.append(make_rod(col_width))
        print(gap.join(parts))

    print("-" * full_width)
    print(gap.join([
        "1".center(col_width),
        "2".center(col_width),
        "3".center(col_width),
    ]))
    print()


def print_big_x():
    """Show a large ASCII X for invalid moves."""
    art = [
        "XX       XX",
        " XX     XX ",
        "  XX   XX  ",
        "   XX XX   ",
        "    XXX    ",
        "   XX XX   ",
        "  XX   XX  ",
        " XX     XX ",
        "XX       XX",
    ]
    print()
    for line in art:
        print("   " + line)
    print("   INVALID MOVE!")
    print()


def parse_move(command):
    """Parse a command like '13' -> (0, 2), or return None."""
    if len(command) != 2 or not command.isdigit():
        return None
    src, dst = int(command[0]), int(command[1])
    if src not in (1, 2, 3) or dst not in (1, 2, 3) or src == dst:
        return None
    return src - 1, dst - 1


def is_valid_move(towers, src, dst):
    if not towers[src]:
        return False
    if not towers[dst]:
        return True
    return towers[src][-1] < towers[dst][-1]


def medal_for_result(disk_count, successful_moves, mistakes):
    target = min_moves_for(disk_count)
    if successful_moves == target and mistakes == 0:
        return "gold"
    if successful_moves == target and mistakes > 0:
        return "silver"
    return "none"


def print_medal(medal):
    if medal == "gold":
        print("  ****************************")
        print("  *       GOLD MEDAL!        *")
        print("  *   Perfect solution!      *")
        print("  *   Zero mistakes!  (*)    *")
        print("  ****************************")
    elif medal == "silver":
        print("  ****************************")
        print("  *      SILVER MEDAL!       *")
        print("  *   Minimal solution!      *")
        print("  *  Try for 0 mistakes next *")
        print("  *       to get gold.       *")
        print("  ****************************")
    print()


def _solve_steps(n, src, aux, dst):
    """Return the optimal move list for n disks as (src_idx, dst_idx) pairs."""
    if n == 0:
        return []
    return (
        _solve_steps(n - 1, src, dst, aux)
        + [(src, dst)]
        + _solve_steps(n - 1, aux, src, dst)
    )


def iterative_steps(n):
    """Return the optimal move list using the easy iterative rule.

    The easy rule (no recursion required):
      - Odd-numbered moves:  move disk A one step along its cycle.
            n odd  -> cycle  1 → 3 → 2 → 1 → ...
            n even -> cycle  1 → 2 → 3 → 1 → ...
      - Even-numbered moves: make the only other legal move.
    """
    cycle = [0, 2, 1] if n % 2 == 1 else [0, 1, 2]
    towers = [list(range(n, 0, -1)), [], []]
    steps = []
    small_pos_idx = 0  # index into cycle: disk A is at cycle[small_pos_idx % 3]
    for move_num in range(min_moves_for(n)):
        if move_num % 2 == 0:
            # Move disk A one step forward in the cycle.
            src = cycle[small_pos_idx % 3]
            dst = cycle[(small_pos_idx + 1) % 3]
            small_pos_idx += 1
        else:
            # Make the only legal move that does NOT involve disk A.
            small_pos = cycle[small_pos_idx % 3]
            p0, p1 = [p for p in range(3) if p != small_pos]
            top0 = towers[p0][-1] if towers[p0] else float('inf')
            top1 = towers[p1][-1] if towers[p1] else float('inf')
            src, dst = (p0, p1) if top0 < top1 else (p1, p0)
        disk = towers[src].pop()
        towers[dst].append(disk)
        steps.append((src, dst))
    return steps


def _annotate_recursive_steps(n, src, aux, dst):
    """Like _solve_steps but returns (src, dst, annotation) triples.

    Each move is labeled with the top-level phase it belongs to:
      Step 1/3: clearing the n-1 smaller disks off the biggest one
      Step 2/3: moving the biggest disk to its goal pillar
      Step 3/3: stacking the n-1 smaller disks back on top
    """
    if n == 0:
        return []
    big = DISK_LETTERS[n - 1]
    count = n - 1
    noun = f"{count} disk{'s' if count != 1 else ''}"
    phase1 = f"Step 1/3 — clear {noun} off disk {big} (make room)"
    phase2 = f"Step 2/3 — move disk {big} to its goal  (pillar {dst + 1})"
    phase3 = f"Step 3/3 — stack {noun} back onto disk {big}"
    sub1 = _annotate_recursive_steps(n - 1, src, dst, aux)
    sub3 = _annotate_recursive_steps(n - 1, aux, src, dst)
    return (
        [(s, d, phase1) for s, d, _ in sub1]
        + [(src, dst, phase2)]
        + [(s, d, phase3) for s, d, _ in sub3]
    )


def _annotate_iterative_steps(n):
    """Like iterative_steps but returns (src, dst, annotation) triples.

    Each move is labeled with which rule produced it:
      Rule 1 (odd moves):  slide disk A one step along its fixed cycle
      Rule 2 (even moves): make the only legal move not involving disk A
    """
    cycle = [0, 2, 1] if n % 2 == 1 else [0, 1, 2]
    cycle_str = "→".join(str(p + 1) for p in cycle) + "→..."
    towers = [list(range(n, 0, -1)), [], []]
    steps = []
    small_pos_idx = 0
    for move_num in range(min_moves_for(n)):
        if move_num % 2 == 0:
            src = cycle[small_pos_idx % 3]
            dst = cycle[(small_pos_idx + 1) % 3]
            annotation = (
                f"Rule 1 (odd move):  slide disk A  "
                f"{src + 1}→{dst + 1}  "
                f"[repeating cycle: {cycle_str}]"
            )
            small_pos_idx += 1
        else:
            small_pos = cycle[small_pos_idx % 3]
            p0, p1 = [p for p in range(3) if p != small_pos]
            top0 = towers[p0][-1] if towers[p0] else float('inf')
            top1 = towers[p1][-1] if towers[p1] else float('inf')
            src, dst = (p0, p1) if top0 < top1 else (p1, p0)
            annotation = (
                f"Rule 2 (even move): only legal non-A move  "
                f"{src + 1}→{dst + 1}  "
                f"[disk A is resting]"
            )
        disk = towers[src].pop()
        towers[dst].append(disk)
        steps.append((src, dst, annotation))
    return steps


def choose_watch_config():
    """Prompt for disk count + solution method; return (n, method_str)."""
    print()
    print("=" * 50)
    print("        WATCH COMPUTER SOLVE")
    print("=" * 50)
    print()
    print("  Choose number of disks:")
    print("    3 --  3 disks (min  7 moves)")
    print("    4 --  4 disks (min 15 moves)")
    print("    5 --  5 disks (min 31 moves)")
    print()
    while True:
        choice = input("  Disks (3, 4, or 5): ").strip()
        if choice in ("3", "4", "5"):
            n = int(choice)
            break
        print("  Please type 3, 4, or 5.")

    if n % 2 == 1:
        cycle_note = "1 → 3 → 2 → 1 → ..."
    else:
        cycle_note = "1 → 2 → 3 → 1 → ..."

    print()
    print("  Choose solution method:")
    print("    r -- Recursive algorithm  (classic computer-science approach)")
    print("    e -- Easy rule            (no mental recursion needed!)")
    print(f"         Odd moves:  move disk A one step along its cycle ({cycle_note})")
    print( "         Even moves: make the only other legal move")
    print( "         Repeat until solved!")
    print()
    while True:
        method = input("  Method (r or e): ").strip().lower()
        if method in ("r", "e"):
            break
        print("  Please type r or e.")

    return n, ("iterative" if method == "e" else "recursive")


def watch_solve(disk_count, method):
    """Animate a computer solution step by step with per-move explanations."""
    if method == "iterative":
        steps = _annotate_iterative_steps(disk_count)
        method_name = "Easy Rule"
    else:
        steps = _annotate_recursive_steps(disk_count, 0, 1, 2)
        method_name = "Recursive Algorithm"

    total = min_moves_for(disk_count)
    print()
    print(f"  {disk_count}-disk Hanoi  --  {method_name}")
    print(f"  Total moves: {total}")
    print()
    input("  Press Enter to start the animation ...  ")

    towers = [list(range(disk_count, 0, -1)), [], []]
    render_board(towers, disk_count, title="STARTING POSITION")

    for i, (src, dst, annotation) in enumerate(steps):
        print(f"  Move {i + 1}/{total}:  {annotation}")
        input(f"  Execute: pillar {src + 1} --> pillar {dst + 1}   [Press Enter]  ")
        disk = towers[src].pop()
        towers[dst].append(disk)
        render_board(towers, disk_count,
                     title=f"After move {i + 1}/{total}: {src + 1} --> {dst + 1}")

    print(f"  Solved in exactly {total} moves!")
    print()


def choose_mode():
    """Return an int (3/4/5) for play, 'watch', or 'teach'."""
    print()
    print("=" * 50)
    print("         TOWER OF HANOI")
    print("=" * 50)
    print()
    print("  3 -- Play 3-disk Hanoi  (min  7 moves)")
    print("  4 -- Play 4-disk Hanoi  (min 15 moves)")
    print("  5 -- Play 5-disk Hanoi  (min 31 moves)")
    print("  s -- Watch computer solve  (choose 3/4/5 + method)")
    print("  t -- Teach Me: learn the rules and strategy")
    print()
    while True:
        choice = input("  Choose (3, 4, 5, s, or t): ").strip().lower()
        if choice in ("3", "4", "5"):
            return int(choice)
        if choice == "s":
            return "watch"
        if choice == "t":
            return "teach"
        print("  Please type 3, 4, 5, s, or t.")


def teach_me():
    """Interactive walkthrough: rules, strategy, animated demo, then free play."""

    def pause():
        input("\n  [Press Enter to continue...]\n")

    # -- Introduction ----------------------------------------------------------
    print()
    print("=" * 50)
    print("    TEACH ME: TOWERS OF HANOI")
    print("=" * 50)
    print()
    print("  The Towers of Hanoi is one of the most famous")
    print("  puzzles in computer science and mathematics.")
    print()
    print("  Three pillars. A stack of disks. One simple goal:")
    print("  move every disk from pillar 1 to pillar 3.")
    pause()

    # -- Show the start board --------------------------------------------------
    demo_n = 3
    demo_towers = [list(range(demo_n, 0, -1)), [], []]
    print("  Here is what a 3-disk puzzle looks like to start:")
    render_board(demo_towers, demo_n, title="START POSITION")
    print("  Disks are labeled A (smallest) through C (largest).")
    print("  Each disk label is wider than the one above it,")
    print("  so you can always tell which disk is bigger.")
    pause()

    # -- Rules -----------------------------------------------------------------
    print("  THE RULES (only three of them!):")
    print()
    print("  1. Move only ONE disk at a time.")
    print("  2. Only the TOP disk of a pillar can be moved.")
    print("  3. NEVER place a larger disk on top of a smaller one.")
    print()
    print("  Simple rules -- surprisingly tricky puzzle!")
    pause()

    # -- Show an illegal move --------------------------------------------------
    print("  For example, you CANNOT move C onto B:")
    bad_towers = [[3], [2], [1]]
    render_board(bad_towers, demo_n, title="ILLEGAL: C cannot go on top of B!")
    print("  C is wider than B, so that move is forbidden.")
    pause()

    # -- Minimum moves formula -------------------------------------------------
    print("  HOW MANY MOVES DOES IT TAKE?")
    print()
    print("  3 disks:  min  7 moves   (2^3 - 1)")
    print("  4 disks:  min 15 moves   (2^4 - 1)")
    print("  5 disks:  min 31 moves   (2^5 - 1)")
    print()
    print("  The formula is always:  2^n - 1")
    print()
    print("  Fun fact: legend says monks move 64 golden disks.")
    print("  2^64 - 1 moves at 1 per second = 585 BILLION years.")
    pause()

    # -- The recursive algorithm -----------------------------------------------
    print("  THE WINNING STRATEGY -- recursive thinking:")
    print()
    print("  To move N disks from pillar A to pillar C")
    print("  (using B as your spare pillar):")
    print()
    print("    STEP 1:  Move the top N-1 disks   A --> B")
    print("             (use C as the spare)")
    print()
    print("    STEP 2:  Move the BIG bottom disk  A --> C")
    print()
    print("    STEP 3:  Move the top N-1 disks   B --> C")
    print("             (use A as the spare)")
    print()
    print("  Each sub-problem is just a SMALLER Hanoi puzzle!")
    print("  This technique -- solving a problem by breaking it")
    print("  into smaller versions of itself -- is called RECURSION.")
    pause()

    # -- Trace the 3-disk case -------------------------------------------------
    print("  LET'S TRACE THE STRATEGY FOR 3 DISKS (A=small, C=big):")
    print()
    print("  Goal: move A, B, C from pillar 1 to pillar 3")
    print()
    print("  STEP 1 -- move 2 disks (A and B) from 1 to 2:")
    print("      1a.  Move A  :  1 --> 3  (3 is our spare)")
    print("      1b.  Move B  :  1 --> 2")
    print("      1c.  Move A  :  3 --> 2")
    print()
    print("  STEP 2 -- move C (the biggest) :  1 --> 3")
    print()
    print("  STEP 3 -- move 2 disks (A and B) from 2 to 3:")
    print("      3a.  Move A  :  2 --> 1  (1 is now the spare)")
    print("      3b.  Move B  :  2 --> 3")
    print("      3c.  Move A  :  1 --> 3")
    print()
    print("  Total: 7 moves -- the minimum possible.")
    pause()

    # -- Invite them to watch the computer solve -------------------------------
    print("  Want to watch it animated step by step?")
    print("  From the main menu, choose  s -- Watch computer solve.")
    print("  You can pick the recursive method or the easy rule!")
    pause()

    # -- Free play -------------------------------------------------------------
    print("  YOUR TURN -- try a 3-disk puzzle on your own!")
    print()
    print("  Remember the strategy:")
    print("    1. Move N-1 disks to the spare pillar.")
    print("    2. Move the biggest disk to the goal.")
    print("    3. Move N-1 disks from the spare to the goal.")
    print()
    print("  Gold medal:   7 moves, zero invalid attempts.")
    print("  Silver medal: 7 moves, but some invalid attempts.")
    print()
    play_game(3)


def play_game(disk_count):
    """Run a complete game for the given number of disks."""
    towers = [list(range(disk_count, 0, -1)), [], []]
    successful_moves = 0
    mistakes = 0
    target_moves = min_moves_for(disk_count)

    print()
    print(f"  Minimum possible moves: {target_moves}")
    print("  Type a move like 13, or h for help, q to quit.")

    while True:
        render_board(towers, disk_count)

        if len(towers[2]) == disk_count:
            print("  SOLVED!")
            print(f"  Successful moves:  {successful_moves}  (min: {target_moves})")
            print(f"  Invalid attempts:  {mistakes}")
            medal = medal_for_result(disk_count, successful_moves, mistakes)
            if medal == "none":
                print("  No medal this time -- try for the minimal solution!")
            else:
                print_medal(medal)
            break

        command = input("  Move (e.g. 13), h, or q: ").strip().lower()

        if command == "q":
            print("  Goodbye!")
            break

        if command == "h":
            print()
            print("  Type two digits: source pillar then destination.")
            print("  Example: 13 moves the top disk from pillar 1 to pillar 3.")
            print("  Rule: never place a LARGER disk on a SMALLER one.")
            print()
            continue

        # Every non-help, non-quit command counts as an attempt.
        move = parse_move(command)
        if move is None:
            print_big_x()
            mistakes += 1
            continue

        src, dst = move
        if not is_valid_move(towers, src, dst):
            print_big_x()
            mistakes += 1
            continue

        disk = towers[src].pop()
        towers[dst].append(disk)
        successful_moves += 1


def main():
    print("\nWelcome to Tower of Hanoi!")
    while True:
        mode = choose_mode()
        if mode == "teach":
            teach_me()
        elif mode == "watch":
            n, method = choose_watch_config()
            watch_solve(n, method)
        else:
            play_game(mode)

        print()
        again = input("  Play again or try another mode? (y/n): ").strip().lower()
        if again != "y":
            print("  Thanks for playing!")
            break


if __name__ == "__main__":
    main()
