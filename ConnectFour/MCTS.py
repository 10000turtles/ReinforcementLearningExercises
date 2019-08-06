import math
import random
from Environment import ConnectFour
import pickle
import sys
import numpy as np


class Node:
  def __init__(self, parent, children = []):
    self.parent = parent
    self.children = children
    self.value = 0
    self.visits = 0
    self.boardState = 0

  def UCB1(self, parentVisits):
    if self.visits == 0:  # If the visits are 0 then UCB1 is infinite. Avoiding a divide by 0 error
      return sys.maxsize
    return self.value/self.visits + 2 * math.sqrt(math.log(self.parentVisits)/self.visits)  # UCB1 Formula


class MCTS:  # Monte Carlo Tree Search
  def __init__(self):
    self.nodes = [Node('Recursion')]

  def train(self, environment):
    current = self.nodes[0]
    while (len(current.children)) != 0:
      # current = self.nodes[current.children[np.argmax(j.UCB1(current.value) for j in [self.nodes[i] for i in current.children])]]
      childNodes = [self.nodes[i] for i in current.children]
      UCBValues = [j.UCB1(current.visits) for j in childNodes]
      argmaxValue = np.argmax(UCBValues)
      current = self.nodes[current.children[argmaxValue]]
    print(current)
    for i in env.possibleMoves():
      tempEnv = ConnectFour()
      current.children.append(i)

  def save(self, file):
    filehandler = open(file, "wb")
    pickle.dump(self, filehandler)

  def load(self, file):
    filehandler = open(file, "rb")
    placeholder = pickle.load(filehandler)
    self.copy(placeholder)


columns = 7
rows = 6
winNum = 4

env = ConnectFour(columns, rows, winNum)
bot = MCTS()
bot.save("Tree.obj")
