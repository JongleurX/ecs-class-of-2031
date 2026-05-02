"""Games driver menu (Code.org-friendly, standard library only).

How it works:
- Finds each game folder under games/ that contains a main.py file.
- Lets students choose a game from a menu.
- Runs the selected game using a small run/back menu.

Optional checker support:
- If a game folder has check.py, this driver will show a `c = check` option.
- `check.py` is executed as a script.
"""

import os
import runpy
import sys


def _resolve_games_root():
    """Find the games root in environments where __file__ may be missing."""
    if "__file__" in globals() and __file__:
        return os.path.dirname(os.path.abspath(__file__))

    cwd = os.getcwd()

    # If running from inside games/, use cwd directly.
    if os.path.isfile(os.path.join(cwd, "main.py")):
        return cwd

    # If running from project root, use ./games.
    games_dir = os.path.join(cwd, "games")
    if os.path.isdir(games_dir):
        return games_dir

    # Last-resort fallback.
    return cwd


GAMES_ROOT = _resolve_games_root()


def _pretty_name(folder_name):
    """Convert snake/kebab folder names to a friendly title."""
    return folder_name.replace("_", " ").replace("-", " ").title()


def discover_games():
    """Return menu-ready game entries discovered from subfolders."""
    entries = []
    for name in sorted(os.listdir(GAMES_ROOT)):
        full = os.path.join(GAMES_ROOT, name)
        if not os.path.isdir(full):
            continue
        if name.startswith("."):
            continue

        main_path = os.path.join(full, "main.py")
        check_path = os.path.join(full, "check.py")
        if os.path.isfile(main_path):
            entries.append(
                {
                    "folder": name,
                    "label": _pretty_name(name),
                    "main": main_path,
                    "check": check_path if os.path.isfile(check_path) else None,
                }
            )

    games = {}
    for i, item in enumerate(entries, start=1):
        games[str(i)] = item
    return games


def _show_menu(games):
    print()
    print("=" * 50)
    print("   Games  —  Runner")
    print("=" * 50)

    if not games:
        print("   No games found yet.")
    else:
        for key, item in games.items():
            print(f"   {key}.  {item['label']}  ({item['folder']})")

    print("   q.  Quit")
    print()


def _run_game_script(path):
    """Run a game script and handle common exit conditions."""
    abs_path = os.path.abspath(path)
    script_dir = os.path.dirname(abs_path)
    old_cwd = os.getcwd()

    try:
        # Make local game imports work (e.g., "from strategies import ...").
        if script_dir and script_dir not in sys.path:
            sys.path.insert(0, script_dir)

        # Some student files assume relative paths from their own folder.
        if script_dir:
            os.chdir(script_dir)

        runpy.run_path(abs_path, run_name="__main__")
    except SystemExit:
        # Some scripts intentionally call exit(); treat as normal.
        pass
    except Exception as err:
        print(f"\nError while running script: {err}")
    finally:
        os.chdir(old_cwd)
        if script_dir in sys.path:
            try:
                sys.path.remove(script_dir)
            except ValueError:
                pass


def _run_game_menu(item):
    print()
    print(f"--- Game: {item['label']} ---")
    print(f"Folder: {item['folder']}")
    print()

    while True:
        if item["check"]:
            print("  r = run   c = check   b = back")
        else:
            print("  r = run   b = back")

        choice = input("Choice: ").strip().lower()

        if choice == "b":
            return
        if choice == "r":
            print()
            _run_game_script(item["main"])
            continue
        if choice == "c" and item["check"]:
            print()
            _run_game_script(item["check"])
            continue

        if item["check"]:
            print("Please enter r, c, or b.")
        else:
            print("Please enter r or b.")


def main():
    print("\nWelcome to the Games Runner!")
    print("Choose a game, then run it from the game menu.\n")

    while True:
        games = discover_games()
        _show_menu(games)

        choice = input("Which game? (number or q) ").strip().lower()
        if choice == "q":
            print("See you next time!")
            break
        if choice in games:
            _run_game_menu(games[choice])
        else:
            print("Please enter a valid game number or q.")


if __name__ == "__main__":
    main()
