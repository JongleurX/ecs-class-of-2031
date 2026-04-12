# Trace this code on paper. What does it print?

evens = 0
odds = 0
for n in range(1, 6):
    if n % 2 == 0:
        evens = evens + n
    else:
        odds = odds + n
print("Evens:", evens)
print("Odds:", odds)
