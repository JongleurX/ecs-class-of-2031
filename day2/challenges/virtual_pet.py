"""Challenge 12: Virtual Pet Mood Tracker
Biscuit the pet tells you how it feels based on how many times you fed it today.
"""

times_fed = int(input("How many times have you fed Biscuit today? "))

if times_fed == 0:
    mood = "STARVING! 😿 Biscuit glares at you."
elif times_fed == 1:
    mood = "a little hungry. 🐾 One snack is never enough."
elif times_fed <= 3:
    mood = "happy! 😸 Biscuit purrs contentedly."
elif times_fed <= 5:
    mood = "full and sleepy. 😴 Biscuit has found the sunny spot."
else:
    mood = "absolutely stuffed. 🤢 You may have overdone it..."

print("Biscuit is feeling", mood)
