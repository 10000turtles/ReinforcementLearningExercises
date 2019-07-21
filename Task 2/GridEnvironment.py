# Hello

# Belman EQ: Value(move,state) = Max(Reward + WeightedSum(All possible outcomes))


class GridEnvironment:
  RewardKey = {"_": 0, "W": 1, "L": -10, "0": 0}
  MoveKey = ["R", "U", "L", "D", "■"]
  DirectionKey = [(0, 1), (-1, 0), (0, -1), (1, 0)]

  def __init__(self, envData, agentStartPos, obeyProbs, gamma):
    self.board = envData  # envData is a 2-D array of characters/strings. _ = empty, 0 = wall, W = winning spot, L = losing spot.
    self.startPos = agentStartPos  # agentStartPos is a tuple of 2 integers representing where the player starts.
    self.position = agentStartPos
    self.obeyProbs = obeyProbs  # obeyProbs is a list of 4 probabilities that add to 1 and explain the probability of the agent obeying. index 0 = Obey, index 1 = left, index 2 = back, index 3 = right.
    self.gamma = gamma
    self.terminalState = 0

  def move(self, direction):  # direction is 0-3. 0 is right, 1 is up, 2 is left, 3 is down.
    newSpace = (self.position[0]+GridEnvironment.DirectionKey[direction][0], self.position[1]+GridEnvironment.DirectionKey[direction][1])
    if self.board[newSpace[0]][newSpace[1]] != "0":
      self.position = newSpace
    if self.board[self.position[0]][self.position[1]] == "W":
      self.terminalState = 1
    if self.board[self.position[0]][self.position[1]] == "L":
      self.terminalState = -1
  def reset(self):
    self.position = self.startPos
    self.terminalState = 0
  def printBoard(self):
    for i in self.board:
      print("-"*(len(self.board[0])*2+1))
      a = "|"
      for j in i:
        a += j + "|"
      print(a)
    print("-"*(len(self.board[0])*2+1))
