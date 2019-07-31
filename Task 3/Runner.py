from TemporalDifference import TaxiBot
import gym

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
