# Hello

# Belman EQ: Value(move,state) = Max(Reward + WeightedSum(All possible outcomes))


class GridEnvironment:
  RewardKey = {"_": 0, "W": 1, "L": -10, "0": 0}
  MoveKey = ["R", "U", "L", "D", "■"]

  def __init__(self, envData, agentPos, obeyProbs, gamma):
    self.board = envData  # envData is a 2-D array of characters/strings. _ = empty, 0 = wall, W = winning spot, L = losing spot.
    self.boardValues = [[0 for i in envData[0]]for j in envData]  # initalizing a matrix the size of envData with all 0's
    self.boardMoves = [[4 for i in envData[0]]for j in envData]  # Same thing
    self.position = agentPos  # agentPos is a tuple of 2 integers representing where the player starts.
    self.obeyProbs = obeyProbs  # obeyProbs is a list of 4 probabilities that add to 1 and explain the probability of the agent obeying. index 0 = Obey, index 1 = left, index 2 = back, index 3 = right.
    self.gamma = gamma

  def move(self, direction):  # direction is 0-3. 0 is right, 1 is up, 2 is left, 3 is down.
    return

  def calcValue(self, p):  # p is a tuple representing position. Returns the maxValue, move
    possibleMoves = [(p[0], p[1]+1), (p[0]-1, p[1]), (p[0], p[1]-1), (p[0]+1, p[1])]
    moveValues = [0]*4
    for j, i in enumerate(possibleMoves):
      reward = sum([GridEnvironment.RewardKey[self.board[possibleMoves[(j+k) % 4][0]][possibleMoves[(j+k) % 4][1]]]*self.obeyProbs[k] for k in range(4)])
      outcomes = self.gamma * sum([self.boardValues[possibleMoves[(j+k) % 4][0]][possibleMoves[(j+k) % 4][1]]*self.obeyProbs[k] for k in range(4)])
      moveValues[j] = reward + outcomes
    maxValue = max(moveValues)
    return maxValue, moveValues.index(maxValue)

  def updateValues(self):
    valuesTemp = [[0]*len(self.boardValues[0]) for i in range(len(self.boardValues))]
    movesTemp = [[4]*len(self.boardValues[0]) for i in range(len(self.boardValues))]
    for i in range(len(valuesTemp)):
      for j in range(len(valuesTemp[0])):
        if self.board[i][j] == "_":
          valuesTemp[i][j], movesTemp[i][j] = self.calcValue((i, j))
    self.boardValues = valuesTemp
    self.boardMoves = movesTemp

  def printBoard(self):
    for i in self.board:
      print("-"*(len(self.board[0])*2+1))
      a = "|"
      for j in i:
        a += j + "|"
      print(a)
    print("-"*(len(self.board[0])*2+1))

  def printValues(self):
    for i in self.boardValues:
      print("-"*(len(self.board[0])*2+1))
      a = "|"
      for j in i:
        a += str(j) + "|"
      print(a)
    print("-"*(len(self.board[0])*2+1))

  def printMoves(self):
    for i in self.boardMoves:
      print("-"*(len(self.board[0])*2+1))
      a = "|"
      for j in i:
        a += GridEnvironment.MoveKey[j] + "|"
      print(a)
    print("-"*(len(self.board[0])*2+1))
