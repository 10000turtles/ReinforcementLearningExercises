from GridEnvironment import GridEnvironment
import random
def mean(ar):
  return sum(ar)/len(ar)
class GridWorldBot:
  MoveKey = ["R", "U", "L", "D"]

  def __init__(self, board, gamma, epsilon):
    self.policyTable = {}
    for i in range(len(board.board)):
      for j in range(len(board.board[0])):
        if board.board[i][j] == "_":
          randMove = random.randint(0, 3)
          self.policyTable.update({str(i)+str(j): randMove})
    self.QTable = {}
    for i in self.policyTable:
      for j in range(4):
        self.QTable.update({i+str(j): 0})
    self.gamma = gamma
    self.epsilon = epsilon

  def move(self, board):
    state = str(board.position[0])+str(board.position[1])
    moveValues = [self.QTable[state+str(i)]for i in range(4)]
    moveChoice = moveValues.index(max(moveValues))
    if random.random() > (1-self.epsilon):
      return moveChoice
    else:
      return random.randint(0, 3)

  def playGame(self, board):
    StatesActionsRewards = []
    while board.terminalState == 0:
      action = self.move(board)
      state = board.position
      board.move(action)
      StatesActionsRewards += [[state, action, 0]]
    StatesActionsRewards.reverse()
    StatesActionsRewards[0][2] = board.terminalState
    for i in range(1, len(StatesActionsRewards), 1):
      StatesActionsRewards[i][2] = StatesActionsRewards[i-1][2]*self.gamma
    StatesActionsRewards.reverse()
    board.reset()
    return StatesActionsRewards

  def monteCarloTraining(self, board):
    StatesActionsRewards = self.playGame(board)
    returns = []
    returnValues = []
    for s, a, r in StatesActionsRewards:
      try:
        spot = returns.index(str(s[0])+str(s[1])+str(a))
        returns = returns[0:spot+1]
        returnValues = returnValues[0:spot+1]
      except ValueError:
        returns.append(str(s[0])+str(s[1])+str(a))
        returnValues.append(r)
        self.QTable[returns[-1]] = mean(returnValues)
    for state in self.policyTable:
      moveValues = [self.QTable[state+str(i)]for i in range(4)]
      moveChoice = moveValues.index(max(moveValues))
      self.policyTable[state] = moveChoice
  def printPolicyTable(self,board):
    print("-"*(len(board.board[0])*2+1))
    for i in range(len(board.board)):
      a = "|"
      for j in range(len(board.board[0])):
        try:
          move = self.policyTable[str(i)+str(j)]
          a += GridWorldBot.MoveKey[move]+"|"
        except:
          a += "■|"
      print(a)
      print("-"*(len(board.board[0])*2+1))
