import sys
from engine.generator import Board

DEFAULT_SIZE = 4
DEFAULT_DIFFICULTY = 0

def main():
    size, difficulty = parse_arguments()
    crossword = Board(size, difficulty)
    crossword.genereate()

def parse_arguments():
    size = DEFAULT_SIZE
    difficulty = DEFAULT_DIFFICULTY

    if len(sys.argv) > 1:
        try:
            size = int(sys.argv[1])
        except ValueError:
            print(f"Invalid size argument. Using default size: {DEFAULT_SIZE}")

    if len(sys.argv) > 2:
        difficulty_arg = sys.argv[2].lower()
        if difficulty_arg in ["easy", "e"]:
            difficulty = 0
        elif difficulty_arg in ["medium", "m"]:
            difficulty = 1
        elif difficulty_arg in ["hard", "h"]:
            difficulty = 2
        else:
            print(f"Invalid difficulty argument. Using default difficulty: {DEFAULT_DIFFICULTY}")

    return size, difficulty

if __name__ == "__main__":
    main()