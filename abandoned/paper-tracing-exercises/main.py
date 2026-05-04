"""Menu-driven warmup runner for Code.org-style single-file projects."""

import contextlib
import hashlib
import io
import inspect


def run_01_simple_math():
    # Trace this code on paper. What does it print?
    x = 5
    y = 3
    z = x + y * 2
    print(z)


def run_02_string_building():
    # Trace this code on paper. What does it print?
    message = "Hello"
    message = message + " "
    message = message + "World"
    print(message)


def run_03_simple_loop():
    # Trace this code on paper. What does it print?
    for i in range(4):
        print(i)


def run_04_counting_up():
    # Trace this code on paper. What does it print?
    total = 0
    for i in range(1, 4):
        total = total + i
        print(total)


def run_05_building_a_word():
    # Trace this code on paper. What word is printed?
    word = ""
    for letter in "CAT":
        word = word + letter
        print(word)
    print("Final:", word)


def run_06_hidden_message():
    # Trace this code on paper. What secret message is revealed?
    text = "ACBADCEB"
    secret = ""
    for i in range(0, 8, 2):
        secret = secret + text[i]
    print(secret)


def run_07_pattern_loop():
    # Trace this code on paper. What pattern is printed?
    for row in range(3):
        line = ""
        for col in range(row + 1):
            line = line + "*"
        print(line)


def run_08_multi_accumulator():
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


def run_09_secret_code():
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


def run_10_integration_challenge():
    # Trace this code on paper step by step. What does it print?
    grid = ""
    for row in range(3):
        for col in range(4):
            if (row + col) % 2 == 0:
                grid = grid + "🟢"
            else:
                grid = grid + "⚪"
        grid = grid + "\n"
    print(grid)

    # And what is the final count?
    count = 0
    for char in grid:
        if char == "🟢":
            count = count + 1
    print("Green count:", count)


WARMUPS = {
    "1": ("Simple Math", run_01_simple_math),
    "2": ("String Building", run_02_string_building),
    "3": ("Simple Loop", run_03_simple_loop),
    "4": ("Counting Up", run_04_counting_up),
    "5": ("Building a Word", run_05_building_a_word),
    "6": ("Hidden Message", run_06_hidden_message),
    "7": ("Pattern Loop", run_07_pattern_loop),
    "8": ("Multi Accumulator", run_08_multi_accumulator),
    "9": ("Secret Code", run_09_secret_code),
    "10": ("Integration Challenge", run_10_integration_challenge),
}

ANSWER_PASSWORD_HASH = "198becaf9c45016fec5d9bcd2e8d748de6b44a26cd4cc35ea72b670e665dff79"
MAX_PASSWORD_ATTEMPTS = 5

RED = "\033[31m"
GREEN = "\033[32m"
RESET = "\033[0m"


PASSWORD_FAILURE_WARNINGS = [
    "Not correct yet. If you run out of attempts, you must re-enter every prediction.",
    "Still incorrect. Keep in mind: all predictions reset after 5 failed attempts.",
    "Nope. You are getting close to a full reset of your saved answers.",
    "Last warning before lockout. One more miss means retyping all answers.",
    "That was the 5th miss. You now need to re-enter every prediction from the start.",
]


def execute_exercise(exercise_function):
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        exercise_function()
    return buffer.getvalue().rstrip("\n")


def normalize_output(text):
    cleaned_lines = [line.rstrip() for line in text.strip().splitlines()]
    return "\n".join(cleaned_lines).strip()


def extract_green_count_line(text):
    for line in text.splitlines():
        stripped_line = line.strip()
        if stripped_line.startswith("Green count:"):
            return stripped_line
    return ""


def prediction_is_correct(item_number, predicted_text, actual_text):
    if item_number == "10":
        predicted_green_count = extract_green_count_line(predicted_text)
        actual_green_count = extract_green_count_line(actual_text)
        return predicted_green_count == actual_green_count

    predicted_normalized = normalize_output(predicted_text)
    actual_normalized = normalize_output(actual_text)
    return predicted_normalized == actual_normalized


def show_progress(index, total):
    percent = int((index / total) * 100)
    print("Progress: " + str(percent) + "% complete (" + str(index) + "/" + str(total) + ")")


def show_challenge(exercise_name, exercise_function):
    print()
    print("Trace this warmup before viewing the answer:")
    print(exercise_name)
    print("------------------------------")
    print(inspect.getsource(exercise_function))


def collect_student_answer():
    print("Type your predicted output below.")
    print("Press Enter on a blank line when you are done.")

    answer_lines = []
    while True:
        line = input()
        if line == "":
            break
        answer_lines.append(line)

    print()
    print("Prediction recorded.")
    return "\n".join(answer_lines)


def password_is_correct(password):
    encoded_password = password.strip().lower().encode("utf-8")
    password_hash = hashlib.sha256(encoded_password).hexdigest()
    return password_hash == ANSWER_PASSWORD_HASH


def show_intro(total):
    print()
    print("Warmup Trace Check")
    print("------------------")
    print("You will predict all " + str(total) + " warmups first, then unlock answers with a password.")


def collect_all_predictions(warmup_items):
    predictions = []
    total = len(warmup_items)

    for index, exercise in enumerate(warmup_items, start=1):
        print()
        print("Challenge " + str(index) + " of " + str(total) + ": " + exercise[1][0])
        show_challenge(exercise[1][0], exercise[1][1])
        if exercise[0] == "10":
            print("For this challenge, only enter your predicted line: Green count: X")
        student_answer = collect_student_answer()
        predictions.append(
            {
                "number": exercise[0],
                "name": exercise[1][0],
                "function": exercise[1][1],
                "predicted": student_answer,
            }
        )
        show_progress(index, total)

    return predictions


def unlock_answers_with_retries():
    print()
    print("All predictions are in. Enter the password to reveal answers.")

    for attempt in range(1, MAX_PASSWORD_ATTEMPTS + 1):
        password = input("Password attempt " + str(attempt) + " of " + str(MAX_PASSWORD_ATTEMPTS) + ": ")
        if password_is_correct(password):
            print("Password accepted.")
            return True

        print(PASSWORD_FAILURE_WARNINGS[attempt - 1])

    return False


def show_answer_report(predictions):
    print()
    print("Answer Key")
    print("----------")

    correct_count = 0
    mismatches = []

    for item in predictions:
        actual_output = execute_exercise(item["function"])
        is_correct = prediction_is_correct(item["number"], item["predicted"], actual_output)

        print()
        print(item["number"] + ". " + item["name"])
        print(actual_output)

        if is_correct:
            correct_count = correct_count + 1
        else:
            actual_for_compare = actual_output
            if item["number"] == "10":
                actual_for_compare = extract_green_count_line(actual_output)
            mismatches.append(
                {
                    "number": item["number"],
                    "name": item["name"],
                    "predicted": item["predicted"],
                    "actual": actual_for_compare,
                }
            )

    print()
    print("Summary")
    print("-------")
    print("Score: " + str(correct_count) + " / " + str(len(predictions)) + " correct")

    if not mismatches:
        print("Excellent tracing. All predictions were correct.")
        return

    print("Review incorrect predictions:")
    for mismatch in mismatches:
        student_text = mismatch["predicted"] if mismatch["predicted"].strip() else "[no prediction entered]"
        correct_text = mismatch["actual"] if mismatch["actual"].strip() else "[no output]"
        print()
        print(mismatch["number"] + ". " + mismatch["name"])
        print(RED + "Your answer:" + RESET)
        print(RED + student_text + RESET)
        print(GREEN + "Correct answer:" + RESET)
        print(GREEN + correct_text + RESET)


def main():
    warmup_items = list(WARMUPS.items())
    show_intro(len(warmup_items))

    while True:
        predictions = collect_all_predictions(warmup_items)
        if not unlock_answers_with_retries():
            print()
            print("Restarting trace mode. Re-enter all predictions.")
            continue

        show_answer_report(predictions)
        break

    print()
    print("Goodbye.")


main()