"""Exercises 01-07 — driver / checker.

Students: open the exercise file for your current exercise (e.g. ex03_guessing_game.py),
read the task at the top, and edit the TODO / FIXME sections.
Then come back here and run this file to check your work.

Files:
  ex01_hello_world.py
  ex02_typo_calculator.py
  ex03_guessing_game.py
  ex04_functions.py
  ex05_list_tricks.py
  ex06_japanese_tutor.py
  ex07_flag_painter.py
"""

import contextlib
import ast
import inspect
import io

# ── import student exercise code ──────────────────────────────
from ex01_hello_world      import exercise_01
from ex02_typo_calculator  import exercise_02
from ex03_guessing_game    import helper_hint, exercise_03
from ex04_functions        import greet_user, is_even, exercise_04
from ex05_list_tricks      import exercise_05
from ex06_japanese_tutor   import play_game_06
import ex07_flag_painter as ex07


# ═══════════════════════════════════════════════════════════════
#  CHECK FUNCTIONS  (students do not need to read this section)
# ═══════════════════════════════════════════════════════════════

def check_01():
    src = inspect.getsource(exercise_01)
    if "Scratch Kid" in src:
        print("Not done yet — change your_name away from 'Scratch Kid'.")
        return False
    if "fav_number = 7" in src:
        print("Not done yet — change fav_number to your favourite number (not 7).")
        return False
    print("Exercise 01 complete!  Great job.")
    return True


def check_02():
    src = inspect.getsource(exercise_02)
    if ".stirp()" in src:
        print("Not fixed yet — there is still a typo in one of the method names.")
        print("Hint: look very carefully at how .strip() is spelled.")
        return False
    if ".strip()" not in src:
        print("Hmm — make sure you are still calling .strip() on the input.")
        return False
    print("Exercise 02 complete!  You found and fixed the typo.")
    return True


def check_03():
    r1 = helper_hint(1, 100)
    r2 = helper_hint(1, 10)

    if "100" not in r1:
        print(f"helper_hint(1, 100) should say '100 numbers left'.  Got: {r1}")
        return False
    if "50" not in r1 and "51" not in r1:
        print(f"helper_hint(1, 100) should suggest trying 50.  Got: {r1}")
        return False
    if "10" not in r2:
        print(f"helper_hint(1, 10) should say '10 numbers left'.  Got: {r2}")
        return False
    if "5" not in r2 and "6" not in r2:
        print(f"helper_hint(1, 10) should suggest trying 5.  Got: {r2}")
        return False
    print("Exercise 03 complete!  helper_hint() is working correctly.")
    return True


def check_04():
    result = greet_user("Sophie")
    if not result:
        print("greet_user() is still returning an empty string — add a greeting!")
        return False
    if "Sophie" not in str(result):
        print(f'greet_user("Sophie") should include "Sophie".  Got: {repr(result)}')
        return False

    cases = [(0, True), (1, False), (2, True), (7, False), (100, True), (99, False)]
    for n, expected in cases:
        got = is_even(n)
        if got is not expected:
            print(f"is_even({n}) should return {expected}, got {got}")
            return False

    print("Exercise 04 complete!  Both functions work correctly.")
    return True


def check_05():
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        exercise_05()
    output = buf.getvalue()

    for line in output.splitlines():
        if "Total animals:" in line:
            try:
                count = int(line.split(":")[1].strip())
            except ValueError:
                count = 0
            if count <= 3:
                print(f"Not done yet — add a new animal (currently {count}).")
                return False
            break

    src = inspect.getsource(exercise_05)
    if ".upper()" not in src:
        print("Not done yet — add a loop that prints each animal in uppercase.")
        return False

    print("Exercise 05 complete!  List updated and uppercase loop added.")
    return True


def check_06():
    src = inspect.getsource(play_game_06)
    mode_fn = getattr(__import__("ex06_japanese_tutor"), "play_mode", None)
    if mode_fn is not None:
        src = src + "\n" + inspect.getsource(mode_fn)
    issues = []

    if "correct_count +=" not in src and "correct_count = correct_count +" not in src:
        issues.append("correct_count is not being updated when the answer is right")

    if "incorrect_count +=" not in src and "incorrect_count = incorrect_count +" not in src:
        issues.append("incorrect_count is not being updated when the answer is wrong")

    has_streak_inc   = "streak +=" in src or "streak = streak +" in src
    has_streak_reset = "streak = 0" in src
    if not (has_streak_inc and has_streak_reset):
        issues.append("streak is not being incremented on correct answers and reset on wrong ones")

    if "Stats coming soon" in src:
        issues.append("the 'stats' command still says 'coming soon' — implement real stats")

    if issues:
        for issue in issues:
            print("Not done:", issue)
        return False

    print("Exercise 06 complete!  Tracking is implemented.")
    return True


def _has_color(line, color):
    return f"'{color}'" in line or f'"{color}"' in line


def _extract_assignment_expr(source_text, var_name):
    for raw_line in source_text.splitlines():
        line = raw_line.split("#", 1)[0].strip()
        if line.startswith(var_name + " =") or line.startswith(var_name + "="):
            return line.split("=", 1)[1].strip()
    return ""


def _safe_eval_arithmetic(expr, names):
    allowed_nodes = (
        ast.Expression,
        ast.BinOp,
        ast.UnaryOp,
        ast.Add,
        ast.Sub,
        ast.Mult,
        ast.Div,
        ast.FloorDiv,
        ast.Mod,
        ast.Pow,
        ast.UAdd,
        ast.USub,
        ast.Name,
        ast.Load,
        ast.Constant,
        ast.Call,
    )

    tree = ast.parse(expr, mode="eval")
    for node in ast.walk(tree):
        if not isinstance(node, allowed_nodes):
            raise ValueError("unsupported expression")
        if isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name) or node.func.id not in {"min", "max"}:
                raise ValueError("unsupported function call")

    return eval(compile(tree, "<expr>", "eval"), {"__builtins__": {}}, names)


def check_07():
    exercise_07_fn = getattr(ex07, "exercise_07", None)
    if exercise_07_fn is None:
        print("Not done: exercise_07() is missing from ex07_flag_painter.py")
        return False

    src = inspect.getsource(exercise_07_fn)
    circle_fn = getattr(ex07, "circle_flag", None)
    circle_src = inspect.getsource(circle_fn) if circle_fn is not None else ""
    width_value = getattr(ex07, "WIDTH", 50)
    height_value = getattr(ex07, "HEIGHT", 26)
    issues = []

    def assignment_line(var):
        for line in src.splitlines():
            s = line.strip()
            if s.startswith(var + " =") or s.startswith(var + "="):
                return s
        return ""

    f1 = assignment_line("flag1")
    f2 = assignment_line("flag2")
    f3 = assignment_line("flag3")
    f4 = assignment_line("flag4")
    f5 = assignment_line("flag5")
    f6 = assignment_line("flag6")

    if "vertical_stripes" not in f1:
        issues.append("France (flag1): should use vertical_stripes()")
    elif not (_has_color(f1, 'blue') and _has_color(f1, 'white') and _has_color(f1, 'red')):
        issues.append("France (flag1): needs blue, white, and red stripes")

    if "vertical_stripes" not in f2:
        issues.append("Italy (flag2): should use vertical_stripes()")
    elif not (_has_color(f2, 'green') and _has_color(f2, 'white') and _has_color(f2, 'red')):
        issues.append("Italy (flag2): needs green, white, and red stripes")

    if "horizontal_stripes" not in f3:
        issues.append("Germany (flag3): should use horizontal_stripes()")
    elif not (_has_color(f3, 'black') and _has_color(f3, 'red') and _has_color(f3, 'yellow')):
        issues.append("Germany (flag3): needs black, red, and yellow stripes")

    if "horizontal_stripes" not in f4:
        issues.append("Ukraine (flag4): should use horizontal_stripes()")
    elif not (_has_color(f4, 'blue') and _has_color(f4, 'yellow')):
        issues.append("Ukraine (flag4): needs blue and yellow stripes")

    if "circle_flag" not in f5:
        issues.append("Japan (flag5): should use circle_flag()")
    elif not _has_color(f5, 'red'):
        issues.append("Japan (flag5): the circle should be red")
    elif not _has_color(f5, 'white'):
        issues.append("Japan (flag5): the background should be white")

    if "circle_flag" not in f6:
        issues.append("Bangladesh (flag6): should use circle_flag()")
    elif not _has_color(f6, 'red'):
        issues.append("Bangladesh (flag6): the circle should be red")
    elif not _has_color(f6, 'green'):
        issues.append("Bangladesh (flag6): the background should be green")

    center_expr = _extract_assignment_expr(circle_src, "center_x")
    radius_expr = _extract_assignment_expr(circle_src, "radius")

    if circle_fn is None:
        issues.append("circle_flag() is missing")

    if not center_expr:
        issues.append("circle_flag(): center_x assignment is missing")
    else:
        try:
            center_value = _safe_eval_arithmetic(center_expr, {"WIDTH": width_value, "HEIGHT": height_value, "min": min, "max": max})
            if center_value != width_value // 2:
                issues.append("circle_flag(): center_x should be WIDTH // 2")
        except Exception:
            issues.append("circle_flag(): center_x expression could not be checked")

    if not radius_expr:
        issues.append("circle_flag(): radius assignment is missing")
    else:
        try:
            radius_value = _safe_eval_arithmetic(radius_expr, {"WIDTH": width_value, "HEIGHT": height_value, "min": min, "max": max})
            diameter_value = 2 * radius_value
            min_diameter = height_value / 3
            max_diameter = (3 * height_value) / 5
            tolerance = 1
            if not (min_diameter - tolerance <= diameter_value <= max_diameter + tolerance):
                issues.append(
                    "circle_flag(): diameter should be between 1/3 and 3/5 of HEIGHT"
                )
        except Exception:
            issues.append("circle_flag(): radius expression could not be checked")

    if issues:
        for issue in issues:
            print("Not done:", issue)
        return False

    print("Exercise 07 complete!  All flags have the correct orientation and colors.")
    return True


# ═══════════════════════════════════════════════════════════════
#  DRIVER MENU
# ═══════════════════════════════════════════════════════════════

EXERCISES = {
    "1": ("Hello World",             exercise_01,  check_01, False),
    "2": ("Fix the Typo Calculator", exercise_02,  check_02, True),
    "3": ("Number Guessing Game",    exercise_03,  check_03, True),
    "4": ("Function Practice",       exercise_04,  check_04, True),
    "5": ("List Tricks",             exercise_05,  check_05, False),
    "6": ("Japanese Tutor",          play_game_06, check_06, True),
    "7": ("Flag Painter",            ex07.exercise_07,  check_07, False),
}

TASKS = {
    "1": "Open ex01_hello_world.py — change your_name and fav_number.",
    "2": "Open ex02_typo_calculator.py — find and fix the typo in the method name.",
    "3": "Open ex03_guessing_game.py — fix helper_hint() (count and middle).",
    "4": "Open ex04_functions.py — implement greet_user() and is_even().",
    "5": "Open ex05_list_tricks.py — add a new animal and an uppercase loop.",
    "6": "Open ex06_japanese_tutor.py — add tracking variables and real stats.",
    "7": "Open ex07_flag_painter.py — fix the function calls so each flag is correct.",
}


def _show_menu():
    print()
    print("=" * 50)
    print("   Exercises 01-07  —  Runner & Checker")
    print("=" * 50)
    for key, (name, _, _, _) in EXERCISES.items():
        print(f"   {key}.  {name}")
    print("   q.  Quit")
    print()


def _run_exercise_menu(key):
    name, run_fn, check_fn, is_interactive = EXERCISES[key]
    print()
    print(f"--- Exercise {key.zfill(2)}: {name} ---")
    print(f"Task: {TASKS[key]}")
    print()

    while True:
        if is_interactive:
            print("  r = run (interactive)   c = check   b = back")
        else:
            print("  r = run   c = check   b = back")

        choice = input("Choice: ").strip().lower()

        if choice == "b":
            return
        elif choice == "r":
            print()
            try:
                run_fn()
            except AttributeError as err:
                print(f"\nError: {err}")
                print("Hint: a method name is spelled incorrectly.")
            except Exception as err:
                print(f"\nError: {err}")
        elif choice == "c":
            print()
            # Reload the exercise module so changes are picked up without restarting
            import importlib, sys
            mod_map = {
                "1": "ex01_hello_world",   "2": "ex02_typo_calculator",
                "3": "ex03_guessing_game", "4": "ex04_functions",
                "5": "ex05_list_tricks",   "6": "ex06_japanese_tutor",
                "7": "ex07_flag_painter",
            }
            mod_name = mod_map[key]
            if mod_name in sys.modules:
                importlib.reload(sys.modules[mod_name])
            check_fn()
        else:
            print("Please enter r, c, or b.")


def main():
    print("\nWelcome to the Exercise Runner!")
    print("Open the exercise file listed in each task, make your changes,")
    print("then come back here and press c to check.\n")

    while True:
        _show_menu()
        choice = input("Which exercise? (1-7 or q) ").strip().lower()
        if choice == "q":
            print("See you next time!")
            break
        if choice in EXERCISES:
            _run_exercise_menu(choice)
        else:
            print("Please enter a number 1-7 or q.")


main()
