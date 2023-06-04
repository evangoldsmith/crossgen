from engine import Board

thing = Board(3, 'words.txt')
thing.read()
thing.debug()

for i in range(9):
    print('Iteration: ' + str(i+1))
    thing.collapse()
    thing.debug()