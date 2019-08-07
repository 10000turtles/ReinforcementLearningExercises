from GridEnvironment import GridEnvironment
from MonteCarlo import GridWorldBot
data = [["0", "0", "0", "0", "0", "0"],
        ["0", "_", "_", "_", "W", "0"],
        ["0", "_", "0", "_", "L", "0"],
        ["0", "_", "_", "_", "_", "0"],
        ["0", "0", "0", "0", "0", "0"]]
iterations = 20000
board = GridEnvironment(data, (3, 1), [.8, .1, 0, .1], .9)
bot = GridWorldBot(board, 0.9, 0.9)
for i in range(iterations):
  if(i % 100 == 0):
    print(str(float(i/iterations*100)) + "% Complete")
  bot.monteCarloTraining(board)
bot.printPolicyTable(board)
