import random
import copy
import re
import sys

import numpy as np
import pandas as pd

from engine.cell import Cell, CHARS

MAX_SIZE = 5

class Board:

    def __init__(self, size, difficulty=0):
        if size > MAX_SIZE:
            print(f"Board size must be less than or equal to {MAX_SIZE}")
            sys.exit(1)

        self.size = size
        self.difficulty = difficulty
        self.filename = f"words_{['easy', 'medium', 'hard'][difficulty]}.txt"
        self.counter = 0

        # Create grid of cells
        self.grid = self._create_grid()

        # Store words from file in set
        self.words = self._read_words(self.filename)

        self.complete = False
        

    def genereate(self):
        print(self.grid)
        self.print_ent()
        while not self.complete:
            self._collapse()

        print(self.grid)
        print(self._get_finished_words())


    def _collapse(self):
        self.print_ent()
        print(self.grid)

        choice = self._pick()
        if choice:

            # print(f"Collapsing cell {choice.get_info()}")
            choice.observe()
            # print(f"Collapsed cell {choice.get_info()}")
        else:
            print("No cells to collapse")
            return None
        
        self._update()


    def _update(self):
        for cell in self.grid.flatten():
            if not cell.collapsed:
                cell.options = list(self._get_possible_chars(cell))
                cell.ent = len(cell.options)
                # print(f"\t\tCell {cell.options} {cell.ent} possible characters")
                if len(cell.options) == 0:
                    # print(f"\n\n\nCell {cell.cord} has no possible characters, Backtrack!")
                    # get second to last in history
                    self.counter += 1

                    if self.counter > 200:
                        # print("\n\n\nBacktrack limit reached, full reset")
                        self.grid = self._create_grid()
                        self.counter = 0
                    else:
                        vertical_cells = [cell for cell in self.grid[cell.x, :]]
                        horizontal_cells = [cell for cell in self.grid[:, cell.y]]

                        for cell in vertical_cells:
                            cell.reset()
                        for cell in horizontal_cells:
                            cell.reset()

                    # print(f"\tCounter: {self.counter}")
                    # print(f"\tGrid: {self.grid}")

                    self._collapse()


    def _pick(self):
        # get a list of cells that have cell.collapsed == False
        uncollapsed_list = [cell for row in self.grid for cell in row if not cell.collapsed]

        if len(uncollapsed_list) == 0:
            print("All cells have been collapsed")
            self.complete = True
            return None
        
        # get all cells with the least entropy
        least_entropy = min([cell.ent for cell in uncollapsed_list])
        least_entropy_cells = [cell for cell in uncollapsed_list if cell.ent == least_entropy]

        # return a random cell from the list of cells with the least entropy
        return random.choice(least_entropy_cells)


    def _get_possible_chars(self, cell):
        res, hPotential, vPotential = set(), set(), set()

        # Extract the vertical/horizontal word associated with a given cell
        vertical_word = ''.join(cell.char for cell in self.grid[cell.x, :])
        horizontal_word = ''.join(cell.char for cell in self.grid[:, cell.y])

        # Search the current words for matches in word list
        possible_horizontal = self._search_with_regex(horizontal_word)
        possible_vertical = self._search_with_regex(vertical_word)

        # print first 10 words in possible_horizontal and possible_vertical
        # print(f"\t\t\tHorizontal: {list(possible_horizontal)[:10]}")
        # print(f"\t\t\tVertical: {list(possible_vertical)[:10]}")

        # Skip if all words are possible
        if possible_horizontal == self.words and possible_vertical == self.words:
            return set(CHARS)
        
        if possible_horizontal == self.words: hPotential = set(CHARS)
        if possible_vertical == self.words: vPotential = set(CHARS)

        # Extract possible characters from the potential words
        if possible_horizontal and possible_horizontal != self.words:
            for word in possible_horizontal:
                hPotential.add(word[cell.x])

        if possible_vertical and possible_vertical != self.words:
            for word in possible_vertical:
                vPotential.add(word[cell.y])

        res = hPotential.intersection(vPotential)

        return res
    

    def _get_finished_words(self):
        if not self.complete:
            return None
        # return each row and column of the grid    
        rows = [''.join(cell.char for cell in row) for row in self.grid]
        columns = [''.join(cell.char for cell in column) for column in self.grid.T]

        return rows + columns


    def _search_with_regex(self, pattern):
        if '_' not in pattern:
            return {pattern}
        elif pattern.count('_') == len(pattern):
            return self.words

        regex_pattern = pattern.replace('_', '.')
        regex = re.compile(f"^{regex_pattern}$")
        return {word for word in self.words if regex.match(word)}

    
    def _create_grid(self):
        out = np.empty((self.size, self.size), dtype=object)

        for i in range(self.size):
            for j in range(self.size):
                out[i][j] = Cell(i, j)

        return out
    
    
    def _read_words(self, fileName):
        words = set()

        with open(f'engine/words/{fileName}', 'r') as f:
            for line in f:
                if (len(line.strip()) == self.size):
                    words.add(line.strip())
        return words

    def print_ent(self):
        for row in self.grid:
            for cell in row:
                print(cell.ent, end=' ')
            print()