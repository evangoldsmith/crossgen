import sys
from engine.generator import Board

DEFAULT_DIFFICULTY = 0

SHAPE = [
    "X_X_X",
    "_____",
    "X_X_X",
    "_____",
    "X_X_X",
]

def main():
    difficulty = parse_arguments()
    crossword = Board(difficulty)
    crossword._visualize()

    crossword.generate()

def parse_arguments():
    difficulty = DEFAULT_DIFFICULTY

    if len(sys.argv) > 1:
        difficulty_arg = sys.argv[1].lower()
        if difficulty_arg in ["easy", "e"]:
            difficulty = 0
        elif difficulty_arg in ["medium", "m"]:
            difficulty = 1
        elif difficulty_arg in ["hard", "h"]:
            difficulty = 2
        else:
            print(f"Invalid difficulty argument. Using default difficulty: {DEFAULT_DIFFICULTY}")

    return difficulty

if __name__ == "__main__":
    main()