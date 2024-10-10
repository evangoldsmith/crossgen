import re
import random

from engine.cell import Cell, CHARS

DEBUG = False

def print_debug(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)

class Board:

    def __init__(self, difficulty=0):
        self.difficulty = difficulty
        self.filename = f"words_{['easy', 'medium', 'hard'][difficulty]}.txt"
        self.counter = 0
        self.complete = False
        self.shapes = self.read_shapes_file()

        self.shape = random.choice(self.shapes)
        self.grid = self._create_grid()

        self.words = self._read_words(self.filename)

    def generate(self):
        while not self.complete:
            self._collapse()
        self._visualize()

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
        if self.counter > 200:
            print_debug("Backtrack limit reached, full reset")
            for cell in self.grid.values():
                cell.reset()
            self.counter = 0
        else:
            for cell in self.grid.values():
                if (cell.x == problem_cell.x or cell.y == problem_cell.y):
                    cell.reset()
    
    def _pick(self):
        uncollapsed_cells = [cell for cell in self.grid.values() if not cell.collapsed]

        if not uncollapsed_cells:
            print("All cells have been collapsed")
            self.complete = True
            return None

        least_entropy = min(cell.ent for cell in uncollapsed_cells)
        least_entropy_cells = [cell for cell in uncollapsed_cells if cell.ent == least_entropy]

        # print(f'Least entropy: {least_entropy_cells}')
        return random.choice(least_entropy_cells)
    
    def _get_possible_chars(self, cell):
        res, hPotential, vPotential = set(), set(), set()
        current_words = self._get_finished_words()

        horizontal_word = self._get_word_at(cell.x, cell.y, horizontal=True)
        vertical_word = self._get_word_at(cell.x, cell.y, horizontal=False)

        possible_horizontal = self._search_with_regex(horizontal_word)
        possible_vertical = self._search_with_regex(vertical_word)

        # print(f"Horizontal: {possible_horizontal}")
        # print(f"Vertical: {possible_vertical}")

        if possible_horizontal == self.words and possible_vertical == self.words:
            return set(CHARS)
        
        if possible_horizontal == self.words: hPotential = set(CHARS)
        if possible_vertical == self.words: vPotential = set(CHARS)

        h_spot, v_spot = cell.x - (self._get_word_start(cell.x, cell.y, horizontal=True))[0], cell.y - (self._get_word_start(cell.x, cell.y, horizontal=False))[1]

        if possible_horizontal and possible_horizontal != self.words:
            for word in possible_horizontal:
                if word not in current_words and len(word) > h_spot: hPotential.add(word[h_spot])

        if possible_vertical and possible_vertical != self.words:
            for word in possible_vertical:
                if word not in current_words and len(word) > v_spot: vPotential.add(word[v_spot])

        res = hPotential.intersection(vPotential)

        return res
    
    def _get_finished_words(self):
        finished_words = []
        visited_starts = set()

        def is_word_start(x, y, horizontal):
            if horizontal:
                return (x - 1, y) not in self.grid
            else:
                return (x, y - 1) not in self.grid

        for (x, y) in self.grid:
            # Horizontal
            if is_word_start(x, y, True) and (x, y, True) not in visited_starts:
                word = self._get_word_at(x, y, horizontal=True)
                if '_' not in word:
                    finished_words.append(word)
                    visited_starts.add((x, y, True))

            # Vertical
            if is_word_start(x, y, False) and (x, y, False) not in visited_starts:
                word = self._get_word_at(x, y, horizontal=False)
                if '_' not in word:
                    finished_words.append(word)
                    visited_starts.add((x, y, False))

        return finished_words


    def _search_with_regex(self, pattern):
        if '_' not in pattern:
            return {pattern} if pattern in self.words else set()
        elif pattern.count('_') == len(pattern):
            return {word for word in self.words if len(word) == len(pattern)}

        regex_pattern = pattern.replace('_', '.')
        regex = re.compile(f"^{regex_pattern}$")
        return {word for word in self.words if regex.match(word) and len(word) == len(pattern)}
    
    def _create_grid(self):
        grid = {}
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell == '_':
                    grid[(x, y)] = Cell(x, y)
        return grid
    
    def _get_word_at(self, x, y, horizontal=True):
        word = []
        start_x, start_y = self._get_word_start(x, y, horizontal)
        dx, dy = (1, 0) if horizontal else (0, 1)

        while (start_x, start_y) in self.grid:
            word.append(self.grid[(start_x, start_y)].char)
            start_x += dx
            start_y += dy

        return ''.join(word)

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
                        print(self.grid[(x, y)].char, end='  ')
                    else:
                        print('_', end='  ')
                else:
                    print('X', end='  ')
            print("\n")

    def _visualize_ent(self):
        for y in range(len(self.shape)):
            for x in range(len(self.shape[0])):
                if (x, y) in self.grid:
                    print(self.grid[(x, y)].ent, end='  ')
                else:
                    print('X', end='  ')
            print("\n")
                
    def _read_words(self, fileName):
        words = set()
        with open(f'engine/words/{fileName}', 'r') as f:
            for line in f:
                word = line.strip()
                if any(len(word) == len(self._get_word_at(x, y, horizontal=True)) or
                       len(word) == len(self._get_word_at(x, y, horizontal=False))
                       for x, y in self.grid):
                    words.add(word)
        return words
    
    def read_shapes_file(self, filename='engine/shapes.txt'):
        shapes = []
        current_shape = []

        with open(filename, 'r') as file:
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
