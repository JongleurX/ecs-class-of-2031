#!/usr/bin/env python3

"""Exercise 08: Pixel Art Starter

Task:
1. Run this file and notice how the helper functions color each pixel.
2. Fill in the TODO rows in `main()` with your own print statements.
3. Build a small piece of pixel art one row at a time.

Notes:
- Each pixel is printed as two spaces so the art looks more square.
- ANSI color codes work in most terminals.
- The helper functions already handle turning color on and off.
"""

COLORS = {
    "black": "40",
    "red": "41",
    "green": "42",
    "yellow": "43",
    "blue": "44",
    "magenta": "45",
    "cyan": "46",
    "white": "47",
    "gray": "100",
    "brown": "48;5;137",
    "tan": "48;5;222",
}

RLE_CODES = {
    "a": "gray",
    "o": "brown",
    "k": "black",
    "r": "red",
    "g": "green",
    "y": "yellow",
    "b": "blue",
    "m": "magenta",
    "c": "cyan",
    "t": "tan",
    "w": "white",
    "_": None,
}


def set_color(color_name):
    print(f"\033[{COLORS[color_name]}m", end="")


def reset_color():
    print("\033[0m", end="")


def pixel(color_name):
    set_color(color_name)
    print("  ", end="")
    reset_color()


def blank():
    print("  ", end="")


def end_row():
    print()


def border_row(width, color_name="cyan"):
    for _ in range(width):
        pixel(color_name)
    end_row()


def draw_run(count, color_name=None):
    for _ in range(count):
        if color_name is None:
            blank()
        else:
            pixel(color_name)


def draw_rle_row(row_text):
    """Draw one row from tokens like 'm1 b14 m1' or 'c1 _14 c1'."""
    for token in row_text.split():
        code = token[0]
        count = int(token[1:])
        draw_run(count, RLE_CODES[code])
    end_row()


def draw_rle_art(rows):
    for row in rows:
        draw_rle_row(row)


def print_cat():
    """Print a 16x16 cat scene inspired by the reference image."""
    rows = [
        "o16",
        "o16",
        "o7 k2 o3 k1 o3",
        "o7 k1 a1 k3 a1 k1 o2",
        "o3 k1 o1 k8 o3",
        "o2 k1 o2 k3 y1 k2 y1 k2 o2",
        "o2 k1 o2 k3 m1 k4 o3",
        "o2 k1 o4 w4 o5",
        "o3 k1 o1 k4 w3 o4",
        "o3 k7 w2 o1 w1 o2",
        "o4 k5 w1 k2 w1 o3",
        "o5 k3 w1 k2 w1 o4",
        "t1 o1 t2 o8 t3 o1",
        "t16",
        "o16",
        "o16",
    ]
    draw_rle_art(rows)


def print_mini_soccer_ball():
    """Print an 8x8 soccer ball using direct pixel() and blank() calls."""
    blank(); blank(); pixel("white"); pixel("white"); pixel("white"); pixel("white"); blank(); blank(); end_row()
    blank(); pixel("white"); pixel("white"); pixel("red"); pixel("red"); pixel("white"); pixel("white"); blank(); end_row()
    pixel("white"); pixel("white"); pixel("red"); pixel("white"); pixel("white"); pixel("red"); pixel("white"); pixel("white"); end_row()
    pixel("white"); pixel("red"); pixel("white"); pixel("white"); pixel("white"); pixel("white"); pixel("red"); pixel("white"); end_row()
    pixel("white"); pixel("red"); pixel("white"); pixel("white"); pixel("white"); pixel("white"); pixel("red"); pixel("white"); end_row()
    pixel("white"); pixel("white"); pixel("red"); pixel("white"); pixel("white"); pixel("red"); pixel("white"); pixel("white"); end_row()
    blank(); pixel("white"); pixel("white"); pixel("red"); pixel("red"); pixel("white"); pixel("white"); blank(); end_row()
    blank(); blank(); blank(); blank(); blank(); blank(); blank(); blank(); end_row()


def print_concentric_squares():
    """Print a 16x16 concentric squares example using simple RLE rows."""
    rows = [
        "m16",
        "m1 b14 m1",
        "m1 b1 g12 b1 m1",
        "m1 b1 g1 y10 g1 b1 m1",
        "m1 b1 g1 y1 r8 y1 g1 b1 m1",
        "m1 b1 g1 y1 r8 y1 g1 b1 m1",
        "m1 b1 g1 y1 r8 y1 g1 b1 m1",
        "m1 b1 g1 y1 r8 y1 g1 b1 m1",
        "m1 b1 g1 y1 r8 y1 g1 b1 m1",
        "m1 b1 g1 y1 r8 y1 g1 b1 m1",
        "m1 b1 g1 y1 r8 y1 g1 b1 m1",
        "m1 b1 g1 y1 r8 y1 g1 b1 m1",
        "m1 b1 g1 y10 g1 b1 m1",
        "m1 b1 g12 b1 m1",
        "m1 b14 m1",
        "m16",
    ]
    draw_rle_art(rows)


def main():
    print("Pixel Art Starter")
    print("Build your picture by filling in the TODO rows below.")
    print("RLE tip: use short codes like m1 b14 m1 or o7 k2 o3 k1 o3")
    print()

    print("Example: Cat (RLE)")
    print_cat()
    print()

    print("Example: Concentric Squares (RLE)")
    print_concentric_squares()
    print()

    print("Example: Mini Soccer Ball (direct pixel calls)")
    print_mini_soccer_ball()
    print()

    # TODO: row 1
    # Example: pixel("yellow"); pixel("yellow"); blank(); pixel("yellow")
    end_row()

    # TODO: row 2
    end_row()

    # TODO: row 3
    end_row()

    # TODO: row 4
    end_row()

    # TODO: row 5
    end_row()


if __name__ == "__main__":
    main()