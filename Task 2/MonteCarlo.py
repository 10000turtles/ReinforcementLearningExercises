from GridEnvironment import GridEnvironment
import random


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
    print(StatesActionsRewards)


data = [["0", "0", "0", "0", "0", "0"],
        ["0", "_", "_", "_", "W", "0"],
        ["0", "_", "0", "_", "L", "0"],
        ["0", "_", "_", "_", "_", "0"],
        ["0", "0", "0", "0", "0", "0"]]


iterations = 10000
board = GridEnvironment(data, (3, 1), [.8, .1, 0, .1], .9)
bot = GridWorldBot(board, 0.99, 0.99)
bot.playGame(board)
