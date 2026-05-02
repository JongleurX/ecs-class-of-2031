"""Challenge 14: Secret Message Encoder (Caesar Cipher)
Shift every letter in a message forward by 3 positions.
A→D, B→E, Z→C, etc. Non-letters pass through unchanged.
"""

message = input("Enter a secret message: ")
encoded = ""

for ch in message:
    if ch.isalpha():
        base = ord("A") if ch.isupper() else ord("a")
        encoded += chr((ord(ch) - base + 3) % 26 + base)
    else:
        encoded += ch

print("Encoded:", encoded)
