import math
from ConnectFour import ConnectFour
import pickle
import sys
import numpy as np


class Node:
  def __init__(self, env, moveJustMade, turn):
    self.children = []
    self.value = 0
    self.moveJustMade = moveJustMade
    self.moveToMake = 0
    self.visits = 0
    self.boardState = env
    self.done = False
    self.turn = turn
    self.pruned = False
    self.parent = 0

  def __str__(self):
    return " Value: " + str(self.value) + " Children: " + str(len(self.children)) + " Visits: " + str(self.visits) + " State: " + (self.boardState) + " MoveToMake: " + str(self.moveToMake) + " MoveJustMade: " + str(self.moveJustMade) + " Done: " + str(self.done) + " Pruned: " + str(self.pruned)

  def UCB1(self, parentVisits):
    if self.visits == 0:
      if self.turn == 1:
        return -sys.maxsize
      else:
        return sys.maxsize
    if self.turn == 1:
      return 1/self.visits
    else:
      return self.value/self.visits + 2 * math.sqrt(math.log(parentVisits)/self.visits)  # UCB1 Formula

  def UCB2(self):
    if self.visits == 0:
      return self.value
    return self.value/self.visits

  def populate(self, env):
    for j, i in enumerate(env.possibleMoves()):
      tempEnv = ConnectFour(env.columns, env.rows, env.winNum, env.turn, env.returnBoard())
      tempEnv.makeMove(i)
      self.children.append(Node(tempEnv.encodeState(), i, tempEnv.turn))  # (tempEnv.isWinner() != 0 or tempEnv.isTie()),
      if tempEnv.isWinner() != 0:
        self.children[j].done = True
        self.children[j].value = -tempEnv.turn*10
        if self.children[j].value == 10:
          self.children = [self.children[j]]
          self.moveToMake = 0
          break
      if tempEnv.isTie():
        self.children[j].done = True
        self.children[j].value = 0
    for i in self.children:
      i.parent = self


class MCTS:  # Monte Carlo Tree Search
  def __init__(self, env, t):
    self.home = Node(env.encodeState(), "Recursion", env.turn)
    self.visitThreshold = t

  def printTree(current, spaces):
    print((" "*spaces) + str(current) + " UCB Values: " + str([j.UCB1(current.visits) for j in current.children]))
    for i in current.children:
      MCTS.printTree(i, spaces+1)

  def train(self, env, games):
    current = self.home
    if current.done:
      return 0
    env.reset()
    pathTaken = []
    while (len(current.children)) != 0:
      if current.pruned:
        current = current.children[0]
        pathTaken.append(0)
      else:
        newChildNodes = []
        newChildIndecies = []
        for i, node in enumerate(current.children):
          if not node.done:
            newChildNodes.append(node)
            newChildIndecies.append(i)
        if len(newChildNodes) == 0:
          current.done = True
          return 1
        if current.turn == -1:
          leastVisits = np.argmin([i.visits for i in newChildNodes])
          current = newChildNodes[leastVisits]
          pathTaken.append(newChildIndecies[leastVisits])
        else:
          UCBValues = [j.UCB1(current.visits) for j in newChildNodes]
          if current.turn == 1:
            argmaxValue = np.argmax(UCBValues)
          else:
            argmaxValue = np.argmin(UCBValues)
          if False:  # current.visits > self.visitThreshold:
            UCBValues = [j.UCB1(current.visits) for j in current.children]
            argmaxValue = np.argmax(UCBValues)
            current.children = [current.children[argmaxValue]]
            current.moveToMake = 0
            current.pruned = True
            current = current.children[0]
            pathTaken.append(0)
          else:
            current = newChildNodes[argmaxValue]
            pathTaken.append(newChildIndecies[argmaxValue])

    env.decodeState(current.boardState)
    current.populate(env)
    if current.moveJustMade != "Recursion":
      if len(current.parent.children) == 1 and current.done:
        current.parent.done = True
        return 5
    availableNodes = True
    for j, i in enumerate(current.children):
      if not current.children[j].done:
        current = i
        availableNodes = False
        pathTaken.append(j)
        break
    if availableNodes:
      current.done = True
      # self.updateTree(self.home, current.value, pathTaken, 0)
      return 2

    env.decodeState(current.boardState)
    totalReward = 0
    for i in range(games):
      tempEnv = ConnectFour(env.columns, env.rows, env.winNum, env.turn, env.returnBoard())
      if tempEnv.isTie() or (tempEnv.isWinner() != 0):
        totalReward = games*(-10)*tempEnv.turn
        break
      totalReward += self.playRandomGame(tempEnv)
    averageReward = totalReward/games
    self.updateTree(self.home, averageReward, pathTaken, 0)
    return 3

  def updateTree(self, current, averageReward, pathTaken, index):

    current.value += averageReward
    current.visits += 1

    if index < len(pathTaken):
      self.updateTree(current.children[pathTaken[index]], averageReward, pathTaken, index+1)

    if current.turn == 1 and len(current.children) != 0:
      current.moveToMake = np.argmax([i.UCB2() for i in current.children])
    elif current.turn == -1 and len(current.children) != 0:
      current.moveToMake = np.argmin([i.UCB2() for i in current.children])

  def playRandomGame(self, env):
    reward = 0
    done = False
    while(not done):
      done, reward = env.makeRandomMove()
    return reward

  def playGameWithPlayer(self, env):
    env.reset()
    current = self.home
    reward = 0
    done = False
    randomBotMoves = False
    ifPlayerTurn = False
    while(not done):
      if len(current.children) == 0:
        randomBotMoves = True
        print("I am now making random moves")
      if ifPlayerTurn:

        move = input("Make ur Move (0-6): ")
        done, reward = env.makeMove(int(move))
        if not randomBotMoves:
          print(str(current) + '\n')
          for i in current.children:
            print(i)
          current = current.children[int(move)]
      else:

        if randomBotMoves:
          done, reward = env.makeRandomMove()
        else:
          print(str(current) + '\n')
          for i in current.children:
            print(i)
          current = current.children[current.moveToMake]
          done, reward = env.makeMove(current.moveJustMade)

      env.printBoard()
      ifPlayerTurn = not ifPlayerTurn

  def save(self, file):
    filehandler = open(file, "wb")
    pickle.dump(self, filehandler)

  def load(self, file):
    filehandler = open(file, "rb")
    placeholder = pickle.load(filehandler)
    self.copy(placeholder)

  def copy(self, placeholder):
    self.nodes = placeholder.nodes
