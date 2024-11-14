# import re
# import random

# from engine.cell import Cell, CHARS

# DEBUG = False

# def print_debug(*args, **kwargs):
#     if DEBUG:
#         print(*args, **kwargs)

# class Word:
#     def __init__(self, origin, word=None):
#         self.origin = origin
#         self.length = 1 if not word else len(word)
#         self.word = ('_' * self.length) if not word else word
#         self.horizontal = True

#     def add_char(self, char, index):
#         self.length += 1
#         self.word += "_"

#     def __repr__(self):
#         return f"Word(origin={self.origin}, word='{self.word}', length={self.length}, horizontal={self.horizontal})"

# class Board:

#     def __init__(self, difficulty=0, shape=None):
#         self.difficulty = difficulty
#         self.filename = f"words_{['easy', 'medium', 'hard'][difficulty]}.txt"
#         self.counter = 0
#         self.complete = False
#         self.shapes = self.read_shapes_file()

#         self.shape = random.choice(self.shapes) if not shape else shape
#         self.grid = self._create_grid()
#         self._setup_grid()

#         self.words = self._read_words(self.filename)

#     def _create_grid(self):
#         grid = {}
#         for y, row in enumerate(self.shape):
#             for x, cell in enumerate(row):
#                 if cell == '_':
#                     grid[(x, y)] = "_"
#         return grid
    
#     def _setup_grid(self):
#         for i in range(len(self.shape)):
            

#     def read_shapes_file(self, filename='engine/shapes.txt'):
#         shapes = []
#         current_shape = []

#         with open(filename, 'r') as file:
#             for line in file:
#                 line = line.strip()
#                 if line:
#                     current_shape.append(line)
#                 else:
#                     if current_shape:
#                         shapes.append(current_shape)
#                         current_shape = []
            
#             if current_shape:
#                 shapes.append(current_shape)

#         return shapes
