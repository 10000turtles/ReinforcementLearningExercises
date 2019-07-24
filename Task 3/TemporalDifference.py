import gym
import random
import numpy as np


def analyze(obj):
  object_methods = [method_name for method_name in dir(environment)
                    if callable(getattr(environment, method_name))]
  print(object_methods)
  print(environment.__dict__.keys())


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
      action = bot.move(oldState, True)
      newState, reward, done, garbo = environment.step(action)

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
    self.QTable[oldState][action] = (1-self.learningRate)*self.QTable[oldState][action]+self.learningRate*(reward+self.gamma*max(self.QTable[newState]))


game = "Taxi-v2"
environment = gym.make(game)
bot = TaxiBot(0.9, 0.1, 0)
iterations = 3000

for i in range(iterations):
  if(i % 10 == 0):
    print(str(float(i/iterations*100)) + "% Complete")
  bot.trainingGame(environment)

state = environment.reset()
for i in range(TaxiBot.maxSteps):

  action = bot.move(state, False)
  print(bot.QTable[state])
  state, r, d, g = environment.step(action)
  environment.render()
  if d:
    break
