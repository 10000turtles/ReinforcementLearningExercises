from NNL import NNL
import numpy as np
import math
import random


class FrozenLakeBot:

  numMoves = 4
  maxSteps = 50

  def __init__(self, gamma, epsilon, learningRate, layerSizes, gridSize):
    self.QNetwork = NNL(layerSizes, learningRate)
    self.gridSize = gridSize
    self.targetNetwork = NNL(layerSizes, learningRate)
    self.gamma = gamma
    self.learningRate = learningRate
    self.epsilon = epsilon
    self.epsilonStart = epsilon

  def trainingGame(self, environment, isPrint):
    self.epsilon = self.epsilonStart
    didWin = False
    oldState = environment.reset()
    for i in range(FrozenLakeBot.maxSteps):
      action = self.move(oldState, environment)
      newState, reward, done, info = environment.step(action)
      if done and reward == 0:
        reward = -10
      if (not done) and reward == 0:
        reward = -1
      if done and reward == 1:
        reward = 100
      self.UpdateQNetwork(oldState, action, reward, newState, environment)

      oldState = newState
      self.epsilon += (1-self.epsilonStart)/FrozenLakeBot.maxSteps
      if done:
        if reward == 1:
          didWin = True
        break
      if isPrint:
        environment.render()
    self.copy()
    return didWin

  def move(self, pos, environment):

    if random.random() < self.gamma:
      inputs = np.matrix([self.oneHotState(environment, pos)]).T
      return np.argmax(self.QNetwork.ff(inputs))
    else:
      return random.randint(0, FrozenLakeBot.numMoves)

  def UpdateQNetwork(self, oldState, action, reward, newState, env):
    inputs = np.matrix([self.oneHotState(env, newState)]).T
    target = max(self.targetNetwork.ff(inputs).T.tolist()[0])
    self.QNetwork.train([self.oneHotState(env, oldState)], [[0]*action+[reward+target]+[0]*(FrozenLakeBot.numMoves-action-1)], 1)

  def oneHotState(self, env, pos):
    def bianary(i):
      ar = []
      for j in range(math.ceil(math.log2(self.gridSize))):
        ar.append(i % 2)
        i = i//2
      return list(reversed(ar))

    def decode(i):
      xPos = i % 4
      i = i // 4
      yPos = i
      return (xPos, yPos)

    pos = decode(pos)
    oneHotArray = []
    for i in env.desc:
      for j in i:
        if j == b'S':
          oneHotArray.append(0)
        if j == b'H':
          oneHotArray.append(-1)
        if j == b'F':
          oneHotArray.append(0)
        if j == b'G':
          oneHotArray.append(1)
    return oneHotArray + bianary(pos[0]) + bianary(pos[1])

  def copy(self):
    for i in range(len(self.QNetwork.weights)):
      for j in range(len(self.QNetwork.weights[i])):
        for k in range(len(self.QNetwork.weights[i][j])):
          self.targetNetwork.weights[i][j][k] = self.QNetwork.weights[i][j][k]
