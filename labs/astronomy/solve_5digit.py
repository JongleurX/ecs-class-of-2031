"""5-digit mission ID: brute-force signal ID solver.

Rules
─────
  0. Digit 1 is not 0 (no leading zeros).
  1. All five digits are different.
  2. Digit 2 is 3 more than digit 1.
  3. Digit 3 is a prime number (2, 3, 5, or 7).
  4. Digit 4 is 1 more than digit 3.
  5. Digit 5 is twice digit 4.
  6. The sum of all digits is 24.

Expected answer: 58236
"""


def ok(d):
    return (
        d[0] != 0 and               # not a leading zero
        len(set(d)) == 5 and        # all five digits are different
        d[1] == d[0] + 3 and        # digit 2 is 3 more than digit 1
        d[2] in [2, 3, 5, 7] and    # digit 3 is prime
        d[3] == d[2] + 1 and        # digit 4 is 1 more than digit 3
        d[4] == 2 * d[3] and        # digit 5 is twice digit 4
        sum(d) == 24                 # digits add up to 24
    )


for n in range(0, 100_000):         # try every 5-digit sequence (00000 to 99999)
    if ok([int(c) for c in str(n).zfill(5)]):
        print(n)
