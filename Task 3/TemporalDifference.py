
import random
import numpy as np


class TaxiBot:
  numMoves = 6
  numStates = 500
  maxSteps = 50

  def __init__(self, gamma, learningRate, epsilon):
    self.QTable = [[0 for i in range(TaxiBot.numMoves)]for j in range(TaxiBot.numStates)]
    self.PTable = [random.randint(0, 5)for j in range(TaxiBot.numStates)]
    self.gamma = gamma
    self.learningRate = learningRate
    self.epsilon = epsilon
    self.epsilonStart = epsilon

  def trainingGame(self, environment):
    self.epsilon = self.epsilonStart
    oldState = environment.reset()

    for i in range(TaxiBot.maxSteps):
      action = self.move(oldState, True)
      newState, reward, done, info = environment.step(action)

      if oldState == newState:
        reward = -10

      self.TempDiffQTable(oldState, newState, action, reward)

      oldState = newState
      self.epsilon += (1-self.epsilonStart)/TaxiBot.maxSteps
      if done:
        break
    self.updatePTable()

  def move(self, state, useEpsilon):
    if random.random() > self.epsilon or (not useEpsilon):
      return self.PTable[state]
    else:
      return random.randint(0, 5)

  def updatePTable(self):
    for i in range(TaxiBot.numStates):
      self.PTable[i] = np.argmax(self.QTable[i])

  def TempDiffQTable(self, oldState, newState, action, reward):
    self.QTable[oldState][action] = (1-self.learningRate) * self.QTable[oldState][action] + self.learningRate * (reward + self.gamma * max(self.QTable[newState]))
