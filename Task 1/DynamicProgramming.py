from GridEnvironment import GridEnvironment


def updateValues(board):
  def calcValue(board, p):  # p is a tuple representing position. Returns the maxValue, move
    possibleMoves = [(p[0], p[1]+1), (p[0]-1, p[1]), (p[0], p[1]-1), (p[0]+1, p[1])]
    moveValues = [0]*4
    for j, i in enumerate(possibleMoves):
      reward = sum([GridEnvironment.RewardKey[board.board[possibleMoves[(j+k) % 4][0]][possibleMoves[(j+k) % 4][1]]]*board.obeyProbs[k] for k in range(4)])
      outcomes = board.gamma * sum([board.boardValues[possibleMoves[(j+k) % 4][0]][possibleMoves[(j+k) % 4][1]]*board.obeyProbs[k] for k in range(4)])
      moveValues[j] = reward + outcomes
    maxValue = max(moveValues)
    return maxValue, moveValues.index(maxValue)
  valuesTemp = [[0]*len(board.boardValues[0]) for i in range(len(board.boardValues))]
  movesTemp = [[4]*len(board.boardValues[0]) for i in range(len(board.boardValues))]
  for i in range(len(valuesTemp)):
    for j in range(len(valuesTemp[0])):
      if board.board[i][j] == "_":
        valuesTemp[i][j], movesTemp[i][j] = calcValue(board, (i, j))
  board.boardValues = valuesTemp
  board.boardMoves = movesTemp


data = [["0", "0", "0", "0", "0", "0"],
        ["0", "_", "_", "_", "L", "0"],
        ["0", "_", "0", "_", "L", "0"],
        ["0", "_", "L", "_", "W", "0"],
        ["0", "0", "0", "0", "0", "0"]]
iterations = 10000
board = GridEnvironment(data, (4, 1), [.8, .1, 0, .1], .9)

for i in range(iterations):
  updateValues(board)

board.printBoard()
board.printMoves()
board.printValues()
