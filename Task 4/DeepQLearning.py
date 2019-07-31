from NNL import NNL
import numpy as np


class FrozenLakeBot:

  numMoves = 4
  maxSteps = 50

  def __init__(self, gamma, epsilon, learningRate, layerSizes):
    self.QTable = NNL(learningRate, layerSizes)
    self.gamma = gamma
    self.learningRate = learningRate
    self.epsilon = epsilon
    self.epsilonStart = epsilon

  def trainingGame(self, environment):
    self.epsilon = self.epsilonStart

    oldState = environment.reset()

    for i in range(FrozenLakeBot.maxSteps):
      action = self.move(oldState, True)
      newState, reward, done, info = environment.step(action)

      if oldState == newState:
        reward = -10

      self.TempDiffQTable(oldState, newState, action, reward)

      oldState = newState
      self.epsilon += (1-self.epsilonStart)/FrozenLakeBot.maxSteps
      if done:
        break
    self.updatePTable()

  def move(self, state):
    return

  def updatePTable(self):
    for i in range(FrozenLakeBot.numStates):
      self.PTable[i] = np.argmax(self.QTable[i])

  def TempDiffQTable(self, oldState, newState, action, reward):
    self.QTable[oldState][action] = (1-self.learningRate) * self.QTable[oldState][action] + self.learningRate * (reward + self.gamma * max(self.QTable[newState]))
