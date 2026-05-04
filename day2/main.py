"""Day 2 launcher.

Discovers and runs Python scripts in this folder and all subfolders.
"""

import os
import runpy
import sys


DAY_LABEL = "Day 2"


def resolve_day_root():
    if "__file__" in globals() and __file__:
        return os.path.dirname(os.path.abspath(__file__))
    return os.getcwd()


DAY_ROOT = resolve_day_root()
THIS_FILE = os.path.abspath(__file__) if "__file__" in globals() and __file__ else ""


def polished_title(path):
    stem = os.path.splitext(os.path.basename(path))[0]
    return " ".join(part.capitalize() for part in stem.replace("-", "_").split("_") if part)


def discover_scripts():
    items = []
    for root, dirs, files in os.walk(DAY_ROOT):
        dirs[:] = [d for d in dirs if not d.startswith(".") and d != "__pycache__"]
        for filename in sorted(files):
            if not filename.endswith(".py"):
                continue
            if filename.startswith(".") or filename.startswith("_"):
                continue

            path = os.path.join(root, filename)
            if THIS_FILE and os.path.abspath(path) == THIS_FILE:
                continue

            rel_path = os.path.relpath(path, DAY_ROOT)
            items.append(
                {
                    "title": polished_title(path),
                    "relative_path": rel_path,
                    "absolute_path": path,
                }
            )

    items.sort(key=lambda item: item["relative_path"].lower())
    return items


def show_menu(items):
    print("\n" + "=" * 72)
    print(f"{DAY_LABEL} Python Launcher")
    print("=" * 72)

    if not items:
        print("No Python files found under this day folder yet.")
        print("-" * 72)
        print("q. Quit")
        print("=" * 72)
        return

    width = max(len(item["relative_path"]) for item in items)
    for idx, item in enumerate(items, start=1):
        print(f"{idx:>2}. {item['relative_path']:<{width}}  -  {item['title']}")

    print("-" * 72)
    print("q. Quit")
    print("=" * 72)


def run_script(item):
    path = os.path.abspath(item["absolute_path"])
    script_dir = os.path.dirname(path)
    old_cwd = os.getcwd()
    added_path = False

    print("\n" + "-" * 72)
    print(f"Running: {item['relative_path']}")
    print("-" * 72)

    try:
        if script_dir and script_dir not in sys.path:
            sys.path.insert(0, script_dir)
            added_path = True

        if script_dir:
            os.chdir(script_dir)

        runpy.run_path(path, run_name="__main__")
    except KeyboardInterrupt:
        print("\n(Returned to menu)")
    except SystemExit:
        pass
    except Exception as err:
        print(f"Error while running script: {err}")
    finally:
        os.chdir(old_cwd)
        if added_path:
            try:
                sys.path.remove(script_dir)
            except ValueError:
                pass

    print("-" * 72)
    input("Press Enter to return to the menu...")


def main():
    while True:
        items = discover_scripts()
        show_menu(items)

        choice = input("Choose a number or q: ").strip().lower()
        if choice in ("q", "quit", "exit"):
            print("Bye!")
            break

        if not items:
            print("There are no runnable files yet.")
            continue

        if not choice.isdigit():
            print("Please enter a number from the list.")
            continue

        index = int(choice)
        if index < 1 or index > len(items):
            print("That number is not in the list.")
            continue

        run_script(items[index - 1])


if __name__ == "__main__":
    main()
