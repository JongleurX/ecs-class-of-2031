"""Challenge 16: Mood-Based Activity Suggester
Ask how the user is feeling and suggest something to do.
"""

mood = input("How are you feeling today? ").lower().strip()

if "happy" in mood or "great" in mood or "good" in mood:
    suggestion = "Go outside and enjoy the day! ☀️ Maybe ride a bike or call a friend."
elif "tired" in mood or "sleepy" in mood or "bored" in mood:
    suggestion = "Cozy up with a good book or take a short walk to wake up. 📚"
elif "sad" in mood or "down" in mood or "bad" in mood:
    suggestion = "Make yourself a warm drink and watch your favorite show. 🍵"
elif "stressed" in mood or "anxious" in mood or "nervous" in mood:
    suggestion = "Try some deep breathing or doodle for 5 minutes. 🎨"
elif "excited" in mood or "pumped" in mood or "hyper" in mood:
    suggestion = "Channel that energy — start a creative project! 🚀"
else:
    suggestion = "Whatever you're feeling, taking a 10-minute stretch break never hurts. 🧘"

print("Suggestion:", suggestion)
