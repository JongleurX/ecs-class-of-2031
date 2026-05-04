# Teacher's Guide: Python Exercises for Scratch Students

This guide contains sample solutions and teaching hints for each exercise. Solutions show the final working code with line numbers. Use these to help students when they get stuck, but encourage them to figure things out first!

## Exercise 01: Hello World / Simple Edit

**Learning Goals:** Variables, print statements, basic arithmetic

**Hints to Give:**
- "Look for the lines that start with `your_name =` and `fav_number =`"
- "Change the text in quotes to your own information"
- "The program will show your changes when you run it"

**Solution:**
```python
# Student-edit section
your_name = "Jeremy"  # Changed from "Scratch Kid"
fav_number = 42       # Changed from 7
```

**Optional Extension Solution:**
```python
print("Welcome to coding,", your_name + "!")
```

## Exercise 02: Fix the Typo + Change Values

**Learning Goals:** Debugging, string methods, arithmetic operations

**Hints to Give:**
- "Look for the word that looks wrong on line 19"
- "It's a method that cleans up user input - what should it be?"
- "Try changing the numbers `a` and `b` to test different calculations"

**Solution:**
```python
operation = input("Operation: ").strip().lower()  # Fixed: stirp -> strip
```

## Exercise 03: Number Guessing Game

**Learning Goals:** Random numbers, loops, conditionals, binary search concept

**Hints to Give:**
- "The game generates a random number each time - that's why it's different!"
- "For the helper function, you need to calculate how many numbers are left and suggest the middle one"
- "Use `(low + high) // 2` to find the middle number"

**Solution:**
```python
#!/usr/bin/env python3

def helper_hint(low, high):
    count = high - low + 1
    middle = (low + high) // 2
    return f"Our number is between {low} and {high}, with {count} possible numbers left. Try {middle} next!"
```

## Exercise 04: Write Your Own Function

**Learning Goals:** Function definition, return statements, boolean logic

**Hints to Give:**
- "Functions need to `return` a value, not just print it"
- "For `greet_user`, combine the word 'Hello' with the name parameter"
- "For `is_even`, use the modulo operator `%` - even numbers divide by 2 with no remainder"

**Solution:**
```python
def greet_user(name):
    return "Hello, " + name + "!"

def is_even(number):
    return number % 2 == 0
```

## Exercise 05: Lists and Loops

**Learning Goals:** Lists, for loops, string methods, function composition

**Hints to Give:**
- "Add a new animal name to the `animals` list using square brackets `[]`"
- "To print in uppercase, use `.upper()` on each animal name"
- "The `count_vowels` function needs to check each character and count 'a','e','i','o','u'"

**Solution:**
```python
animals = ["cat", "dog", "rabbit", "elephant"]  # Added "elephant"

...

# Second loop for uppercase
print("\nAnimals in UPPERCASE:")
for animal in animals:
    print("-", animal.upper())

...

# Optional function for extension
def count_vowels(word):
    vowels = "aeiou"
    count = 0
    for char in word.lower():
        if char in vowels:
            count += 1
    return count

print("\nVowel counts:")
for animal in animals:
    print(animal, "has", count_vowels(animal), "vowels")
```

## Exercise 06: Japanese Character Tutor

**Learning Goals:** Dictionaries, loops, input validation, statistics calculation, Unicode handling

**Hints to Give:**
- "Store multiple answers per character as a list (e.g., `'し': ['shi','si']`)"
- "Add three variables at the start: `correct_count = 0`, `incorrect_count = 0`, `streak = 0`"
- "Update these variables in the answer checking section"
- "For percentage: `(correct_count / (correct_count + incorrect_count)) * 100` if total > 0"
- "Check streak after updating it: `if streak == 10: print('🎉 10 in a row!')`"

**Solution:**
```python
def normalize_answers(value):
    if isinstance(value, list):
        return [v.lower() for v in value]
    return [value.lower()]


def play_game(character_dict, mode_name):
    """Main game loop for a character set"""
    print(f"\n🎌 Welcome to {mode_name} Tutor!")
    print("Type 'quit' to exit, 'stats' to see your progress.\n")

    # Add tracking variables
    correct_count = 0
    incorrect_count = 0
    streak = 0

    while True:
        # Pick a random character
        char = random.choice(list(character_dict.keys()))
        correct_answer = character_dict[char]
        allowed_answers = normalize_answers(correct_answer)

        # Show character and get answer
        answer = input(f"What is the pronunciation of {char}? ").strip().lower()

        if answer == 'quit':
            print("Thanks for practicing! ありがとう!")
            break
        elif answer == 'stats':
            # Show statistics
            total = correct_count + incorrect_count
            if total > 0:
                percentage = (correct_count / total) * 100
                print(f"📊 Stats: {correct_count} correct, {incorrect_count} incorrect")
                print(f"📈 Success rate: {percentage:.1f}%")
            else:
                print("📊 No answers yet!")
            continue

        # Check answer (case insensitive, multiple readings allowed)
        if answer in allowed_answers:
            print("✅ Correct!")
            correct_count += 1
            streak += 1
        else:
            if len(allowed_answers) == 1:
                print(f"❌ Incorrect. The answer is '{allowed_answers[0]}'.")
            else:
                print(f"❌ Incorrect. The answer can be one of: {', '.join(allowed_answers)}.")

            incorrect_count += 1
            streak = 0

        # Check for streak milestones
        if streak == 10:
            print("🎉 10 in a row! You're on fire!")
        elif streak == 20:
            print("🔥 20 in a row! Amazing!")
        elif streak == 30:
            print("🏆 30 in a row! You're a master!")
```

## Exercise 07: Flag Painter - Abstraction with Colors

**Learning Goals:** Function abstraction, parameter passing, geometry vs. appearance separation

**Teaching Points:**
- Same `vertical_stripes()` function creates both France and Italy flags
- Same `horizontal_stripes()` function handles Germany (3 stripes) and Ukraine (2 stripes)
- Same `circle_flag()` function creates Japan and Bangladesh with different circle colors
- Abstraction: geometry code stays the same, only color parameters change

**Hints to Give:**
- "France and Italy both use `vertical_stripes()` - just change the color list"
- "Germany and Ukraine both use `horizontal_stripes()` - the function handles different stripe counts automatically"
- "Japan and Bangladesh both use `circle_flag()` - just change the circle color and background parameters"

**Solution - Only the Lines That Need to Change:**
```python

def circle_flag(circle_color, background_color='white'):
    ...
    center_x = WIDTH // 2  # Center the circle horizontally instead of positioning it 25% of the way from the left
    radius = HEIGHT * 3 // 10  # Diameter should be 3/5 of height for the Japanese flag, so radius is 3/10 the height

... 

# France
flag1 = vertical_stripes(['blue', 'white', 'red'])  # FIXED: vertical stripes with correct colors and correct number of colors!

...

# Italy
flag2 = vertical_stripes(['green', 'white', 'red'])  # FIXED: vertical stripes with correct colors!

...

# Germany
flag3 = horizontal_stripes(['black', 'red', 'yellow'])  # FIXED: horizontal stripes with correct colors!

...

# Ukraine
flag4 = horizontal_stripes(['blue', 'yellow'])  # FIXED: horizontal stripes with correct colors!

...

# Japan
flag5 = circle_flag('red', 'white')  # FIXED: red circle on white background!

...
# Bangladesh
flag6 = circle_flag('green', 'red')  # FIXED: green circle on red background!
```

**Key Abstraction Concepts:**
- `vertical_stripes(['blue', 'white', 'red'])` → France (left to right)
- `vertical_stripes(['green', 'white', 'red'])` → Italy (left to right)
- `horizontal_stripes(['black', 'red', 'yellow'])` → Germany (top to bottom, 3 stripes)
- `horizontal_stripes(['blue', 'yellow'])` → Ukraine (top to bottom, 2 stripes)
- `circle_flag('red', 'white')` → Japan
- `circle_flag('green', 'red')` → Bangladesh

**Discussion Questions:**
- "Why do France and Italy use `vertical_stripes()` while Germany and Ukraine use `horizontal_stripes()`?"
- "How does changing just the color list create completely different flags?"
- "What's the advantage of separating geometry (shape/direction) from appearance (colors)?"

## Common Student Questions

**"What does this error mean?"**
- Guide them to read the error message carefully
- Point out line numbers and specific problems

**"How do I know what to type?"**
- Refer them to the comments and task descriptions
- Encourage looking at similar examples in the code

**"My program doesn't work!"**
- Ask them to run it and describe what happens
- Have them check their changes against the original code

Remember: The goal is understanding, not perfection. Celebrate small victories and learning from mistakes!