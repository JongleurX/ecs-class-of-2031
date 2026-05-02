"""Challenge 14b: Secret Message Decoder (Caesar Cipher)
Paste in an encoded message (input is hidden so nobody can read over
your shoulder). Shift every letter back by 3 to reveal the original.
"""

import getpass

# getpass prompts for input without echoing it to the screen
encoded = getpass.getpass("Paste the encoded message (hidden): ")
decoded = ""

for ch in encoded:
    if ch.isalpha():
        base = ord("A") if ch.isupper() else ord("a")
        decoded += chr((ord(ch) - base - 3) % 26 + base)
    else:
        decoded += ch

print("Decoded:", decoded)
