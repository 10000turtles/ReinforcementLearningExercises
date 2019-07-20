from GridEnvironment import GridEnvironment
import random


def playGame(board, bot):
  while board.terminalState == 0:
    action = bot.move(board)
    state = board.board
    board.move(action)


class GridWorldBot:
  MoveKey = ["R", "U", "L", "D"]

  def __init__(self, board):
    self.policyTable = {}
    for i in board.board:
      for j in i:
        if j == "_":
          randMove = random.randint(0, 3)
          self.policyTable.update({(i, j): GridWorldBot.MoveKey[randMove]})
    self.QTable = {}

  def move(self, board):

  def


data = [["0", "0", "0", "0", "0", "0"],
        ["0", "_", "_", "_", "L", "0"],
        ["0", "_", "0", "_", "L", "0"],
        ["0", "_", "L", "_", "W", "0"],
        ["0", "0", "0", "0", "0", "0"]]

board = GridEnvironment(data, (4, 1), [.8, .1, 0, .1], .9)

iterations = 10000
