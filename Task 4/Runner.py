from gym.envs.toy_text.frozen_lake import generate_random_map
from DeepQLearning import FrozenLakeBot
import gym

game = "FrozenLake8x8-v0"
mapSize = 6
LearningRate = 0.1
LayerSizes = [mapSize**2+6, mapSize, 4]
gamma = 1
epsilon = 1
holeProb = 0.2
iterations = 2000

bot = FrozenLakeBot(gamma, epsilon, LearningRate, LayerSizes)


for i in range(iterations):
  random_map = generate_random_map(size=mapSize, p=(1-holeProb))
  env = gym.make(game, desc=random_map)
  bot.trainingGame()

env.render()
