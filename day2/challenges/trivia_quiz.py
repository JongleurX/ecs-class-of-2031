"""Challenge 18: Trivia Quiz
5 questions, keep score, get a funny title at the end.
"""

questions = [
    ("What is 7 × 8?",               "56"),
    ("What color do you get mixing red and blue?", "purple"),
    ("How many sides does a hexagon have?",        "6"),
    ("What planet is closest to the sun?",         "mercury"),
    ("What is the square root of 144?",            "12"),
]

score = 0

print("🧠 Welcome to the PyTrivia Quiz!\n")

for question, answer in questions:
    response = input(question + " ").strip().lower()
    if response == answer.lower():
        print("  ✅ Correct!\n")
        score += 1
    else:
        print(f"  ❌ Nope! The answer was: {answer}\n")

print(f"You got {score} out of {len(questions)}.")

if score == 5:
    title = "Quiz Wizard 🧙 — Perfect score!"
elif score >= 3:
    title = "Knowledge Knight ⚔️ — Solid work!"
elif score >= 1:
    title = "Brave Guesser 🎲 — Keep studying!"
else:
    title = "Rookie Explorer 🗺️ — Everyone starts somewhere!"

print("Your title:", title)
