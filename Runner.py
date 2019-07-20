from GridEnvironment import GridEnvironment

data = [["0", "0", "0", "0", "0", "0"],
        ["0", "_", "_", "_", "L", "0"],
        ["0", "_", "0", "_", "L", "0"],
        ["0", "_", "L", "_", "W", "0"],
        ["0", "0", "0", "0", "0", "0"]]
iterations = 10000
board = GridEnvironment(data, (4, 1), [.8, .1, 0, .1], .9)

for i in range(iterations):
  board.updateValues()

board.printBoard()
board.printMoves()
board.printValues()
