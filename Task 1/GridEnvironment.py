# Hello

# Belman EQ: Value(move,state) = Max(Reward + WeightedSum(All possible outcomes))


class GridEnvironment:
  RewardKey = {"_": 0, "W": 1, "L": -10, "0": 0}
  MoveKey = ["R", "U", "L", "D", "■"]
  DirectionKey = [(0, 1), (-1, 0), (0, -1), (1, 0)]

  def __init__(self, envData, agentPos, obeyProbs, gamma):
    self.board = envData  # envData is a 2-D array of characters/strings. _ = empty, 0 = wall, W = winning spot, L = losing spot.
    self.boardValues = [[0 for i in envData[0]]for j in envData]  # initalizing a matrix the size of envData with all 0's
    self.boardMoves = [[4 for i in envData[0]]for j in envData]  # Same thing
    self.position = agentPos  # agentPos is a tuple of 2 integers representing where the player starts.
    self.obeyProbs = obeyProbs  # obeyProbs is a list of 4 probabilities that add to 1 and explain the probability of the agent obeying. index 0 = Obey, index 1 = left, index 2 = back, index 3 = right.
    self.gamma = gamma

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
