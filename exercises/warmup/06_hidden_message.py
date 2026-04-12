# Trace this code on paper. What secret message is revealed?

text = "ACBADCEB"
secret = ""
for i in range(0, 8, 2):
    secret = secret + text[i]
print(secret)
