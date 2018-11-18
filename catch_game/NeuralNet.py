import numpy as np
import json
import os

def sigmoid(x, derivative=False):
    return x*(1.0-x) if derivative else 1.0/(1.0+np.exp(-x))

class NeuralNet:

    def __init__(self, base_in, base_out, input_size, hidden_size, output_size, saved_weight1=None, saved_weight2=None):

        self.LEARNING_RATE = 0.0005

        self.input = base_in
        self.y = base_out

        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size

        if saved_weight1 is None:
            self.weights_input = np.random.rand(input_size,hidden_size) - 0.5
        else:
            self.weights_input = saved_weight1

        if saved_weight2 is None:
            self.weights_output = np.random.rand(hidden_size,output_size) - 0.5
        else:
            self.weights_output = saved_weight2

    def feedforward(self, input=None):
        input_array = []

        if input is None:
            input_array = np.array(self.input, ndmin=2)
        else:
            input_array = np.array(input, ndmin=2)

        self.layer1 = sigmoid(np.dot(input_array, self.weights_input))
        self.output = sigmoid(np.dot(self.layer1, self.weights_output))
    
    def backpropagation(self):
        # application of the chain rule to find derivative of the loss function with respect to weights2 and weights1
        d_weights2 = np.dot(self.layer1.T, ((self.y - self.output) * sigmoid(self.output, True)))
        d_weights1 = np.dot(self.input.T,  (np.dot((self.y - self.output) * sigmoid(self.output, True), self.weights_output.T) * sigmoid(self.layer1, True)))

        # update the weights with the derivative (slope) of the loss function
        self.weights_input += d_weights1 * self.LEARNING_RATE
        self.weights_output += d_weights2 * self.LEARNING_RATE
    
    def get_output(self, input):
        self.feedforward(input)
        return self.output

    
if __name__ == "__main__":
    data = []

    path = os.getcwd() + '/base_weuler'
    for filename in os.listdir(path):
        with open(path + '/' + filename) as f:
            data = data + json.load(f)
    
    input = []
    out = []

    for d in data:
        input.append(d[0])
        out.append(d[1])

    input = np.array(input)
    out = np.array(out)
    
    neural_net = NeuralNet(input, out, 2, 20, 1)

    epochs = 10000
    diff = 5
    while(diff > 0.06 and epochs > 0):
        epochs -= 1
        past_diff = diff
        neural_net.feedforward()
        diff = np.sum((neural_net.output - neural_net.y)**2)/len(neural_net.input)
        print(diff)
        neural_net.backpropagation()

    w1 = neural_net.weights_input.tolist()
    w2 = neural_net.weights_output.tolist()

    with open('w1', 'w') as out:
        json.dump(w1, out)

    with open('w2', 'w') as out:
        json.dump(w2, out)

    neural_net.feedforward(np.array([20, 100]))
    print(neural_net.output)
    neural_net.feedforward(np.array([300, 100]))
    print(neural_net.output)
    neural_net.feedforward(np.array([200, 150]))
    print(neural_net.output)