# Python Intro for Scratch Students

A set of beginner-friendly Python exercises designed for 11-12 year olds transitioning from Scratch to text-based coding.

Goals:
- Start with copy-edit / number changes
- Introduce variables, print, input, arithmetic, string operations
- Progress to writing simple functions with driver code
- Keep it pure Python (no pip, no extra libraries)

How to use:
1. Open a terminal in this folder.
2. Run `python3 exercises/01_hello_world.py` (or any exercise file).
3. Read the comments at the top of the file and make the changes asked.
4. Re-run to check behavior.

Structure:
- `exercises/` contains numbered exercises.
- `teacher-guide/` contains suggested solutions (optional for teacher use).

Exercise 07 Notes:
- Simplified to focus on abstraction: same geometry functions create different flags
- Vertical stripes: France (blue-white-red left-to-right) and Italy (green-white-red left-to-right)
- Horizontal stripes: Germany (black-red-yellow top-to-bottom, 3 stripes) and Ukraine (blue-yellow top-to-bottom, 2 stripes)
- Circle flags: Japan (red circle on white) and Bangladesh (green circle on red background)
- Students fix WRONG function calls and parameters to make flags correct
- Demonstrates how geometry code stays the same while colors and orientations change
- Uses ANSI color codes for terminal display (works in most modern terminals)
- Solutions file: 07a_flag_painter_solutions.py shows all flags correct

Current Exercises:
1. Hello World - Simple variable editing
2. Calculator - Fix a typo and change values  
3. Number Guessing Game - Binary search with helper mode
4. Function Practice - Implement greet_user() and is_even()
5. Lists and Loops - Add animals, uppercase loop, vowel counter
6. Japanese Tutor - Character recognition with progress tracking
7. Flag Painter - Fix function calls and parameters for 6 flags (France, Italy, Germany, Ukraine, Japan, Bangladesh)

Have fun learning programming! 🌟
