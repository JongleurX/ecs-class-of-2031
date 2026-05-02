# Astronomy Lab — Signal ID: Teacher Guide

## The idea

Students decode the authentication ID of a reactivated space probe by applying
mathematical constraint rules — first by hand on a small version, then with Python
on the full-size version, then watching how performance changes as the code gets longer.

The puzzle type is **constraint satisfaction**: given a set of rules about digits,
find the one number that satisfies them all. The computational-thinking payoff is that
the same problem-solving strategy — list possibilities, eliminate impossible ones,
keep going — translates directly into code.

---

## Suggested class flow  (~80 minutes)

### Part 1 — Explore on paper  (30 min)

Hand out the **3-digit warm-up** (generate one with `--digits 3`).

Walk through it together:
- Which rule eliminates the most possibilities?
- What can we work out from just rules 1 and 2 combined?
- Is there a systematic order, or do you jump around?

Once students have an answer, reveal it and discuss the reasoning.
Then hand out the **5-digit main puzzle** and let pairs work through it
(15–20 min). Encourage them to write out their elimination steps, not just guess.

### Part 2 — Translate to code  (25 min)

Show the brute-force solver pattern on the board — about 10 lines:

```python
def ok(d):
    return (
        len(set(d)) == 5 and
        d[1] == d[0] + 3 and
        d[2] in [2, 3, 5, 7] and
        d[3] == d[2] + 1 and
        d[4] == 2 * d[3] and
        sum(d) == 24
    )

for n in range(10000, 100000):
    if ok([int(c) for c in str(n)]):
        print(n)
```

Ask students to type it in and run it. Then open `signal_solver.py` and show how
the same logic is organised into reusable `Rule` building blocks.

### Part 3 — Scaling  (15 min)

Run `python signal_solver.py` together as a class. Look at the timing table.

Discussion questions:
- Why is the smart solver faster? (It only tries digit combinations where no digit repeats.)
- What happens at n=10? Would you want to be the one checking 9 billion numbers by hand?
- Does Python solve it the "smart" way, or does it just brute-force faster?
- What other rules could you add that would make the search even faster?

### Part 4 — Wrap-up  (10 min)

Return to the original hand-solve. Ask:
- Did anyone use a strategy similar to what the smart solver does?
- What made some rules more useful than others?

---

## Generating puzzles

### Basic usage

```bash
# 5-digit puzzle (default)
python puzzle_generator.py

# 3-digit warm-up
python puzzle_generator.py --digits 3

# Reproducible puzzle (share the seed with a colleague)
python puzzle_generator.py --digits 5 --seed 42

# Three different puzzles at once
python puzzle_generator.py --digits 5 --count 3
```

### What comes out

Each run prints two blocks:

**Student handout** — the story premise, the numbered rules, and a blank
`Signal ID: __ __ __ __ __` line. Ready to copy into a slide or print directly.

**Teacher key** — the answer, a pruning table showing how each rule narrows
the candidate pool, and a short Python snippet to verify the answer.

### Tips

- The generator tries random answers and adds rules greedily (most-pruning first).
  If a seed produces a puzzle with only 2–3 rules, try a neighbouring seed — more rules
  generally makes for a better classroom puzzle.
- For a 3-digit warm-up, puzzles can sometimes be solved in one or two rules.
  Run with `--count 5` and pick the one with the most interesting rule set.
- Codes longer than 7 digits are not supported by the generator (the permutation
  pool gets large). For the scaling discussion you don't need a unique puzzle —
  the solver's timing table already makes the point.

---

## The no-repeat rule

For codes up to 10 digits the "all digits different" rule is always in effect.
At 11+ digits there aren't enough distinct digits (0–9) to go around, so repeats
would be necessary. The solver handles this automatically:
- n ≤ 10: uses `itertools.permutations` — no-repeat built in, fast
- n > 10: uses `itertools.product` — repeats allowed, slower

This is worth mentioning briefly to curious students: the rule isn't just a puzzle
choice, it's a mathematical necessity at scale.

---

## Files

| File | Audience | Purpose |
|---|---|---|
| `signal_solver.py` | Students + teacher | Reference solver; run directly for the demo |
| `puzzle_generator.py` | Teacher only | Generates fresh puzzles with unique solutions |
| `outline.txt` | Teacher | Original design notes for the activity |
| `secondtake.txt` | Teacher | Alternative framing and additional puzzle types |
