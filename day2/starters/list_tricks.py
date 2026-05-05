# ─────────────────────────────────────────────────────────────
#  Exercise 05 — List tricks
#
#  Task A: add at least one new animal to the animals list.
#  Task B: add a second for-loop that prints every animal
#          in UPPERCASE.  Hint: use  .upper()
# ─────────────────────────────────────────────────────────────

def exercise_05():
    animals = ["cat", "dog", "rabbit"]   # TODO: add a new animal here

    print("Animals in the list:")
    for animal in animals:
        print("-", animal)
    print("Total animals:", len(animals))

    # TODO: add a second loop here that prints each animal in uppercase
    # Hint: use .upper() on the animal name inside the loop


if __name__ == "__main__":
    exercise_05()
