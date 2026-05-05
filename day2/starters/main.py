"""Starter Activities launcher.

Runs any Python file in this folder (except this main.py file).
"""

import os
import runpy

HERE = os.path.dirname(os.path.abspath(__file__))

# Student quick-launch toggle:
# - Leave blank ("") to use the menu.
# - Set to a file in this folder to run it directly from main.py.
# Example: "guessing_game.py"
QUICK_RUN_FILE = ""

DISPLAY = {
    "hello_world": ("👋", "Hello World"),
    "typo_calculator": ("🧮", "Typo Calculator"),
    "guessing_game": ("🎯", "Guessing Game"),
    "functions": ("🧩", "Functions"),
    "list_tricks": ("📚", "List Tricks"),
    "japanese_tutor": ("🗾", "Japanese Tutor"),
    "flag_painter": ("🎌", "Flag Painter"),
}


def polished_title(filename):
    stem = os.path.splitext(filename)[0].replace("-", "_")
    if stem in DISPLAY:
        return DISPLAY[stem][1]
    return " ".join(part.capitalize() for part in stem.split("_") if part)


def icon_for(filename):
    stem = os.path.splitext(filename)[0].replace("-", "_")
    if stem in DISPLAY:
        return DISPLAY[stem][0]
    return "📄"


def discover_scripts():
    items = []
    for name in sorted(os.listdir(HERE)):
        if not name.endswith(".py"):
            continue
        if name in {"main.py"}:
            continue
        if name.startswith(".") or name.startswith("_"):
            continue

        items.append(
            {
                "filename": name,
                "title": polished_title(name),
                "icon": icon_for(name),
                "path": os.path.join(HERE, name),
            }
        )

    return items


def resolve_quick_run(items):
    target = QUICK_RUN_FILE.strip()
    if not target:
        return None

    if not target.endswith(".py"):
        target += ".py"

    for item in items:
        if item["filename"].lower() == target.lower():
            return item

    print(f"Quick-run file not found: {target}")
    print("Falling back to starter menu.")
    return None


def show_menu(items):
    print("\n" + "=" * 56)
    print("Starter Activities")
    print("=" * 56)

    if not items:
        print("No Python starter files found.")
        return

    title_width = max(len(item["title"]) for item in items)
    for idx, item in enumerate(items, start=1):
        print(f"{idx:>2}. {item['icon']}  {item['title']:<{title_width}}   [{item['filename']}]")

    print("-" * 56)
    print("q. Return to Day 2 menu")
    print("=" * 56)


def run_script(item, pause_after=True):
    print("\n" + "-" * 56)
    print(f"Running: {item['filename']}")
    print("-" * 56)
    try:
        runpy.run_path(item["path"], run_name="__main__")
    except KeyboardInterrupt:
        print("\n(Returned to starter menu)")
    except Exception as err:
        print(f"\nScript error: {err}")
    print("-" * 56)
    if pause_after:
        input("Press Enter to return to the starter menu...")


def main():
    while True:
        items = discover_scripts()

        quick_item = resolve_quick_run(items)
        if quick_item is not None:
            run_script(quick_item, pause_after=False)
            break

        show_menu(items)

        if not items:
            break

        choice = input("Choose a starter number: ").strip().lower()
        if choice in ("q", "quit", "exit"):
            break

        if not choice.isdigit():
            print("Please enter a number from the list.")
            continue

        idx = int(choice)
        if idx < 1 or idx > len(items):
            print("That number is not in the list.")
            continue

        run_script(items[idx - 1])


if __name__ == "__main__":
    main()
