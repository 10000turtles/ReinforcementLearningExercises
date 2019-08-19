import numpy as np
import random
import pickle


class NNL:
  def __init__(self, layerSizes, LearningRate):
    self.nodes = layerSizes
    self.weights = [np.matrix(randomMatrix(self.nodes[i+1], self.nodes[i]))/self.nodes[0] for i in range(len(self.nodes)-1)]
    self.biases = [np.matrix(randomMatrix(self.nodes[i+1], 1)) for i in range(len(self.nodes)-1)]
    self.lastOutputs = [np.matrix(randomMatrix(self.nodes[i], 1)) for i in range(len(self.nodes))]
    self.LearningRate = LearningRate

  def ff(self, inputs):
    outputs = inputs
    self.lastOutputs[0] = inputs
    for i in range(len(self.nodes)-1):
      outputs = np.matmul(self.weights[i], outputs)
      outputs += self.biases[i]
      outputs = sigmoid(outputs)
      self.lastOutputs[i+1] = outputs
    return outputs

  def bp(self, inputs, targets):
    self.ff(inputs)
    length = len(self.biases)  # for [3,7,2] this is 2
    adj = [np.matrix([]) for i in range(length)]
    errors = [np.matrix([]) for i in range(length)]
    errors[length-1] = self.lastOutputs[length] - targets
    delta = np.multiply(errors[length-1], dsigmoid(self.lastOutputs[length]))
    adj[length-1] = np.matmul(delta, self.lastOutputs[length-1].T)

    for i in range(length-2, -1, -1):
      errors[i] = np.matmul(delta.T, self.weights[i+1]).T
      delta = np.multiply(errors[i], dsigmoid(self.lastOutputs[i+1]))
      adj[i] = np.matmul(delta, self.lastOutputs[i].T)
    for i in range(len(adj)):
      self.weights[i] -= self.LearningRate*adj[i]

  def trainPrint(self, datasetI, datasetT, iterations, testIterations, equalsMethod):
    print("Before: ")
    self.accuracy(datasetI, datasetT, testIterations, equalsMethod)
    self.train(datasetI, datasetT, iterations)
    print("\nAfter: ")
    self.accuracy(datasetI, datasetT, testIterations, equalsMethod)

  def train(self, datasetI, datasetT, iterations, isPrint = False):
    for i in range(iterations):
      if(isPrint):
        if i % (iterations/100) < 1:
          print(str(float(i/iterations)*100)+"% Complete")
      num = random.randint(0, len(datasetI)-1)
      inputs = np.matrix([datasetI[num]]).T
      targets = np.matrix([datasetT[num]]).T
      self.bp(inputs, targets)

  def accuracy(self, datasetI, datasetT, iterations, equalsMethod):
    counter = 0
    for i in range(iterations):
      num = random.randint(0, len(datasetI)-1)
      inputs = np.matrix([datasetI[num]]).T
      outputs = self.ff(inputs)
      if equalsMethod(outputs, datasetT[num]):
        counter += 1
    print("Accuracy: " + str(float(counter/iterations*100)) + "%")

  def save(self, file):
    filehandler = open(file, "wb")
    pickle.dump(self, filehandler)

  def load(self, file):
    filehandler = open(file, "rb")
    placeholder = pickle.load(filehandler)
    self.copy(placeholder)

  def copy(self, obj):
    self.nodes = obj.nodes
    self.weights = obj.weights
    self.biases = obj.biases
    self.lastOutputs = obj.lastOutputs
    self.LearningRate = obj.LearningRate


def sigmoid(x):
  return 1 / (1 + np.exp(-x))


def dsigmoid(x):
  return np.multiply(x, (1-x))


def randomMatrix(r, c):
  return [[random.random() for i in range(c)]for j in range(r)]
