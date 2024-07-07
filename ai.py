import numpy as np

class Network(object): # A Neural Network Model
    def __init__(self, generateNewData=False, storedLocation="tuningPoints.txt"):
        self.layers = self.initLayers()
        self.direction = self.initDirections()
        self.saveLocation = storedLocation
        if not generateNewData:
            self.updateLayers()
        self.updateSave()
    
    def updateSave(self):
        with open(self.saveLocation, "w") as f:
            f.write(f"{self}")

    def updateLayers(self):
        with open(self.saveLocation, "r") as f:
            text = "".join(f.readlines())

        text = text.split("\n")
        layers = [[list() for i in range(2)] for layer in self.layers]

        count = -1
        for line in text:
            if line[0].isdigit() or line[0] == "-":
                count += 1
                nums = [float(n) if n != "0." else float(0) for n in line.strip().split()]
                layers[count // 2][count % 2] = nums
            else:
                nums = [float(n) if n != "0." else 0 for n in line.strip().split()]
                if type(layers[count // 2][count % 2][0]) == list:
                    layers[count // 2][count % 2].append(nums)
                else:
                    layers[count // 2][count % 2] = [layers[count // 2][count % 2], nums]

        for i in range(len(self.layers)):
            self.layers[i].weights = np.array(layers[i][0])
            self.layers[i].biases = np.array(layers[i][1])

    def initDirections(self):
        return {i : c for i, c in enumerate("lurd")}

    def aiDidBadMove(self, score):
        pass

    def initLayers(self):
        layers = list()
        layers.append(Layer(4, 4, ActivationReLU()))
        layers.append(Layer(1, 4, ActivationSoftmax()))
        return layers
    
    def chooseDirection(self, boardInput):
        for layer in self.layers:
            boardInput = layer.forward(boardInput)
        self.latestMove = (self.direction[boardInput.argmax()], boardInput)
        return self.direction[self.latestMove[0]]

    def __str__(self):
        return "\n".join([f"{layer}" for layer in self.layers])

class Layer(object): # A layer model
    def __init__(self, nInputs, nNeurons, activation): # Number of inputs each neuron will take in, and the number of neurons the layer will have
        self.activation = activation
        self.rng = np.random.default_rng()
        self.weights = 0.1 * self.rng.standard_normal((nInputs, nNeurons))
        self.biases = np.zeros((1, nNeurons))

    def forward(self, inputs):
        dotProduct = np.dot(self.weights, inputs)
        dotProduct += self.biases
        output = self.activation.forward(dotProduct)
        return output
    
    def __str__(self):
        weights = f"{self.weights}".replace("[", "").replace("]", "").strip()
        biases = f"{self.biases}".replace("[", "").replace("]", "").strip()
        return f"{weights}\n{biases}"

class ActivationReLU(object): # ReLU Activation function, used to make each node non-linear, works well, used for all hidden layers
    def forward(self, inputs):
        return np.maximum(0, inputs)

class ActivationSoftmax(object): # Softmax Activation function, used to normalize the output of a network, usually used on the output layer
    def forward(self, inputs):
        expValues = np.exp(inputs - np.max(inputs, axis=1, keepdims=True))
        probabilities = expValues / np.sum(expValues, axis=1, keepdims=True)
        return probabilities

class Loss(object):
    def calculate(self, softMaxOutput, expectedOutputIndex):
        dataLoss = self.forward(softMaxOutput, expectedOutputIndex)
        return dataLoss