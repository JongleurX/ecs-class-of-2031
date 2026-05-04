# Warmup Exercises: Teacher Guide

These exercises build the **hand-tracing** habit — students trace through code line by line on paper to predict what prints. This foundation makes debugging and understanding code much easier.

## Code.org Single-File Option

If students are working in a Code.org Python project that needs a single entry file, use `main.py` in this folder.

- `main.py` contains all 10 warmup activities in one file.
- Students are guided through all 10 warmups in order (no menu), with progress shown as a percentage.
- For each warmup, the code is printed and students enter their predicted output before answers are unlocked.
- After all predictions are entered, students must enter the password `buffalo` to reveal answers.
- Password checking is case-insensitive (`buffalo`, `BUFFALO`, and `Buffalo` all work).
- Students get 5 password attempts; if all 5 are wrong, they must re-enter all predictions from the beginning.
- After reveal, the program shows the answer key, a total score, and colored red/green comparisons for incorrect predictions.
- This keeps the original individual exercise files for class use while also providing one copy-paste-friendly driver.

## Printable Loop Templates

Use [PRINTABLE_LOOP_TRACE_TEMPLATES.html](PRINTABLE_LOOP_TRACE_TEMPLATES.html) for print-friendly tracing pages for every loop-based warmup (Exercises 3 through 10).

- Includes dedicated before/after trace tables for each loop warmup.
- Includes an expanded nested-loop breakdown for Exercise 10 (outer loop, inner loop per row, and final counting loop).
- For a completed teacher exemplar, use [PRINTABLE_LOOP_TRACE_TEMPLATES_FILLED_EXAMPLE.html](PRINTABLE_LOOP_TRACE_TEMPLATES_FILLED_EXAMPLE.html).

---

## Teaching Progression

### Phase 1: Variables & Print (Exercise 1-2)

**Before Exercise 1, teach:**

**Variables** — A box that holds a value
```python
x = 5        # Create a box called "x", put 5 in it
y = 3        # Create a box called "y", put 3 in it
z = x + y    # Create a box called "z", put the result of x+y in it
```

Rules:
- Left side of `=` is the name (label) of the box
- Right side is what goes in the box
- You can use variable names in new expressions
- `=` means "put this value in that box" (not equals)

**Print** — Display something on screen
```python
print(5)           # Print the number 5
print(x)           # Look inside box x, print what's there
print("Hello")     # Print text (with quotes)
```

**Quick syntax notes:**
- `print()` with parentheses and something inside
- Numbers print as-is
- Text needs `"quotes"` or `'quotes'`
- Variable names print their value (no quotes)

* → Do Exercise 1: `01_simple_math.py` (variable math)
* → Do Exercise 2: `02_string_building.py` (variable strings)

---

### Phase 2: The For Loop (Exercise 3-4)

**Before Exercise 3, teach:**

**For loops** — Do something multiple times
```python
for i in range(4):     # i goes 0, 1, 2, 3
    print(i)           # Indented: do this each time
```

Rules:
- `for VARIABLE in range(NUMBER):` 
  - `range(4)` = 0, 1, 2, 3 (always starts at 0, stops before the number)
  - `range(1, 4)` = 1, 2, 3 (start at 1, stop before 4)
- Everything indented under `for:` repeats
- Indentation is critical (use 4 spaces or press Tab)
- The variable updates automatically each loop

**Accumulators** — A variable that grows
```python
total = 0              # Start with 0
for i in range(1, 4):
    total = total + i  # Add i to what's already in total
    print(total)
```

This prints: `1` (0+1), then `3` (1+2), then `6` (3+3)

* → Do Exercise 3: `03_simple_loop.py` (basic loop)
*→ Do Exercise 4: `04_counting_up.py` (accumulators)

---

### Phase 3: Strings & Loops (Exercise 5-6)

**Before Exercise 5, teach:**

**Looping through text** — Iterate character by character
```python
for letter in "CAT":
    print(letter)      # Prints: C, A, T (one per line)
```

**Building strings** — Concatenation with `+`
```python
word = ""              # Start empty
for letter in "CAT":
    word = word + letter  # Attach the letter
```

This builds: "" → "C" → "CA" → "CAT"

**Indexing** — Grab one character by position
```python
text = "HELLO"
print(text[0])  # First character: H
print(text[1])  # Second character: E
print(text[4])  # Fifth character: O
```

Rules:
- Position counting starts at 0 (not 1)
- `text[0]` means "character at position 0"
- Use `text[i]` inside a loop to grab each character

* → Do Exercise 5: `05_building_a_word.py` (build strings in loop)
* → Do Exercise 6: `06_hidden_message.py` (indexing with step)

**Note on Exercise 6:** Introduce `range(0, 8, 2)` — starts at 0, stops before 8, counts by 2s (0, 2, 4, 6)

---

### Phase 4: Conditionals (Exercise 7-8)

**Before Exercise 7, teach:**

**If statements** — Do something only when a condition is true
```python
if n % 2 == 0:
    print("even")
else:
    print("odd")
```

Rules:
- `%` is modulo (remainder after dividing)
- `n % 2 == 0` means "Does n divided by 2 have remainder 0?"
- `==` means "are these equal?" (not assignment like `=`)
- Only one of `if` or `else` block runs
- Both must be indented

Common conditions:
- `x == y` — is x equal to y?
- `x > y` — is x greater than y?
- `x < y` — is x less than y?
- `x % 2 == 0` — is x even?

* → Do Exercise 7: `07_pattern_loop.py` (nested loops, no conditional yet)

This introduces nested loops — loops inside loops. The key is indentation.

* → Do Exercise 8: `08_multi_accumulator.py` (if/else with accumulators)

---

### Phase 5: Integration (Exercise 9-10)

**Before Exercise 9, teach:**

Bring it all together. Students should now:
- Trace through nested loops
- Use indexing to grab from lists or strings
- Combine accumulators with conditionals

**Introduce list basics (minimal):**
```python
words = ["SNAKE", "TIGER", "EAGLE"]
for word in words:
    print(word[0])     # First letter of each word
```

This is just syntax — they understand loops and indexing already.

* → Do Exercise 9: `09_secret_code.py` (list iteration + tracing)
* → Do Exercise 10: `10_integration_challenge.py` (final challenge)

---

## Quick Reference: Syntax Cheat Sheet

### Variables
```python
x = 5              # Create and assign
y = x + 3          # Use in expressions
name = "Alice"     # Strings need quotes
```

### Print
```python
print(x)           # Print a number
print("Hello")     # Print text
print(x, "is big") # Print multiple things
```

### For Loops
```python
for i in range(5):          # 0, 1, 2, 3, 4
    print(i)

for i in range(1, 5):       # 1, 2, 3, 4
    print(i)

for i in range(0, 10, 2):   # 0, 2, 4, 6, 8
    print(i)

for letter in "HELLO":      # Each character
    print(letter)
```

### String Operations
```python
text = "HELLO"
print(text[0])      # First character: H
print(text[2])      # Third character: L

word = "HE"
word = word + "Y"   # Concatenate: HEY
```

### If Statements
```python
if x > 5:
    print("big")
else:
    print("small")

if n % 2 == 0:
    print("even")
```

### Accumulators
```python
total = 0
for i in range(5):
    total = total + i

word = ""
for letter in "HELLO":
    word = word + letter
```

---

## Assessment Tips

**Ask students to trace by hand first.** Before running code:
1. Provide a blank table with columns: Iteration | Variable Values | Print Output
2. Students fill in by hand
3. Run code to check

**Example for Exercise 4:**
| Iteration | total | i | Print |
|-----------|-------|---|-------|
| before    | 0     | — | —     |
| 1st       | 1     | 1 | 1     |
| 2nd       | 3     | 2 | 3     |
| 3rd       | 6     | 3 | 6     |

This builds the mental model and makes errors visible immediately.

---

## Quick Test Questions (No Running Code)

After each phase, ask:
- **Phase 1:** "If `x = 5` and `y = x + 2`, what does `y` equal?"
- **Phase 2:** "What does `range(2, 5)` produce?" (Answer: 2, 3, 4)
- **Phase 3:** "If `text = "PYTHON"`, what is `text[2]`?" (Answer: T)
- **Phase 4:** "Is 7 even? How would you check with code?" (Answer: `7 % 2 == 0` → False)
- **Phase 5:** "Trace the output of Exercise 9 in your head."

