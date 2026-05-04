"""Challenge 13: Color Mixer
Type two color names and get a fun mixed result.
"""

# Each combo is stored once, with the alphabetically earlier color first.
# Before looking up, we swap the two inputs if they're in the wrong order,
# so "red + blue" and "blue + red" both find the same entry.
combos = {
    ("black", "white"): "Gray — like a confused cloud. ☁️",
    ("blue", "red"):    "Purple — like a grape soda! 🍇",
    ("blue", "white"):  "Light Blue — like a clear sky on a perfect day! 🌤️",
    ("blue", "yellow"): "Green — like a frog in a raincoat! 🐸",
    ("red", "white"):   "Pink — like a flamingo at a pool party! 🦩",
    ("red", "yellow"):  "Orange — like a traffic cone! 🍊",
}

color1 = input("Enter the first color: ").lower().strip()
color2 = input("Enter the second color: ").lower().strip()

# Swap so color1 always comes before color2 alphabetically
if color2 < color1:
    color1, color2 = color2, color1

result = combos.get((color1, color2), "Hmm... that's a new color we haven't named yet! 🎨")
print(color1.capitalize() + " + " + color2.capitalize() + " = " + result)
