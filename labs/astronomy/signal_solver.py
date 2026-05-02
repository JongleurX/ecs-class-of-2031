"""Signal ID Solver — Astronomy Lab reference implementation.

Story: A probe launched in 1977 has started transmitting again after decades
of silence. The authentication signal is garbled, but the original engineering
rules survived. Decode the signal ID.

This file provides:
  - Rule building blocks (digit properties, relationships, checksum)
  - Two solvers: brute-force and smart (permutation-based)
  - A timing comparison showing how speed scales with code length

Run directly:
    python signal_solver.py
"""

import argparse
import itertools
import sys
import time

PRIMES = {2, 3, 5, 7}


# ─────────────────────────────────────────────────────────────
# Rule building blocks
# ─────────────────────────────────────────────────────────────
#
# A Rule is a named check on a list of digits.
# Use the helper functions below to build rules.
#
# Example:
#   rules = [no_repeat(), digit_is_prime(2), digit_sum_equals(15)]
#   solve_brute(5, rules)

class Rule:
    def __init__(self, description, fn):
        self.description = description
        self._fn = fn       # stored as _fn (private) so callers use .check() not ._fn()

    def check(self, digits):
        """Return True if these digits satisfy this rule."""
        return self._fn(digits)

    def __repr__(self):
        return f"Rule({self.description!r})"


def no_repeat():
    """All digits in the code are different."""
    return Rule(
        "All digits are different",
        lambda d: len(set(d)) == len(d),
    )

def digit_is_prime(pos):
    """Digit at position pos (0-based) is 2, 3, 5, or 7."""
    return Rule(
        f"Digit {pos + 1} is a prime number  (2, 3, 5, or 7)",
        # "p=pos" captures the current value of pos as a default argument.
        # Without it, all lambdas would close over the same variable and
        # see only the last value it had after the loop finished.
        lambda d, p=pos: d[p] in PRIMES,
    )

def digit_is_even(pos):
    """Digit at position pos is even."""
    return Rule(
        f"Digit {pos + 1} is even",
        lambda d, p=pos: d[p] % 2 == 0,  # same default-arg capture as above
    )

def digit_is_odd(pos):
    """Digit at position pos is odd."""
    return Rule(
        f"Digit {pos + 1} is odd",
        lambda d, p=pos: d[p] % 2 == 1,
    )

def digit_offset(pos_a, pos_b, offset):
    """d[pos_b] == d[pos_a] + offset  (offset may be negative)."""
    if offset > 0:
        desc = f"Digit {pos_b + 1} is {offset} more than digit {pos_a + 1}"
    else:
        desc = f"Digit {pos_b + 1} is {-offset} less than digit {pos_a + 1}"
    return Rule(desc, lambda d, a=pos_a, b=pos_b, k=offset: d[b] == d[a] + k)

def digit_double(pos_a, pos_b):
    """d[pos_b] == 2 * d[pos_a]."""
    return Rule(
        f"Digit {pos_b + 1} is twice digit {pos_a + 1}",
        lambda d, a=pos_a, b=pos_b: d[b] == 2 * d[a],
    )

def digit_sum_equals(target):
    """Sum of all digits equals target."""
    return Rule(
        f"The sum of all digits is {target}",
        lambda d, t=target: sum(d) == t,
    )

def whole_divisible_by(m):
    """The number formed by all digits (left to right) is divisible by m."""
    return Rule(
        f"The whole number is divisible by {m}",
        lambda d, m=m: int("".join(map(str, d))) % m == 0,
    )


# ─────────────────────────────────────────────────────────────
# Brute-force solver
# ─────────────────────────────────────────────────────────────

def solve_brute(n_digits, rules):
    """Try every n-digit integer from 10^(n-1) to 10^n.

    Simple and obvious, but the number of candidates grows as 10^n,
    so it gets slow quickly for larger codes.

    Returns a list of all integers satisfying every rule.
    """
    solutions = []
    lo = 10 ** (n_digits - 1)   # first n-digit number (e.g. 1000 for n=4)
    hi = 10 ** n_digits          # first (n+1)-digit number — range() stops before this
    for n in range(lo, hi):
        d = [int(c) for c in str(n)]    # split integer into a list of digits
        if all(r.check(d) for r in rules):
            solutions.append(n)
    return solutions


# ─────────────────────────────────────────────────────────────
# Smart solver
# ─────────────────────────────────────────────────────────────

def solve_smart(n_digits, rules):
    """Use digit permutations instead of raw integer enumeration.

    For n_digits ≤ 10: iterates over permutations of the 10 digits taken
    n at a time. This automatically satisfies no-repeat and cuts the search
    space dramatically — at n=10 it's 3.6 million instead of 9 billion.

    For n_digits > 10: digits can repeat so falls back to itertools.product.

    Returns a list of all integers satisfying every rule.
    """
    solutions = []
    if n_digits <= 10:
        # permutations(range(10), n) yields every ordered selection of n
        # distinct digits from 0–9.  This is a strict superset of all valid
        # no-repeat codes, so we never miss a solution — and we never test
        # a number that violates no-repeat (saving ~75% of the work at n=10).
        for perm in itertools.permutations(range(10), n_digits):
            if perm[0] == 0:
                continue                # skip leading zeros (e.g. 0123 is not a 4-digit number)
            if all(r.check(list(perm)) for r in rules):
                solutions.append(int("".join(map(str, perm))))
    else:
        # Beyond 10 digits, digits must repeat (only 10 distinct values exist),
        # so we fall back to the full Cartesian product.
        for perm in itertools.product(range(10), repeat=n_digits):
            if perm[0] == 0:
                continue
            if all(r.check(list(perm)) for r in rules):
                solutions.append(int("".join(map(str, perm))))
    return solutions


# ─────────────────────────────────────────────────────────────
# Timing comparison
# ─────────────────────────────────────────────────────────────

def _candidate_counts(n_digits):
    # Brute: 10^n total integers minus those with fewer digits (leading zeros).
    brute = 10 ** n_digits - 10 ** (n_digits - 1)
    if n_digits <= 10:
        # Smart: P(10, n) = 10 × 9 × 8 × … (n terms) — the permutation count.
        # This is the number of ways to choose n distinct digits in order from 0–9.
        smart = 1
        for k in range(10, 10 - n_digits, -1):
            smart *= k
    else:
        smart = 10 ** n_digits  # repeats allowed; full product space
    return brute, smart


def compare(n_digits, rules, label="", max_brute_digits=5):
    """Run both solvers and print a side-by-side timing table.

    Set max_brute_digits lower to skip brute-force on large puzzles
    where it would take too long to complete in a classroom setting.
    """
    heading = label or f"{n_digits}-digit puzzle"
    bar = "─" * 56
    print()
    print(bar)
    print(f"  {heading}")
    print(bar)
    print("  Rules:")
    for i, r in enumerate(rules, 1):
        print(f"    {i}. {r.description}")
    print()

    brute_count, smart_count = _candidate_counts(n_digits)

    run_brute = n_digits <= max_brute_digits
    if run_brute:
        t0 = time.perf_counter()
        bf_solutions = solve_brute(n_digits, rules)
        t_bf = time.perf_counter() - t0
    else:
        bf_solutions = None
        t_bf = None

    t0 = time.perf_counter()
    sm_solutions = solve_smart(n_digits, rules)
    t_sm = time.perf_counter() - t0

    if bf_solutions is not None:
        assert sorted(bf_solutions) == sorted(sm_solutions), \
            "Solvers disagree — check your rules!"

    solutions = sm_solutions
    if solutions:
        print(f"  Solution(s): {solutions}")
    else:
        print("  No solution found.")
    print()

    print(f"  {'Solver':<14}  {'Time':>10}   {'Candidates':>16}")
    print(f"  {'──────':<14}  {'────':>10}   {'──────────':>16}")
    if run_brute:
        print(f"  {'Brute-force':<14}  {t_bf:>9.4f}s   {brute_count:>16,}")
    else:
        print(f"  {'Brute-force':<14}  {'(skipped)':>10}   {brute_count:>16,}")
    print(f"  {'Smart':<14}  {t_sm:>9.4f}s   {smart_count:>16,}")
    if run_brute and t_sm > 0 and t_bf is not None:
        print(f"  Speed ratio:  {t_bf / t_sm:.1f}× faster")
    print()
    return n_digits, t_bf, t_sm

# ─────────────────────────────────────────────────────────────
# Puzzle definitions
# ─────────────────────────────────────────────────────────────

_PUZZLES = {
    # Rules are stored as lambdas so each call to p["rules"]() produces a fresh
    # list of Rule objects.  Reusing the same list across multiple compare() calls
    # would work here, but the lambda makes the intent explicit.
    3: {
        "label": "3-digit warm-up  (hand-solvable)",
        "rules": lambda: [
            no_repeat(),
            digit_is_even(0),            # digit 1 is even
            digit_offset(0, 1, 3),       # digit 2 is 3 more than digit 1
            digit_is_prime(2),           # digit 3 is prime
            digit_sum_equals(10),        # digits sum to 10
        ],
    },
    5: {
        "label": "5-digit mission ID  (main puzzle)",
        "rules": lambda: [
            no_repeat(),
            digit_offset(0, 1, 3),       # digit 2 is 3 more than digit 1
            digit_is_prime(2),           # digit 3 is prime
            digit_offset(2, 3, 1),       # digit 4 is 1 more than digit 3
            digit_double(3, 4),          # digit 5 is twice digit 4
            digit_sum_equals(24),        # digits sum to 24
        ],
    },
    7: {
        "label": "7-digit stretch  (scaling demo)",
        "rules": lambda: [
            no_repeat(),
            digit_is_prime(0),
            digit_offset(0, 1, 2),       # digit 2 = digit 1 + 2
            digit_is_even(2),
            digit_offset(2, 3, 1),       # digit 4 = digit 3 + 1
            digit_is_odd(4),
            digit_sum_equals(28),
        ],
    },
}


# ─────────────────────────────────────────────────────────────
# Scaling table with extrapolation
# ─────────────────────────────────────────────────────────────

def _fmt_dur(t, est=False):
    """Format a duration in human-readable form."""
    prefix = "~" if est else ""
    if t < 0.001:
        return "~0.001s" if est else "<0.001s"
    if t < 60:
        return f"{prefix}{t:.3f}s"
    if t < 3600:
        return f"{prefix}{t / 60:.1f} min"
    return f"{prefix}{t / 3600:.1f} hr"


def _print_scaling_table(timing_samples):
    """Print a scaling perspective using actual + extrapolated times.

    timing_samples — list of (n, t_bf, t_sm) returned by compare().
                     t_bf may be None when brute-force was skipped.
    """
    # Calibration: use the largest-n actual measurement for each solver.
    brute_pts = [(n, tb) for n, tb, _ in timing_samples if tb is not None]
    if not brute_pts:
        # No brute timing available; do a fast background calibration.
        t_start = time.perf_counter()
        solve_brute(3, [no_repeat()])
        t_cal = time.perf_counter() - t_start
        brute_pts = [(3, t_cal)]

    # Use the largest n we actually measured as the calibration point.
    # Dividing measured time by candidate count gives seconds-per-check,
    # which we then multiply by the candidate count at any other n to estimate.
    nb, tb_ref = max(brute_pts, key=lambda x: x[0])
    cost_b = tb_ref / _candidate_counts(nb)[0]   # seconds per brute candidate

    best_smart = max(timing_samples, key=lambda x: x[0])
    ns_ref, ts_ref = best_smart[0], best_smart[2]
    cost_s = ts_ref / _candidate_counts(ns_ref)[1]  # seconds per permutation

    actual = {n: (tb, ts) for n, tb, ts in timing_samples}
    show_ns = sorted(set(actual) | {3, 5, 7, 10})

    bar = "\u2500" * 56
    print(bar)
    print("  Scaling perspective  (no-repeat codes):")
    print()
    print(f"  {'Digits':>6}   {'Brute-force':>14}   {'Smart':>14}   {'Speed-up':>10}")
    print(f"  {'\u2500\u2500\u2500\u2500\u2500\u2500':>6}   {'\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500':>14}   {'\u2500\u2500\u2500\u2500\u2500':>14}   {'\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500':>10}")

    for n in show_ns:
        bc, sc = _candidate_counts(n)
        if n in actual:
            tb_a, ts_a = actual[n]
            sm_t = _fmt_dur(ts_a)
            if tb_a is not None:
                bf_t = _fmt_dur(tb_a)
                ratio = f"{tb_a / ts_a:.1f}\u00d7" if ts_a > 0 else "\u2014"
            else:
                est_b = cost_b * bc
                bf_t = _fmt_dur(est_b, est=True)
                ratio = f"~{est_b / ts_a:.0f}\u00d7" if ts_a > 0 else "\u2014"
        else:
            est_b = cost_b * bc
            est_s = cost_s * sc
            bf_t = _fmt_dur(est_b, est=True)
            sm_t = _fmt_dur(est_s, est=True)
            ratio = f"~{est_b / est_s:.0f}\u00d7" if est_s > 0 else "\u2014"
        print(f"  {n:>6}   {bf_t:>14}   {sm_t:>14}   {ratio:>10}")

    print()
    print("  Candidate counts:")
    for n in show_ns:
        bc, sc = _candidate_counts(n)
        print(f"    {n} digits:  {bc:>15,}  brute   \u2192  {sc:>12,}  smart")
    print()
    print("  Rows marked with ~ are estimates extrapolated from measured runs.")
    print()


# ─────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run signal ID puzzles and compare brute-force vs smart solver.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python signal_solver.py                # 3- and 5-digit (default)\n"
            "  python signal_solver.py --digits 5     # 5-digit only\n"
            "  python signal_solver.py --digits 3,5,7 # all available puzzles\n"
        ),
    )
    parser.add_argument(
        "--digits",
        default="3,5",
        help=(
            "Comma-separated digit counts to run (default: 3,5). "
            f"Available: {sorted(_PUZZLES)}"
        ),
    )
    args = parser.parse_args()

    try:
        digits_list = [int(x.strip()) for x in args.digits.split(",")]
    except ValueError:
        print("Error: --digits must be comma-separated integers, e.g. 3,5 or 3,5,7")
        sys.exit(1)

    for n in digits_list:
        if n not in _PUZZLES:
            print(f"Error: no puzzle defined for {n} digits. "
                  f"Available: {sorted(_PUZZLES)}")
            sys.exit(1)

    print()
    print("ASTRONOMY LAB — Signal ID Solver")
    print("Decoded from the reactivated probe transmission.")

    timing_samples = []
    for n in digits_list:
        p = _PUZZLES[n]
        sample = compare(n, p["rules"](), label=p["label"])
        timing_samples.append(sample)

    _print_scaling_table(timing_samples)
