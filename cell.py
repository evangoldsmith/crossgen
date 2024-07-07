import random

CHARS ='abcdefghijklmnopqrstuvwxyz'

class Cell:

    # X and Y position -> required parameters
    def __init__(self, x, y, char='_', options=CHARS, ent=26, collapsed=False):
        self.x, self.y = x, y
        self.cord = (x, y)
        self.char = char
        self.ent = ent
        self.options = options
        self.collapsed = collapsed


    def __repr__(self):
        return f"{self.char}"
    

    def observe(self):
        self.collapsed = True
        self.ent = 1
        self.char = random.choice(self.options)
        self.options = [self.char]


    def reset(self):
        self.collapsed = False
        self.char = '_'
        self.ent = 26
        self.options = list(CHARS)


    def manual_observe(self, char):
        self.collapsed = True
        self.char = char
        self.options = [char]
        self.ent = 1


    def calc_ent(self):
        self.ent = len(self.options)
        if self.ent == 1:
            self.collapsed = True
            self.char = self.options[0]
        

    def get_info(self):
        return f"Cell(cord={self.cord}, char='{self.char}', ent={self.ent}, options='{self.options}', collapsed={self.collapsed})"
    