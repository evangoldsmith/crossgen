from engine import Board

thing = Board(4, 'words.txt')
print(thing.grid)
thing.print_ent()

while not thing.complete:
    thing.collapse()

print(thing.grid)