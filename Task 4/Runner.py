from gym.envs.toy_text.frozen_lake import generate_random_map
from DeepQLearning import FrozenLakeBot
import gym
import math

game = "FrozenLake8x8-v0"
mapSize = 3
LearningRate = 0.1
LayerSizes = [mapSize**2+(math.ceil(math.log2(mapSize))*2), mapSize, 4]
gamma = 1
epsilon = 1
holeProb = 0.4
iterations = 5

bot = FrozenLakeBot(gamma, epsilon, LearningRate, LayerSizes, mapSize)

for i in range(iterations):
  counter = 0
  random_map = generate_random_map(size = mapSize, p = (1-holeProb))
  env = gym.make(game, desc = random_map)
  while(True):
    counter += 1
    print(counter)
    isPrint = counter % 1000 == 0
    if(bot.trainingGame(env, isPrint)):
      break
    if isPrint:
      input("Press Enter to Continue")
  if(i % 1 == 0):
    print(str(float(i/iterations*100)) + "% Complete")
for i in range(2):
  oldState = env.reset()
  for i in range(50):
    action = bot.move(oldState, env)
    print(action)
    newState, reward, done, info = env.step(action)
    env.render()
    oldState = newState
    if done:
      break
