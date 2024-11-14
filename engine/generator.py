import re
import json
import random

from engine.cell import Cell, CHARS
from engine.llm.clue_generator import get_llm_response

DEBUG = False


def print_debug(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)


class Board:

    def __init__(self, difficulty=0, shape=None, useLLM=True):
        self.difficulty = difficulty
        self.filename = f"words_{['easy', 'medium', 'hard'][difficulty]}.txt"
        self.counter = 0
        self.complete = False
        self.shapes = self._read_shapes_file()
        self.useLLM = useLLM
        self.clues = None

        self.shape = random.choice(self.shapes) if not shape else shape
        self.grid = self._create_grid()
        self._setup_grid()

        self.words = self._read_words(self.filename)

    def generate(self):
        if len(self.grid) < 2:
            print("Must have at least 2 cells in shape to generate")
            return None

        while not self.complete:
            self._collapse()
        self._visualize()

        across, down = self._return_finshed_words()
        print(f"Across: {across}")
        print(f"Down: {down}")

        self._get_clues()

    def _collapse(self):
        choice = self._pick()
        if choice:
            cord = choice.cord
            self.grid[cord].observe()
        else:
            return None

        self._update()

    def _update(self):
        for cell in self.grid.values():
            if not cell.collapsed:
                cell.options = self._get_possible_chars(cell)
                cell.ent = len(cell.options)
                if len(cell.options) == 0:
                    self._backtrack(cell)

    def _backtrack(self, problem_cell):
        self.counter += 1
        if self.counter > 100:
            print_debug("Backtrack limit reached, full reset")
            if DEBUG:
                self._visualize()
            for cell in self.grid.values():
                cell.reset()
            self.counter = 0
        else:
            for cell in self.grid.values():
                if cell.x == problem_cell.x or cell.y == problem_cell.y:
                    cell.reset()

    def _pick(self):
        uncollapsed_cells = [cell for cell in self.grid.values() if not cell.collapsed]

        if not uncollapsed_cells:
            print("All cells have been collapsed")
            self.complete = True
            return None

        least_entropy = min(cell.ent for cell in uncollapsed_cells)
        least_entropy_cells = [
            cell for cell in uncollapsed_cells if cell.ent == least_entropy
        ]

        # print(f'Least entropy: {least_entropy_cells}')
        return random.choice(least_entropy_cells)

    def _get_possible_chars(self, cell):
        res, hPotential, vPotential = set(), set(CHARS), set(CHARS)
        current_words = self._get_finished_words()

        if cell.has_horizontal:
            horizontal_word = self._get_word_at(cell.x, cell.y, horizontal=True)
            h_spot = cell.x - (self._get_word_start(cell.x, cell.y, horizontal=True))[0]
            hPotential = self._get_potential(horizontal_word, h_spot, current_words)
        if cell.has_vertical:
            vertical_word = self._get_word_at(cell.x, cell.y, horizontal=False)
            v_spot = (
                cell.y - (self._get_word_start(cell.x, cell.y, horizontal=False))[1]
            )
            vPotential = self._get_potential(vertical_word, v_spot, current_words)

        res = hPotential.intersection(vPotential)

        return res

    def _get_potential(self, word, spot, finished_words):
        potential = set()
        valid = self._search_with_regex(word)

        if valid == self.words:
            return set(CHARS)

        for word in valid:
            if word not in finished_words and len(word) > spot:
                potential.add(word[spot])

        return potential

    def _get_finished_words(self):
        finished_words = []
        visited_starts = set()

        def is_word_start(x, y, horizontal):
            if horizontal:
                return (x - 1, y) not in self.grid
            else:
                return (x, y - 1) not in self.grid

        for x, y in self.grid:
            if self.grid[(x, y)].has_horizontal:
                if is_word_start(x, y, True) and (x, y, True) not in visited_starts:
                    word = self._get_word_at(x, y, horizontal=True)
                    if "_" not in word:
                        finished_words.append(word)
                        visited_starts.add((x, y, True))

            if self.grid[(x, y)].has_vertical:
                if is_word_start(x, y, False) and (x, y, False) not in visited_starts:
                    word = self._get_word_at(x, y, horizontal=False)
                    if "_" not in word:
                        finished_words.append(word)
                        visited_starts.add((x, y, False))

        return finished_words

    def _return_finshed_words(self):
        horizontal_words, vertical_words = [], []
        visited_starts = set()

        def is_word_start(x, y, horizontal):
            if horizontal:
                return (x - 1, y) not in self.grid
            else:
                return (x, y - 1) not in self.grid

        for x, y in self.grid:
            if self.grid[(x, y)].has_horizontal:
                if is_word_start(x, y, True) and (x, y, True) not in visited_starts:
                    word = self._get_word_at(x, y, horizontal=True)
                    if "_" not in word:
                        horizontal_words.append(word)
                        visited_starts.add((x, y, True))

            if self.grid[(x, y)].has_vertical:
                if is_word_start(x, y, False) and (x, y, False) not in visited_starts:
                    word = self._get_word_at(x, y, horizontal=False)
                    if "_" not in word:
                        vertical_words.append(word)
                        visited_starts.add((x, y, False))

        return horizontal_words, vertical_words

    def _search_with_regex(self, pattern):
        if "_" not in pattern:
            return {pattern} if pattern in self.words else set()
        elif pattern.count("_") == len(pattern):
            return {word for word in self.words if len(word) == len(pattern)}

        regex_pattern = pattern.replace("_", ".")
        regex = re.compile(f"^{regex_pattern}$")
        return {
            word
            for word in self.words
            if regex.match(word) and len(word) == len(pattern)
        }

    def _create_grid(self):
        grid = {}
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell == "_":
                    grid[(x, y)] = Cell(x, y)
        return grid

    def _setup_grid(self):
        for cord in self.grid:
            if (
                self._get_word_start(cord[0], cord[1], horizontal=True)
                == (cord[0], cord[1])
                and (cord[0] + 1, cord[1]) not in self.grid
            ):
                self.grid[(cord[0], cord[1])].has_horizontal = False
            if (
                self._get_word_start(cord[0], cord[1], horizontal=False)
                == (cord[0], cord[1])
                and (cord[0], cord[1] + 1) not in self.grid
            ):
                self.grid[(cord[0], cord[1])].has_vertical = False

    def _get_word_at(self, x, y, horizontal=True):
        word = []
        start_x, start_y = self._get_word_start(x, y, horizontal)
        dx, dy = (1, 0) if horizontal else (0, 1)

        while (start_x, start_y) in self.grid:
            word.append(self.grid[(start_x, start_y)].char)
            start_x += dx
            start_y += dy

        return "".join(word)

    def _get_word_start(self, x, y, horizontal=True):
        dx, dy = (-1, 0) if horizontal else (0, -1)
        while (x + dx, y + dy) in self.grid:
            x += dx
            y += dy
        return x, y

    def _visualize(self):
        for y in range(len(self.shape)):
            for x in range(len(self.shape[0])):
                if (x, y) in self.grid:
                    if self.grid[(x, y)].collapsed:
                        print(self.grid[(x, y)].char, end="  ")
                    else:
                        print("_", end="  ")
                else:
                    print("X", end="  ")
            print("\n")

    def _visualize_ent(self):
        for y in range(len(self.shape)):
            for x in range(len(self.shape[0])):
                if (x, y) in self.grid:
                    print(self.grid[(x, y)].ent, end="  ")
                else:
                    print("X", end="  ")
            print("\n")

    def _read_words(self, fileName):
        words = set()
        with open(f"engine/words/{fileName}", "r") as f:
            for line in f:
                word = line.strip()
                if any(
                    len(word) == len(self._get_word_at(x, y, horizontal=True))
                    or len(word) == len(self._get_word_at(x, y, horizontal=False))
                    for x, y in self.grid
                ):
                    words.add(word)
        return words

    def _read_shapes_file(self, filename="engine/shapes.txt"):
        shapes = []
        current_shape = []

        with open(filename, "r") as file:
            for line in file:
                line = line.strip()
                if line:
                    current_shape.append(line)
                else:
                    if current_shape:
                        shapes.append(current_shape)
                        current_shape = []

            if current_shape:
                shapes.append(current_shape)

        return shapes

    def _get_clues(self):
        if not self.useLLM:
            print("LLM is not enabled, generating mock clues")
            self.clues = {
                "across_clues": {
                    word: "Mock clue" for word in self._return_finshed_words()[0]
                },
                "down_clues": {
                    word: "Mock clue" for word in self._return_finshed_words()[1]
                },
            }
            return None

        across, down = self._return_finshed_words()
        res = json.loads(get_llm_response(across, down))
        print("Down")
        for word, clue in res["down_clues"].items():
            print(f"{word}: {clue}")
        print("\n")
        print("Across")
        for word, clue in res["across_clues"].items():
            print(f"{word}: {clue}")

        self.clues = res

    def _rle(self):
        if not self.shape:
            return ""

        result = []
        current_char = self.shape[0][0]
        count = 0

        flattened = "".join(self.shape)

        for char in flattened:
            if char == current_char:
                count += 1
            else:
                result.append(f"{count}{current_char}")
                current_char = char
                count = 1

        result.append(f"{count}{current_char}")
        return "".join(result)

    def get_json(self):
        if not self.complete or not self.clues:
            print("Cannot generate JSON until board is complete")
            return None

        across, down = {}, {}
        aCount, dCount = 1, 1
        finished_words = []
        visited_starts = set()

        def is_word_start(x, y, horizontal):
            if horizontal:
                return (x - 1, y) not in self.grid
            else:
                return (x, y - 1) not in self.grid

        for x, y in self.grid:
            if self.grid[(x, y)].has_horizontal:
                if is_word_start(x, y, True) and (x, y, True) not in visited_starts:
                    word = self._get_word_at(x, y, horizontal=True)
                    visited_starts.add((x, y, True))
                    across[aCount] = {
                        "clue": self.clues["across_clues"][word],
                        "answer": word.capitalize(),
                        "row": y,
                        "col": x,
                    }
                    aCount += 1

            if self.grid[(x, y)].has_vertical:
                if is_word_start(x, y, False) and (x, y, False) not in visited_starts:
                    word = self._get_word_at(x, y, horizontal=False)
                    visited_starts.add((x, y, False))
                    down[dCount] = {
                        "clue": self.clues["down_clues"][word],
                        "answer": word.capitalize(),
                        "row": y,
                        "col": x,
                    }
                    dCount += 1
        return {
            "across": across,
            "down": down,
        }
