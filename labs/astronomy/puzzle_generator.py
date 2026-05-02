"""Puzzle Generator — teacher tool for the Astronomy Lab.

Generates a signal ID constraint puzzle with exactly one solution.
Prints a student-facing handout and a teacher key with the answer
and pruning statistics (how much each rule narrows down the candidates).

Usage:
    python puzzle_generator.py               # 5-digit puzzle, random seed
    python puzzle_generator.py --digits 3    # 3-digit warm-up
    python puzzle_generator.py --digits 7 --seed 42
    python puzzle_generator.py --count 3     # three different puzzles
"""

import argparse
import itertools
import random
import sys

PRIMES = {2, 3, 5, 7}
MAX_DIGITS = 7   # above this the permutation pool gets very large


# ─────────────────────────────────────────────────────────────
# Rule representation
# ─────────────────────────────────────────────────────────────

class Rule:
    """A named constraint on a list of digits, with metadata for formatting."""

    def __init__(self, description, fn, kind, params):
        self.description = description
        self._fn = fn
        # kind and params are used by format_teacher_key to generate the
        # Python verification snippet.  They are NOT needed by signal_solver.py's
        # Rule class, which only needs description + fn.
        self.kind = kind
        self.params = params

    def check(self, digits):
        return self._fn(digits)


def _no_repeat():
    return Rule(
        "All digits are different",
        lambda d: len(set(d)) == len(d),
        "no_repeat", {},
    )

def _digit_property(pos, prop):
    if prop == "prime":
        desc = f"Digit {pos + 1} is a prime number  (2, 3, 5, or 7)"
        fn = lambda d, p=pos: d[p] in PRIMES
    elif prop == "even":
        desc = f"Digit {pos + 1} is even"
        fn = lambda d, p=pos: d[p] % 2 == 0
    else:
        desc = f"Digit {pos + 1} is odd"
        fn = lambda d, p=pos: d[p] % 2 == 1
    return Rule(desc, fn, "digit_property", {"pos": pos, "prop": prop})

def _digit_offset(pos_a, pos_b, offset):
    if offset > 0:
        desc = f"Digit {pos_b + 1} is {offset} more than digit {pos_a + 1}"
    else:
        desc = f"Digit {pos_b + 1} is {-offset} less than digit {pos_a + 1}"
    return Rule(
        desc,
        lambda d, a=pos_a, b=pos_b, k=offset: d[b] == d[a] + k,
        "digit_offset", {"pos_a": pos_a, "pos_b": pos_b, "offset": offset},
    )

def _digit_double(pos_a, pos_b):
    return Rule(
        f"Digit {pos_b + 1} is twice digit {pos_a + 1}",
        lambda d, a=pos_a, b=pos_b: d[b] == 2 * d[a],
        "digit_double", {"pos_a": pos_a, "pos_b": pos_b},
    )

def _sum_equals(target):
    return Rule(
        f"The sum of all digits is {target}",
        lambda d, t=target: sum(d) == t,
        "sum_equals", {"target": target},
    )


# ─────────────────────────────────────────────────────────────
# Candidate pool
# ─────────────────────────────────────────────────────────────

def _initial_pool(n_digits):
    """All n-digit no-repeat tuples with no leading zeros.

    For n ≤ 10 uses permutations (no-repeat built in).
    Returns a Python set for fast membership testing.
    """
    # itertools.permutations(range(10), n) generates every ordered selection
    # of n distinct digits from 0–9 — exactly the set of valid no-repeat codes.
    # Building a set (not a list) makes the later "answer in pool" checks O(1).
    return {
        p for p in itertools.permutations(range(10), n_digits)
        if p[0] != 0      # exclude leading-zero codes like (0, 3, 7)
    }


def _filter(pool, rule):
    return {p for p in pool if rule.check(list(p))}


# ─────────────────────────────────────────────────────────────
# Rule vocabulary
# ─────────────────────────────────────────────────────────────

def _candidate_rules(answer, n_digits):
    """Every rule from the vocabulary that the answer satisfies."""
    d = answer
    rules = []

    # Build every rule the answer could be the SUBJECT of.
    # The generator will later choose a small subset of these that together
    # uniquely identify the answer.

    # Digit property rules
    for pos in range(n_digits):
        if d[pos] in PRIMES:
            rules.append(_digit_property(pos, "prime"))
        if d[pos] % 2 == 0:
            rules.append(_digit_property(pos, "even"))
        if d[pos] % 2 == 1:
            rules.append(_digit_property(pos, "odd"))

    # Local relationship rules (offsets 1–5, double)
    for a in range(n_digits):
        for b in range(n_digits):
            if a == b:
                continue
            offset = d[b] - d[a]
            if 1 <= abs(offset) <= 5:
                rules.append(_digit_offset(a, b, offset))
            if d[a] > 0 and d[b] == 2 * d[a]:
                rules.append(_digit_double(a, b))

    # Global sum
    rules.append(_sum_equals(sum(d)))

    return rules


# ─────────────────────────────────────────────────────────────
# Generator
# ─────────────────────────────────────────────────────────────

def generate_puzzle(n_digits, seed=None):
    """Return (answer, rules, pruning_log) for a uniquely-solvable puzzle.

    answer       — list of ints (the unique solution)
    rules        — list of Rule objects in the order they were added
    pruning_log  — list of (description, pool_size_after) pairs

    The generator greedily adds whichever rule from the vocabulary prunes
    the most candidates, stopping as soon as exactly one solution remains.
    """
    if n_digits < 2 or n_digits > MAX_DIGITS:
        raise ValueError(
            f"n_digits must be between 2 and {MAX_DIGITS} (got {n_digits}). "
            f"Larger values make the permutation pool too big for interactive use."
        )

    rng = random.Random(seed)

    # Try many random answers; some will be impossible to uniquely pin down
    # with the available rule vocabulary, so we retry with a fresh answer.
    for _attempt in range(400):
        answer = tuple(rng.sample(range(10), n_digits))
        if answer[0] == 0:
            continue

        # Start with the full no-repeat pool
        pool = _initial_pool(n_digits)
        if answer not in pool:
            continue                # shouldn't happen, but be safe

        chosen = []
        # Record initial size; the no_repeat rule is implicit in this pool
        pruning_log = [("Starting pool (all no-repeat, no leading zeros)", len(pool))]

        # Always include no_repeat on the student handout
        chosen.append(_no_repeat())

        candidates = _candidate_rules(list(answer), n_digits)
        # Shuffle so that when two rules prune equally, the tie-break is random
        # rather than always favouring the same rule type.
        rng.shuffle(candidates)

        while len(pool) > 1 and candidates:
            best_rule = None
            best_size = len(pool)

            for rule in candidates:
                new_pool = _filter(pool, rule)
                # Only consider rules that keep the answer alive in the pool.
                # A rule that would eliminate the answer is wrong, not useful.
                if answer in new_pool and len(new_pool) < best_size:
                    best_size = len(new_pool)
                    best_rule = rule

            if best_rule is None:
                break                # no remaining rule helps

            pool = _filter(pool, best_rule)
            chosen.append(best_rule)
            pruning_log.append((best_rule.description, len(pool)))
            candidates.remove(best_rule)

        if len(pool) == 1:
            return list(answer), chosen, pruning_log

    raise RuntimeError(
        f"Could not generate a uniquely-solvable puzzle for {n_digits} digits "
        f"after 400 attempts. Try a different --seed or --digits value."
    )


# ─────────────────────────────────────────────────────────────
# Formatting
# ─────────────────────────────────────────────────────────────

_STORY = (
    "In 1977, NASA launched Voyager carrying a Golden Record —\n"
    "a message to the cosmos. Engineers also programmed a secret\n"
    "authentication ID so the probe could verify its own identity\n"
    "if ever found again — by us, or anyone else.\n"
    "\n"
    "Decades later, a faint signal has reached our receivers.\n"
    "The probe is alive. But the ID digits are scrambled.\n"
    "\n"
    "All that survived are the original engineering rules.\n"
    "You are the decoding team."
)

def _box(title, width=58):
    return [
        "┌" + "─" * (width - 2) + "┐",
        "│" + f"  {title}".center(width - 2) + "│",
        "└" + "─" * (width - 2) + "┘",
    ]


def format_student_handout(n_digits, rules):
    """Return the student-facing puzzle as a printable string."""
    lines = _box("MISSION: DECODE THE SIGNAL")
    lines.append("")
    lines.extend(_STORY.splitlines())
    lines.append("")
    lines.append(f"The signal ID is {n_digits} digits long.")
    lines.append("")
    lines.append("THE RULES:")

    for i, r in enumerate(rules, 1):
        lines.append(f"  {i}. {r.description}")

    lines.append("")
    lines.append("YOUR MISSION: Find the signal ID.")
    lines.append("")
    blanks = "  ".join(["__"] * n_digits)
    lines.append(f"  Signal ID:  {blanks}")
    lines.append("")
    return "\n".join(lines)


def format_teacher_key(n_digits, answer, rules, pruning_log):
    """Return the teacher key with answer, pruning stats, and verification code."""
    lines = _box("TEACHER KEY")
    lines.append("")

    answer_spaced = "  ".join(map(str, answer))
    answer_compact = "".join(map(str, answer))
    lines.append(f"  Answer:  {answer_spaced}   →  {answer_compact}")
    lines.append("")

    # Pruning table
    lines.append("  How the rules narrow down the candidates:")
    lines.append("")
    start_desc, start_size = pruning_log[0]
    lines.append(f"  {'Start':<40}  {start_size:>8,} candidates")
    for desc, size in pruning_log[1:]:
        lines.append(f"  + {desc:<38}  {size:>8,} remaining")
    lines.append("")

    # Verification snippet
    lines.append("  Quick verification (Python):")
    lines.append(f"    d = {list(answer)}")
    for r in rules:
        if r.kind == "no_repeat":
            lines.append(f"    assert len(set(d)) == len(d)           # all different")
        elif r.kind == "sum_equals":
            lines.append(f"    assert sum(d) == {r.params['target']:<27}# sum check")
        elif r.kind == "digit_property":
            p, prop = r.params["pos"], r.params["prop"]
            if prop == "prime":
                lines.append(f"    assert d[{p}] in {{2,3,5,7}}                    # digit {p+1} prime")
            elif prop == "even":
                lines.append(f"    assert d[{p}] % 2 == 0                         # digit {p+1} even")
            else:
                lines.append(f"    assert d[{p}] % 2 == 1                         # digit {p+1} odd")
        elif r.kind == "digit_offset":
            a, b, k = r.params["pos_a"], r.params["pos_b"], r.params["offset"]
            lines.append(f"    assert d[{b}] == d[{a}] + {k:<26}# {r.description.lower()}")
        elif r.kind == "digit_double":
            a, b = r.params["pos_a"], r.params["pos_b"]
            lines.append(f"    assert d[{b}] == 2 * d[{a}]                       # {r.description.lower()}")
    lines.append("")
    lines.append("  To see the solver in action:")
    lines.append("    python signal_solver.py")
    lines.append("")
    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Generate a signal ID puzzle with exactly one solution.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python puzzle_generator.py --digits 3          # warm-up\n"
            "  python puzzle_generator.py --digits 5 --seed 7 # reproducible\n"
            "  python puzzle_generator.py --count 3           # three puzzles\n"
        ),
    )
    parser.add_argument("--digits", type=int, default=5,
                        help=f"Code length, 2–{MAX_DIGITS} (default: 5)")
    parser.add_argument("--seed", type=int, default=None,
                        help="Random seed — repeat to get the same puzzle again")
    parser.add_argument("--count", type=int, default=1,
                        help="How many puzzles to generate (default: 1)")
    args = parser.parse_args()

    if args.digits < 2 or args.digits > MAX_DIGITS:
        print(f"Error: --digits must be between 2 and {MAX_DIGITS} (got {args.digits})")
        sys.exit(1)

    sep = "═" * 60

    for i in range(args.count):
        # When generating multiple puzzles with a fixed seed, offset it so
        # they're all different but still reproducible.
        seed = (args.seed + i) if args.seed is not None else None

        if args.count > 1:
            print()
            print(sep)
            print(f"  PUZZLE {i + 1} of {args.count}")

        try:
            answer, rules, log = generate_puzzle(args.digits, seed=seed)
        except (ValueError, RuntimeError) as e:
            print(f"Error: {e}")
            sys.exit(1)

        print()
        print(format_student_handout(args.digits, rules))
        print()
        print(format_teacher_key(args.digits, answer, rules, log))

        if args.count > 1:
            print(sep)

    if args.count == 1:
        seed_note = str(args.seed) if args.seed is not None else "(random — use --seed to reproduce)"
        print(f"  Seed used: {seed_note}")
        print()


if __name__ == "__main__":
    main()
