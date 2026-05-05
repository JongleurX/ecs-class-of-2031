"""Exercise 06: Japanese Character Tutor

Task:
1. Run the program and choose a mode (hiragana, katakana, or kanji).
2. Type the pronunciation of each character shown.
3. Add tracking features:
   - Display success rate as a percentage
   - Show total correct and incorrect answers
   - Track consecutive correct answers
4. Bonus: Do something special for 10, 20, 30 correct in a row!

Hint: Use variables to track correct_count, incorrect_count, and streak.
Calculate percentage with: (correct_count / (correct_count + incorrect_count)) * 100
"""

import random

HIRAGANA = {
    'あ': ['a'], 'い': ['i'], 'う': ['u'], 'え': ['e'], 'お': ['o'],
    'か': ['ka'], 'き': ['ki'], 'く': ['ku'], 'け': ['ke'], 'こ': ['ko'],
    'さ': ['sa'], 'し': ['shi', 'si'], 'す': ['su'], 'せ': ['se'], 'そ': ['so'],
    'た': ['ta'], 'ち': ['chi', 'ti'], 'つ': ['tsu', 'tu'], 'て': ['te'], 'と': ['to'],
    'な': ['na'], 'に': ['ni'], 'ぬ': ['nu'], 'ね': ['ne'], 'の': ['no'],
    'は': ['ha'], 'ひ': ['hi'], 'ふ': ['fu', 'hu'], 'へ': ['he'], 'ほ': ['ho'],
    'ま': ['ma'], 'み': ['mi'], 'む': ['mu'], 'め': ['me'], 'も': ['mo'],
    'や': ['ya'], 'ゆ': ['yu'], 'よ': ['yo'],
    'ら': ['ra'], 'り': ['ri'], 'る': ['ru'], 'れ': ['re'], 'ろ': ['ro'],
    'わ': ['wa'], 'を': ['wo', 'o'], 'ん': ['n']
}

KATAKANA = {
    'ア': ['a'], 'イ': ['i'], 'ウ': ['u'], 'エ': ['e'], 'オ': ['o'],
    'カ': ['ka'], 'キ': ['ki'], 'ク': ['ku'], 'ケ': ['ke'], 'コ': ['ko'],
    'サ': ['sa'], 'シ': ['shi', 'si'], 'ス': ['su'], 'セ': ['se'], 'ソ': ['so'],
    'タ': ['ta'], 'チ': ['chi', 'ti'], 'ツ': ['tsu', 'tu'], 'テ': ['te'], 'ト': ['to'],
    'ナ': ['na'], 'ニ': ['ni'], 'ヌ': ['nu'], 'ネ': ['ne'], 'ノ': ['no'],
    'ハ': ['ha'], 'ヒ': ['hi'], 'フ': ['fu', 'hu'], 'ヘ': ['he'], 'ホ': ['ho'],
    'マ': ['ma'], 'ミ': ['mi'], 'ム': ['mu'], 'メ': ['me'], 'モ': ['mo'],
    'ヤ': ['ya'], 'ユ': ['yu'], 'ヨ': ['yo'],
    'ラ': ['ra'], 'リ': ['ri'], 'ル': ['ru'], 'レ': ['re'], 'ロ': ['ro'],
    'ワ': ['wa'], 'ヲ': ['wo', 'o'], 'ン': ['n']
}

KANJI = {
    '一': ['ichi', 'hito'],
    '二': ['ni', 'futa'],
    '三': ['san', 'mi'],
    '四': ['yon', 'shi', 'si'],
    '五': ['go'],
    '日': ['nichi', 'jitsu', 'hi'],
    '月': ['getsu', 'gatsu', 'tsuki'],
    '火': ['ka', 'hi'],
    '水': ['sui', 'mizu'],
    '木': ['moku', 'boku', 'ki'],
    '金': ['kin', 'kon'],
    '土': ['do', 'to', 'tsuchi'],
    '天': ['ten'],
    '人': ['jin', 'nin', 'hito'],
    '大': ['dai', 'tai', 'oo']
}


def normalize_answers(value):
    """Return list of allowed answers for a dictionary value."""
    if isinstance(value, list):
        return [v.lower() for v in value]
    return [value.lower()]


def play_mode(character_dict, mode_name):
    """Main game loop for one selected character set."""
    print(f"\nWelcome to {mode_name} Tutor!")
    print("Type 'quit' to exit, 'stats' to see your progress.\n")

    correct_count = 0
    incorrect_count = 0
    streak = 0

    while True:
        char = random.choice(list(character_dict.keys()))
        correct_answer = character_dict[char]

        answer = input(f"What is the pronunciation of {char}? ").strip().lower()

        if answer == 'quit':
            print("Thanks for practicing! ありがとう!")
            break
        elif answer == 'stats':
            # TODO: Show statistics here
            # Calculate and display success rate, correct/incorrect counts
            print("Stats coming soon!")
        else:
            allowed_answers = normalize_answers(correct_answer)
            if answer in allowed_answers:
                print("✅ Correct!")
                # TODO: Update correct_count and streak
                # TODO: Check for streak milestones (10, 20, 30 correct in a row)
            else:
                if len(allowed_answers) == 1:
                    print(f"❌ Incorrect. The answer is '{allowed_answers[0]}'.")
                else:
                    print(f"❌ Incorrect. The answer can be one of: {', '.join(allowed_answers)}.")
                # TODO: Update incorrect_count and reset streak


def play_game_06():
    """Menu wrapper used by exercises/main.py."""
    print("Japanese Character Tutor")
    print("=" * 30)

    while True:
        print("\nChoose a mode:")
        print("1. Hiragana")
        print("2. Katakana")
        print("3. Kanji")
        print("4. Back")

        choice = input("\nEnter choice (1-4): ").strip()

        if choice == '1':
            play_mode(HIRAGANA, "Hiragana")
        elif choice == '2':
            play_mode(KATAKANA, "Katakana")
        elif choice == '3':
            play_mode(KANJI, "Kanji")
        elif choice == '4':
            print("Returning to runner menu.")
            break
        else:
            print("Please enter 1, 2, 3, or 4.")


def exercise_06():
    play_game_06()


if __name__ == "__main__":
    exercise_06()
