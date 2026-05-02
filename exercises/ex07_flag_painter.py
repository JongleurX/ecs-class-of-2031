"""Exercise 07: Flag Painter (ASCII + color)

Goal: Experiment with abstraction by using the SAME functions to create
DIFFERENT visual patterns through parameter changes.

Tasks:
1. Run the program and observe the 6 flag patterns.
2. Experiment by changing function calls and color parameters.
3. Notice how the SAME geometry functions create different results!

Notes:
- Use pure Python standard library; no pip packages.
- Output uses ANSI escape sequences for color (works in most terminals).
- Same functions can create many different flag-like patterns!
"""

import math

WIDTH = 50
HEIGHT = 26

RESET = "\033[0m"
COLOR = {
    'black': '40',
    'red': '41',
    'green': '42',
    'yellow': '43',
    'blue': '44',
    'white': '47',
}


def colored_block(color_name):
    return f"\033[{COLOR[color_name]}m " + RESET


def horizontal_stripes(colors):
    """Create horizontal stripes flag. Colors list determines stripe colors."""
    rows = []
    stripe_height = HEIGHT // len(colors)

    for r in range(HEIGHT):
        stripe_index = min(r // stripe_height, len(colors) - 1)
        color = colors[stripe_index]
        row = [colored_block(color) for _ in range(WIDTH)]
        rows.append(row)

    return rows


def vertical_stripes(colors):
    """Create vertical stripes flag. Colors list determines stripe colors."""
    rows = []
    stripe_width = WIDTH // len(colors)

    for r in range(HEIGHT):
        row = []
        for c in range(WIDTH):
            stripe_index = min(c // stripe_width, len(colors) - 1)
            color = colors[stripe_index]
            row.append(colored_block(color))
        rows.append(row)

    return rows


def circle_flag(circle_color, background_color='white'):
    """Create circle flag. Circle color and background color parameters."""
    rows = []

    center_y = HEIGHT // 2
    center_x = WIDTH // 4  # FIXME
    radius = min(WIDTH, HEIGHT) // 8  # FIXME

    for r in range(HEIGHT):
        row = []
        for c in range(WIDTH):
            dist = math.sqrt((c - center_x) ** 2 + (r - center_y) ** 2)
            if dist <= radius:
                row.append(colored_block(circle_color))
            else:
                row.append(colored_block(background_color))
        rows.append(row)

    return rows


def print_flag(title, rows):
    print(f"\n{title}")
    for row in rows:
        print(''.join(row))


def exercise_07():
    print("Exercise 07: Flag Painter")
    print("Experiment with the SAME functions to create DIFFERENT flag patterns!\n")

    # France
    flag1 = horizontal_stripes(['red', 'white', 'blue', 'black'])  # FIXME
    print_flag("France", flag1)

    # Italy
    flag2 = horizontal_stripes(['red', 'blue', 'green'])  # FIXME
    print_flag("Italy", flag2)

    # Germany
    flag3 = vertical_stripes(['yellow', 'red', 'black'])  # FIXME
    print_flag("Germany", flag3)

    # Ukraine
    flag4 = vertical_stripes(['yellow', 'blue'])  # FIXME
    print_flag("Ukraine", flag4)

    # Japan
    flag5 = circle_flag('blue', 'white')  # FIXME
    print_flag("Japan", flag5)

    # Bangladesh
    flag6 = circle_flag('red', 'white')  # FIXME
    print_flag("Bangladesh", flag6)

    print("\n" + "=" * 60)
    print("KEY LEARNING: Abstraction separates GEOMETRY from COLORS!")
    print("- vertical_stripes() creates vertical color bands")
    print("- horizontal_stripes() creates horizontal color bands")
    print("- circle_flag() creates a circle on a background")
    print("- Same functions, different parameters = different results!")
    print("=" * 60)
