from ConnectFour import ConnectFour
from MCTS import MCTS


columns = 7
rows = 6
winNum = 4
games = 100
iterations = 2
env = ConnectFour(columns, rows, winNum, 1, [])
bot = MCTS(env)
bot.save("Tree.obj")
for i in range(iterations):
  bot.train(env, games)
