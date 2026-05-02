"""10-digit scaling demo: brute-force signal ID solver with progress bar.

This script is designed to be stopped early with Ctrl+C.
The point is to watch the ETA grow — understanding why checking
9 billion candidates by hand (or naively by computer) is impractical,
and why a smarter search strategy matters.

Rules
─────
  0. Digit 1 is not 0 (no leading zeros).
  1. All 10 digits are different.
  2. Digit 1 is a prime number (2, 3, 5, or 7).
  3. Digit 2 is 3 more than digit 1.
  4. Digit 3 is even.
  5. Digit 4 is 1 more than digit 3.
  6. Digit 5 is odd.
  7. Digit 6 is a prime number (2, 3, 5, or 7).
  8. Digit 7 is 2 more than digit 6.
  9. Digit 8 is even.
  10. Digit 9 is 1 more than digit 8.
  11. Digit 10 is odd.

(Multiple solutions exist. Run signal_solver.py for the instant smart result.)
"""

import sys
import time

TOTAL = 10_000_000_000  # every 10-digit sequence (0000000000 to 9999999999)


def ok(d):
    return (
        d[0] != 0 and
        len(set(d)) == 10 and
        d[0] in {2, 3, 5, 7} and
        d[1] == d[0] + 3 and
        d[2] % 2 == 0 and
        d[3] == d[2] + 1 and
        d[4] % 2 == 1 and
        d[5] in {2, 3, 5, 7} and
        d[6] == d[5] + 2 and
        d[7] % 2 == 0 and
        d[8] == d[7] + 1 and
        d[9] % 2 == 1
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


print(f"Starting 10-digit brute-force search ({TOTAL:,} candidates).")
print("Press Ctrl+C at any time to stop early and check the ETA.")
print()

solutions = []
start = time.perf_counter()
last_report = start
i = -1  # in case Ctrl+C fires before the first iteration

try:
    for i, n in enumerate(range(0, 10_000_000_000)):
        d = [int(c) for c in str(n).zfill(10)]
        if ok(d):
            solutions.append(n)

        # Only check the clock every 500,000 iterations to avoid slowing the loop.
        if i % 500_000 == 0:
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
    sys.stdout.write(f"\r  Done in {fmt_eta(elapsed)}.{' ' * 60}\n")

except KeyboardInterrupt:
    elapsed = time.perf_counter() - start
    checked = i + 1
    pct = checked / TOTAL * 100
    rate = checked / elapsed if elapsed > 0 else 0
    remaining = (TOTAL - checked) / rate if rate > 0 else float("inf")
    sys.stdout.write(f"\n\nStopped after {fmt_eta(elapsed)}  ({pct:.4f}% complete).\n")
    if rate > 0:
        print(f"At this rate, the full search would take ~{fmt_eta(remaining)} more.")

print()
if solutions:
    print(f"Found {len(solutions)} solution(s) in the portion checked:")
    for s in solutions:
        print(f"  {s}")
else:
    print("No solutions found in the portion checked.")
print()
print("Tip: run  python signal_solver.py  to see the smart solver find answers in seconds.")
