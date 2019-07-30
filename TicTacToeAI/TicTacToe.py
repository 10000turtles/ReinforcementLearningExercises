

class TicTacToe:
  WinningPositions = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]

  def __init__(self):
    self.board = [0 for i in range(9)]
    self.done = False
    self.turn = 1  # X is 1, O is -1

  def encode(self):
    i = (1-self.turn)/2
    i *= 3
    for j in range(9):
      i += int(self.board[j]*((3*self.board[j]-1)/2))
      i *= 3
    return int(i/3)

  def decode(self, i):
    board = []
    for j in range(9, 1, -1):
      board.append(i % 3)
      i = i // 3
    board.append(i % 3)
    i = i // 3
    return (list(reversed(board)), 1-i*2)

  def reset(self):
    self.__init__()
    return self.encode()

  def step(self, action):  # action is an integer representing the move
    if (self.board[action] == 0):
      self.board[action] = self.turn
      if(self.isDone()):
        reward = 100*(self.turn)
        return(self.encode(), reward, True, self.turn)
      return(self.encode(), 0, False, 0)
    else:
      return (self.encode(), -10*(self.turn), True, -self.turn)

  def isDone(self):
    done = False
    wp = TicTacToe.WinningPositions
    for i in range(8):
      if (self.board[wp[i][0]] == self.board[wp[i][1]]) and (self.board[wp[i][1]] == self.board[wp[i][2]]) and (self.board[wp[i][0]] != 0):
        done = True
    return done

  def render(self):
    RenderKey = ["O", "_", "X"]
    for i in range(3):
      print("-"*(7))
      a = "|"
      for j in range(3):
        a += RenderKey[self.board[i*3+j]+1] + "|"
      print(a)
    print("-"*(7))
    return
