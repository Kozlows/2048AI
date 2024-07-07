import numpy as np
import random

class NeuralNetwork(object):
    def __init__(self, inputAmount, outputAmount):
        self.inputs = inputAmount
        self.outputs = outputAmount
        self.layers = self.initLayers()
    
    def initLayers(self):
        layers = list()
        layers.append(Layer((4), (4)))
        layers.append(Layer((4), (1))) 
        return layers

    def boardInput(self, board):
        directions = "lurd"
        d = {i : c for i, c in enumerate("lurd")}
        output = board
        for layer in self.layers:
            output = [node.calculate(output[i]) for i, node in enumerate(layer.nodes)]
        biggest = np.max(output)
        return d[output.index(biggest)]


class Layer(object):
    def __init__(self, inputShape, outputShape):
        self.nodes = self.initNodes(inputShape, outputShape)
    
    def initNodes(self, inputShape, outputShape):
        nodes = [Node(inputShape, outputShape) for i in range(4)]
        return nodes

class Node(object):
    def __init__(self, inputShape, outputShape):
        self.ishape = inputShape
        self.oshape = outputShape
        self.weights, self.biases = self.initValues()
    
    def randomValue(self):
        return (random.random() * 2) - 1

    def initValues(self):
        weights = list()
        biases = list()
        if self.ishape == self.oshape:
            weights = [[self.randomValue() for i in range(self.ishape)] for j in range(self.oshape)]
            biases = [self.randomValue() for i in range(self.oshape)]
        elif self.oshape == 1:
            weights = [self.randomValue() for i in range(self.ishape)]
            biases = [self.randomValue()]

        return weights, biases

    def calculate(self, inputs):
        return np.dot(self.weights, inputs) + self.biases
