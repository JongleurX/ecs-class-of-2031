# Trace this code on paper step by step. What does it print?

grid = ""
for row in range(3):
    for col in range(4):
        if (row + col) % 2 == 0:
            grid = grid + "🟢"
        else:
            grid = grid + "⚪"
    grid = grid + "\n"
print(grid)

# And what is the final count?
count = 0
for char in grid:
    if char == "🟢":
        count = count + 1
print("Green count:", count)
