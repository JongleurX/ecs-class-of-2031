# Trace this code on paper. What pattern is printed?

for row in range(3):
    line = ""
    for col in range(row + 1):
        line = line + "*"
    print(line)
