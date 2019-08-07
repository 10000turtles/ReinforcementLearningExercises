from TicTacToe import TicTacToe
from TTTBot import TTTBot
import random
import subprocess as sp

environment = TicTacToe()
bot = TTTBot(0.9, 0.1, 0.5)
iterations = 600000

for i in range(iterations):
  if(i % 1000 == 0):
    tmp = sp.call('clear', shell=True)
    print(str(float(i/iterations*100)) + "% Complete")
  bot.trainingGame(environment)

# state = environment.reset()
# print("\n"*10)
# for i in range(TTTBot.maxSteps):

#   action = bot.move(state, False)
#   print(bot.QTable[state])
#   print(bot.PTable[state])
#   state, r, d, g = environment.step(action)
#   # print(d)
#   environment.turn = -environment.turn
#   environment.render()
#   if d:
#     break

for i in range(5):
  bot.gameWithPlayer(environment, (random.randint(0, 1)*2)-1)
