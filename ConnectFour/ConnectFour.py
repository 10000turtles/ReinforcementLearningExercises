import random
from colorama import Fore, Style


class ConnectFour:
  def __init__(self, col, row, winNum, turn, board = []):
    if board == []:
      self.board = [[0 for j in range(row)]for i in range(col)]
    else:
      self.board = board
    self.turn = turn
    self.winNum = winNum
    self.columns = col
    self.rows = row

  def reset(self):
    self.__init__(self.columns, self.rows, self.winNum, self.turn)

  def makeMove(self, move):
    i = 0
    while (i < (self.rows) and self.board[move][i] == 0):
      i += 1
    self.board[move][i-1] = self.turn
    self.turn = -self.turn
    w = self.isWinner()
    return (w != 0 or self.isTie(), w*10)

  def possibleMoves(self):
    moves = []
    for i in range(self.columns):
      if self.board[i][0] == 0:
        moves.append(i)
    return moves

  def makeRandomMove(self):
    possibleMoves = self.possibleMoves()
    return self.makeMove(possibleMoves[random.randint(0, len(possibleMoves)-1)])

  def encodeState(self):
    encode = ""
    for i in range(self.columns):
      for j in range(self.rows):
        if self.board[i][j] == -1:
          encode += "2"
        else:
          encode += str(self.board[i][j])
    if self.turn == -1:
      encode += "2"
    else:
      encode += str(self.turn)
    return encode

  def decodeState(self, state):
    for i in range(self.columns):
      for j in range(self.rows):
        self.board[i][j] = int(state[i*self.rows+j])
        if self.board[i][j] == 2:
          self.board[i][j] = -1
    self.turn = int(state[self.columns*self.rows])
    if self.turn == 2:
      self.turn = -1

  def returnBoard(self):
    temp = [[0 for j in range(self.rows)]for i in range(self.columns)]
    for i in range(len(temp)):
      for j in range(len(temp[i])):
        temp[i][j] = self.board[i][j]
    return temp

  def isTie(self):
    for i in range(len(self.board)):
      if self.board[i][0] == 0:
        return False
    return True

  def isWinner(self):
    for i in range(self.columns - self.winNum + 1):
      for j in range(self.rows - self.winNum + 1):
        temp = (self.board[i][j] != 0)
        k = 0
        while(temp):
          k += 1
          temp = temp and (self.board[i][j] == self.board[i+k][j])
          if k == self.winNum-1:
            break
        if temp:
          return self.board[i][j]

        temp = (self.board[i][j] != 0)
        k = 0
        while(temp):
          k += 1
          temp = temp and (self.board[i][j] == self.board[i][j+k])
          if k == self.winNum-1:
            break
        if temp:
          return self.board[i][j]

        temp = (self.board[i][j] != 0)
        k = 0
        while(temp):
          k += 1
          temp = temp and (self.board[i][j] == self.board[i+k][j+k])
          if k == self.winNum-1:
            break
        if temp:
          return self.board[i][j]

        temp = (self.board[i][j+3] != 0)
        k = 0
        while(temp):
          k += 1
          temp = temp and (self.board[i][j+3] == self.board[i+k][j+3-k])
          if k == self.winNum-1:
            break
        if temp:
          return self.board[i][j]
    return 0

  def printBoard(self):
    RenderKey = [Fore.BLUE + "■" + Style.RESET_ALL, " ", Fore.RED + "■" + Style.RESET_ALL]
    for i in range(len(self.board)):
      print("-"*(len(self.board[0])*2+1))
      a = "|"
      for j in range(len(self.board[i])):
        a += RenderKey[self.board[i][j]+1] + "|"
      print(a)
    print("-"*(len(self.board[0])*2+1))
    return
