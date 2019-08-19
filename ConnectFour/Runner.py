from ConnectFour import ConnectFour
from MCTS import MCTS
import subprocess as sp
import time
columns = 5
rows = 4
winNum = 3
games = 50
iterations = 20000
visitThreshold = 100

env = ConnectFour(columns, rows, winNum, 1, [])
# env.decodeState("0000020000000000000001110000220000000000001")
bot = MCTS(env, visitThreshold)
outcomes = [0, 0, 0, 0, 0, 0]
averageTime = 1
timesCounted = 1
for i in range(iterations):
  start = time.time()

  out = bot.train(env, games)

  end = time.time()
  outcomes[out] += 1
  averageTime = (averageTime + ((end-start)/(timesCounted)))*((timesCounted)/(timesCounted+1))
  timesCounted += 1
  if(i % (10) == 0):
    tmp = sp.call('clear', shell=True)
    print(str(float(i/iterations*100)) + "% Complete")
    ESTHours = (averageTime*(iterations-i))/3600
    ESTMinutes = (ESTHours % 1)*60
    ESTSeconds = (ESTMinutes % 1)*60
    ESTHours = int(ESTHours)
    ESTMinutes = int(ESTMinutes)
    ESTSeconds = int(ESTSeconds)
    print("Estimated time: "+str(ESTHours)+"h "+str(ESTMinutes)+"m "+str(ESTSeconds)+"s ")
print(outcomes)
# MCTS.printTree(bot.home, 0)
for i in range(3):
  bot.playGameWithPlayer(env)
bot.save("Tree.obj")
