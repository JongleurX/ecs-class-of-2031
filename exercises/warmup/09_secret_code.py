# Trace this code on paper. What secret word is built?

words = ["SNAKE", "TIGER", "EAGLE", "MOOSE"]
secret = ""
for word in words:
    secret = secret + word[0]
print(secret)

# Can you decode this using only a for loop and indexing?
combined = "STEMBRACKETS"
decoded = ""
for i in range(0, 12, 2):
    decoded = decoded + combined[i]
print(decoded)
