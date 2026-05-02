"""3-digit warm-up: brute-force signal ID solver.

Rules
─────
  0. Digit 1 is not 0 (no leading zeros).
  1. All three digits are different.
  2. Digit 1 is even.
  3. Digit 2 is 3 more than digit 1.
  4. Digit 3 is a prime number (2, 3, 5, or 7).
  5. The sum of all digits is 10.

Expected answer: 253
"""


def ok(d):
    return (
        d[0] != 0 and               # not a leading zero
        len(set(d)) == 3 and        # all three digits are different
        d[0] % 2 == 0 and           # digit 1 is even
        d[1] == d[0] + 3 and        # digit 2 is 3 more than digit 1
        d[2] in [2, 3, 5, 7] and    # digit 3 is prime
        sum(d) == 10                 # digits add up to 10
    )


for n in range(0, 1000):            # try every 3-digit sequence (000 to 999)
    if ok([int(c) for c in str(n).zfill(3)]):
        print(n)
