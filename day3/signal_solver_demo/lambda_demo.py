"""Lambda demo — what is a lambda, and why does signal_solver.py use them?

A lambda is a way to write a short, one-line function without giving it a name.
This demo shows the same logic written two ways: with and without a lambda.
"""


# ─────────────────────────────────────────────────────────────
# Part 1: A regular function vs. a lambda
# ─────────────────────────────────────────────────────────────

# Regular function: needs a def statement, a name, and a return statement.
def double_regular(x):
    return x * 2

# The exact same logic written as a lambda.
# Syntax:   lambda <arguments> : <expression to return>
double_lambda = lambda x: x * 2

print("Part 1 — regular function vs lambda:")
print(double_regular(5))   # 10
print(double_lambda(5))    # 10  — identical result
print()


# ─────────────────────────────────────────────────────────────
# Part 2: How lambdas appear in signal_solver.py
# ─────────────────────────────────────────────────────────────
#
# signal_solver.py stores rules as objects.  Each rule has a name (description)
# and a test function.  Here is a stripped-down version of that Rule class:

class Rule:
    def __init__(self, description, fn):
        self.description = description
        self.fn = fn

    def check(self, digits):
        return self.fn(digits)


# ── With a lambda (this is what signal_solver.py does) ────────────────────────
#
# The test function is written right where it is used — no extra name needed.

result_even_lam       = Rule("Digit 1 is even",    lambda d: d[0] % 2 == 0)
result_no_repeat_lam  = Rule("All digits differ",  lambda d: len(set(d)) == len(d))
result_sum_lam        = Rule("Digits sum to 10",   lambda d: sum(d) == 10)


# ── Without a lambda ──────────────────────────────────────────────────────────
#
# Each test needs its own separately-named function.
# With many rules, you end up with a long list of helper functions,
# and the connection between the name and the rule is less obvious.

def _check_even(d):
    return d[0] % 2 == 0

def _check_no_repeat(d):
    return len(set(d)) == len(d)

def _check_sum_is_10(d):
    return sum(d) == 10

result_even_def       = Rule("Digit 1 is even",   _check_even)
result_no_repeat_def  = Rule("All digits differ",  _check_no_repeat)
result_sum_def        = Rule("Digits sum to 10",   _check_sum_is_10)


# ─────────────────────────────────────────────────────────────
# Part 3: Both produce exactly the same results
# ─────────────────────────────────────────────────────────────

test_cases = [
    [2, 5, 3],   # even start, all different, sum = 10 → should pass all rules
    [3, 5, 2],   # odd start → result_even_lam should be False
    [2, 2, 6],   # repeated digit → result_no_repeat_lam should be False
    [2, 5, 4],   # sum = 11, not 10 → result_sum_lam should be False
]

print("Part 3 — comparison: lambda vs regular function:")
print(f"  {'Digits':<12}  {'even (lam)':<12}  {'even (def)':<12}  {'no-repeat (lam)':<17}  {'no-repeat (def)'}")
for t in test_cases:
    print(
        f"  {str(t):<12}  "
        f"{str(result_even_lam.check(t)):<12}  "
        f"{str(result_even_def.check(t)):<12}  "
        f"{str(result_no_repeat_lam.check(t)):<17}  "
        f"{str(result_no_repeat_def.check(t))}"
    )
print()
print("Every lambda result matches its 'def' equivalent — they are identical.")
