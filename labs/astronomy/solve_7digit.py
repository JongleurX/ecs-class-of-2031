"""7-digit stretch: brute-force signal ID solver with progress bar.

This puzzle has multiple valid signal IDs. The point is to watch how long
even a fast computer takes when checking 10 million candidates — and to
compare with the smart solver in signal_solver.py, which finishes in under
half a second.

Rules
─────
  0. Digit 1 is not 0 (no leading zeros).
  1. All seven digits are different.
  2. Digit 1 is a prime number (2, 3, 5, or 7).
  3. Digit 2 is 2 more than digit 1.
  4. Digit 3 is even.
  5. Digit 4 is 1 more than digit 3.
  6. Digit 5 is odd.
  7. The sum of all digits is 28.

(Multiple solutions exist.)
"""

import sys
import time

TOTAL = 10_000_000      # every 7-digit sequence (0000000 to 9999999)


def ok(d):
    return (
        d[0] != 0 and
        len(set(d)) == 7 and
        d[0] in {2, 3, 5, 7} and
        d[1] == d[0] + 2 and
        d[2] % 2 == 0 and
        d[3] == d[2] + 1 and
        d[4] % 2 == 1 and
        sum(d) == 28
    )


def fmt_eta(seconds):
    if seconds < 60:
        return f"{seconds:.0f} seconds"
    elif seconds < 3600:
        m, s = int(seconds // 60), int(seconds % 60)
        return f"{m} min {s} s"
    elif seconds < 86400:
        h, m = int(seconds // 3600), int((seconds % 3600) // 60)
        return f"{h} hr {m} min"
    elif seconds < 2_592_000:
        d, h = int(seconds // 86400), int((seconds % 86400) // 3600)
        return f"{d} days {h} hr"
    else:
        return f"{seconds / 2_592_000:.1f} months"


print(f"Searching {TOTAL:,} candidates...")
print()

solutions = []
start = time.perf_counter()
last_report = start

for i, n in enumerate(range(0, 10_000_000)):
    d = [int(c) for c in str(n).zfill(7)]
    if ok(d):
        solutions.append(n)

    # Only check the clock every 50,000 iterations to avoid slowing the loop.
    if i % 50_000 == 0:
        now = time.perf_counter()
        if now - last_report >= 1.0:
            elapsed = now - start
            pct = (i + 1) / TOTAL * 100
            rate = (i + 1) / elapsed
            remaining = (TOTAL - i - 1) / rate
            bar_w = 30
            filled = int(pct / 100 * bar_w)
            bar = "█" * filled + "░" * (bar_w - filled)
            sys.stdout.write(
                f"\r  [{bar}] {pct:5.1f}%  "
                f"{i+1:,} / {TOTAL:,}  "
                f"ETA: {fmt_eta(remaining)}   "
            )
            sys.stdout.flush()
            last_report = now

elapsed = time.perf_counter() - start
sys.stdout.write(f"\r  Done in {elapsed:.1f}s.{' ' * 60}\n")

print()
if solutions:
    print(f"Found {len(solutions)} solution(s):")
    for s in solutions:
        print(f"  {s}")
else:
    print("No solutions found.")
print()
print("Tip: run  python signal_solver.py  to see the smart solver finish in under 0.5 s.")
