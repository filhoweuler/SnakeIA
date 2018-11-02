import numpy as np
import json
import os

def sigmoid(x, derivative=False):
    return x*(1.0-x) if derivative else 1.0/(1.0+np.exp(-x))

class NeuralNet:

    def __init__(self, base_in, base_out, input_size, hidden_size, output_size, saved_weight1=None, saved_weight2=None):

        self.input = base_in
        self.y = base_out

        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size

        if saved_weight1 is None:
            self.weights_input = np.random.rand(input_size,hidden_size)
        else:
            self.weights_input = saved_weight1

        if saved_weight2 is None:
            self.weights_output = np.random.rand(hidden_size,output_size)
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
        d_weights2 = np.dot(self.layer1.T, (2*(self.y - self.output) * sigmoid(self.output, True)))
        d_weights1 = np.dot(self.input.T,  (np.dot(2*(self.y - self.output) * sigmoid(self.output, True), self.weights_output.T) * sigmoid(self.layer1, True)))

        # update the weights with the derivative (slope) of the loss function
        self.weights_input += d_weights1
        self.weights_output += d_weights2
    
    def get_output(self, input):
        self.feedforward(input)
        return self.output

    
if __name__ == "__main__":
    # X = np.array([[0,0,1],
    #                 [0,1,1],
    #                 [1,0,1],
    #                 [1,1,1]])
    # y = np.array([[0],[1],[1],[0]])
    # nn = NeuralNet(X,y,3,8,1)

    # for i in range(5000):
    #     nn.feedforward()
    #     nn.backpropagation()

    # print(nn.output)
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
    
    neural_net = NeuralNet(input, out, 12, 18, 4)

    for i in range(2000):
        neural_net.feedforward()
        neural_net.backpropagation()

    for k in neural_net.output:
        print(k)

    w1 = neural_net.weights_input.tolist()
    w2 = neural_net.weights_output.tolist()

    with open('w1', 'w') as out:
        json.dump(w1, out)

    with open('w2', 'w') as out:
        json.dump(w2, out)
