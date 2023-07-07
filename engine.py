import random
import copy

class Board:

    def __init__(self, size, file):
        self.size = size
        self.x = size
        self.y = size
        self.file = file
        self.words = []
        self.board = [[Cell(j, i) for i in range(size)] for j in range(size)]

    def pick(self):

        # Create deep copy of board, convert to list, and remove collapsed cells
        grid = copy.deepcopy(self.board)
        cell_list =  [element for sublist in grid for element in sublist]
        #print(cell_list)
        uncollaped_list = list(filter(lambda x: x.collapsed == False, cell_list))
        #print(uncollaped_list)

        # Ensure there are more than 0 cells to choose from
        if (len(uncollaped_list) == 0):
            return None

        # Sort by entropy, create list of cells with least entropy
        uncollaped_list.sort(key=lambda x: x.ent)
        least = uncollaped_list[0].ent
        filtered_list = list(filter(lambda x: x.ent == least, uncollaped_list))
        

        # Return random cell from list
        rand_least = random.choice(filtered_list)
        return rand_least.cord

    def collapse(self):
        print('Collapsing')
        pick = self.pick()
        print('Picked: ' + str(pick))
        if (pick):
            self.board[pick[0]][pick[1]].observe()
        else:
            return 

        print('Full Update')
        self.update()

    
    def update(self):

        cell_list = self.get_list()

        for c in cell_list:
            if not c.collapsed:
                possible = self.get_possible_chars(c)

                if (len(possible) == 0):
                    print('ERROR, Need Backtracking')
                c.options = possible
                c.calc_ent()


    def get_possible_chars(self, c):
        if (c.collapsed):
            return [c.char]

        possible = []

        cur_words = self.build_words(c)
        xvalid = self.get_valid_words(cur_words[0])
        yvalid = self.get_valid_words(cur_words[1])

        if (len(xvalid) < len(yvalid)):
            possible = get_nth_characters(xvalid, c.y)
            for char in possible:
                for w in range(len(yvalid)):
                    if char == yvalid[w][c.x]:
                        break
                    if (w == len(yvalid) - 1):
                        possible.remove(char)
                    
        else:
            possible = get_nth_characters(yvalid, c.x)
            for char in possible:
                for w in range(len(xvalid)):
                    if char == xvalid[w][c.y]:
                        break
                    if (w == len(xvalid) - 1): 
                        possible.remove(char)
        
        return possible

    
    def build_words(self, c):
        down = right = ''
        for y in range(self.size):
            cell = self.board[c.x][y]
            if cell.collapsed:
                right += cell.char
            else:
                right += '*' 

        for x in range(self.size):
            cell = self.board[x][c.y]
            if cell.collapsed:
                down += cell.char
            else:
                down += '*'

        return [right, down]

    
    def get_valid_words(self, word):
        valid = []
        for w in self.words:
            for c in range(len(w)):
                if (word[c] != '*' and w[c] != word[c]):
                    break
                if (c == len(w) - 1):
                    valid.append(w)

        return valid
        
    
    def complete(self):
        cell_list = self.get_list()
        for c in cell_list:
            if (c.collapsed == False):
                return False
    
        return True


    def read(self):
        # Read in words from file
        with open(self.file, 'r') as f:
            for line in f:
                if (len(line.strip()) == self.x):
                    self.words.append(line.strip())

        random.shuffle(self.words)

    def cell_exist(self, x, y):
        if (x < 0 or x >= self.x or y < 0 or y >= self.y):
            return False

        for c in self.get_list():
            if (c.cord == (x, y)):
                return True
            
        return False

    def get_list(self):
        grid = copy.copy(self.board)
        cell_list =  [element for sublist in grid for element in sublist]
        return cell_list
    
    '''
    Debug Functions
    '''

    def manual_collapse(self, x, y, char):
        print('Collapsing')
        if (self.cell_exist(x, y)):
            self.board[x][y].manual_observe(char)
            print('Full Update')
            self.update()
        else:
            print('Error, cell does not exist')
            return

    def print_board(self):
        for i in range(self.y):
            for j in range(self.x):
                cell = self.board[i][j]
                print("{: <2s}".format(str(cell.char)), end=' ')
            print()

    def print_board_ent(self):
        for i in range(self.y):
            for j in range(self.x):
                cell = self.board[i][j]
                print("{: <2s}".format(str(cell.ent)), end=' ')
            print()
    
    def debug(self):
        self.print_board()
        print('\n')
        self.print_board_ent()
        print('\n')
        for i in range(self.y):
            for j in range(self.x):
                cell = self.board[i][j]
                print("{: <2s}".format(str(cell.cord)), end=' ')
            print()
        print('-----------')
        
        

class Cell:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.cord = (x, y)
        self.char = '0'
        self.ent = 26
        self.options = 'abcdefghijklmnopqrstuvwxyz'
        self.collapsed = False

    def __repr__(self):
        out = str(self.cord)
        if (self.collapsed):
            out += ' char: ' + self.char + ' ent: ' + str(self.ent)
        else:
            out += ' ent: ' + str(self.ent)
        
        return out

    
    def calc_ent(self):
        # Calculate potential states of cell
        self.ent = len(self.options)

    def update(self):
        if self.ent == 1:
            self.collapsed = True
            self.char = self.options[0]

    def observe(self):
        # Choose random choice based on neighboring cells
        try:
            print('Observing: ' + str(self.cord))
            self.collapsed = True
            self.char = self.options[random.randint(0, len(self.options) - 1)]
            self.options = [self.char]
            self.ent = 1
            self.update()
        except Exception as e:
            print('Error: ' + str(self.cord) + ' NEED BACKTRACK')
            print(e)
            return
        
    def manual_observe(self, char):
        self.collapsed = True
        self.char = char
        self.options = [self.char]
        self.ent = 1
        self.update()
        
def get_nth_characters(list, n):
    chars = []
    for s in list:
        if s[n] not in chars:
            chars.append(s[n])
    return chars
