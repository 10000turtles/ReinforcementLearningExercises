import math
import random
from ConnectFour import ConnectFour
import pickle
import sys
import numpy as np


class Node:
  def __init__(self, parent, state, index, env, children = []):
    self.parent = parent
    self.children = children
    self.visitValue = 0
    self.moveValue = 0
    self.visits = 0
    self.index = index
    self.boardState = state
    tempEnv = ConnectFour(env.columns, env.rows, env.winNum, env.turn, env.returnBoard())
    w = tempEnv.isWinner()
    self.done = (w != 0 or tempEnv.isTie())
    self.turn = env.turn

  def __str__(self):
    return "Node " + str(self.index) + " Children: " + str(self.children) + " Parent: " + str(self.parent) + " Value: " + str(self.visitValue) + " Visits: " + str(self.visits) + " State: " + self.boardState

  def UCB1(self, parentVisits):
    if self.visits == 0:  # If the visits are 0 then UCB1 is infinite. Avoiding a divide by 0 error
      return sys.maxsize
    return self.visitValue/self.visits + 2 * math.sqrt(math.log(parentVisits)/self.visits)  # UCB1 Formula


class MCTS:  # Monte Carlo Tree Search
  def __init__(self, env):
    self.nodes = [Node("Recursion", env.encodeState(), 0, env)]

  def __str__(self):
    tempStr = ""
    for i in self.nodes:
      tempStr += str(i)+"\n"
    return tempStr

  def train(self, env, games):
    current = self.nodes[0]
    env.reset()
    while (len(current.children)) != 0:
      # current = self.nodes[current.children[np.argmax(j.UCB1(current.value) for j in [self.nodes[i] for i in current.children])]]
      childNodes = [self.nodes[i] for i in current.children]
      for i, node in enumerate(childNodes):
        if node.done:
          childNodes.remove(i)
      UCBValues = [j.UCB1(current.visits) for j in childNodes]
      argmaxValue = np.argmax(UCBValues)
      current = self.nodes[current.children[argmaxValue]]
    env.decodeState(current.boardState)
    for i in env.possibleMoves():
      tempEnv = ConnectFour(env.columns, env.rows, env.winNum, env.turn, env.returnBoard())
      tempEnv.makeMove(i)
      self.nodes.append(Node(current.index, tempEnv.encodeState(), len(self.nodes), tempEnv, []))
      current.children.append(len(self.nodes)-1)

    current = self.nodes[current.children[0]]
    totalReward = 0
    for i in range(games):
      tempEnv = ConnectFour(env.columns, env.rows, env.winNum, env.turn, env.returnBoard())
      totalReward += self.playRandomGame(tempEnv)
    averageReward = totalReward/games
    self.updateTree(current, averageReward)

  def updateTree(self, current, averageReward):
    if current.turn == 1 and len(current.children) != 0:
      current.moveValue = max([self.nodes[i].moveValue for i in current.children])
    elif current.turn == -1 and len(current.children) != 0:
      current.moveValue = min([self.nodes[i].moveValue for i in current.children])
    if current.parent == "Recursion":
      current.visitValue += averageReward
      current.visits += 1
    else:
      self.updateTree(self.nodes[current.parent], averageReward)
      current.visitValue += averageReward
      current.visits += 1

  def playRandomGame(self, env):
    reward = 0
    done = False
    while(not done):
      done, reward = env.makeRandomMove()
    return reward

  def save(self, file):
    filehandler = open(file, "wb")
    pickle.dump(self, filehandler)

  def load(self, file):
    filehandler = open(file, "rb")
    placeholder = pickle.load(filehandler)
    self.copy(placeholder)
