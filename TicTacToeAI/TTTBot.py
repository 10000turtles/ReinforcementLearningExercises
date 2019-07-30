
import random
import numpy as np


class TTTBot:
  numMoves = 9
  numStates = (3**9)*2
  maxSteps = 9

  def __init__(self, gamma, learningRate, epsilon):
    self.QTable = [[0 for i in range(TTTBot.numMoves)]for j in range(TTTBot.numStates)]
    self.PTable = [random.randint(0, TTTBot.numMoves-1)for j in range(TTTBot.numStates)]
    self.gamma = gamma
    self.learningRate = learningRate
    self.epsilon = epsilon
    self.epsilonStart = epsilon

  def trainingGame(self, environment):
    self.epsilon = self.epsilonStart
    oldState = environment.reset()
    for i in range(TTTBot.maxSteps):
      action = self.move(oldState, True)
      newState, reward, done, whoWon = environment.step(action)

      self.TempDiffQTable(oldState, newState, action, reward, environment.turn)
      self.updatePTable(oldState, environment.turn)
      oldState = newState
      # print(environment.turn)
      environment.turn = -environment.turn
      # print(environment.turn, "\n")
      if done:
        break

  def gameWithPlayer(self, environment, computerSide):
    RenderKey = ["O", "_", "X"]
    self.epsilon = self.epsilonStart
    oldState = environment.reset()
    i = 0
    for i in range(TTTBot.maxSteps):
      if(environment.turn == (computerSide)):
        print(oldState)
        action = self.move(oldState, False)
      else:
        action = int(input("Enter a Move(0-8): "))
      newState, reward, done, whoWon = environment.step(action)
      oldState = newState
      environment.turn = -environment.turn
      environment.render()
      if done:
        break
    if i == 9:
      print("Tie!")
    else:
      print(RenderKey[environment.turn+1] + " Won!!!")

  def move(self, state, useEpsilon):
    if random.random() > self.epsilon or (not useEpsilon):
      return self.PTable[state]
    else:
      return random.randint(0, 8)

  def updatePTable(self, state, turn):
    if(turn == 1):
      self.PTable[state] = np.argmax(self.QTable[state])
    else:
      self.PTable[state] = np.argmin(self.QTable[state])

  def TempDiffQTable(self, oldState, newState, action, reward, turn):
    if (turn == 1):
      self.QTable[oldState][action] = (1-self.learningRate) * self.QTable[oldState][action] + self.learningRate * (reward + self.gamma * min(self.QTable[newState]))
    else:
      self.QTable[oldState][action] = (1-self.learningRate) * self.QTable[oldState][action] + self.learningRate * (reward + self.gamma * max(self.QTable[newState]))
