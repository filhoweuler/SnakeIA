import numpy as np
import json
import os

def sigmoid(x, derivative=False):
    return x*(1.0-x) if derivative else 1.0/(1.0+np.exp(-x))
    #return np.greater(x,0).astype(int) if derivative else np.maximum(x,0,x)

class NeuralNet:

    def __init__(self, base_in, base_out, input_size, hidden_size, output_size, saved_weight1=None, saved_weight2=None, saved_weight3=None):

        self.input = base_in
        self.y = base_out

        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size

        if saved_weight1 is None:
            self.w1 = np.random.uniform(-0.5, 0.5, (input_size,hidden_size))
        else:
            self.w1 = saved_weight1

        if saved_weight2 is None:
            self.w2 = np.random.uniform(-0.5, 0.5, (hidden_size,hidden_size))
        else:
            self.w2 = saved_weight2

        if saved_weight3 is None:
            self.w3 = np.random.uniform(-0.5, 0.5, (hidden_size,output_size))
        else:
            self.w3 = saved_weight3

    def feedforward(self, input=None):
        input_array = []

        if input is None:
            input_array = np.array(self.input, ndmin=2)
        else:
            print("recebi input")
            print(input)
            input_array = np.array(input, ndmin=2)

        self.layer1 = sigmoid(np.dot(input_array, self.w1))
        self.layer2 = sigmoid(np.dot(self.layer1, self.w2))
        self.output = sigmoid(np.dot(self.layer2, self.w3))
    
    def backpropagation(self):
        # application of the chain rule to find derivative of the loss function with respect to weights2 and weights1
        d_weights3 = np.dot(self.layer2.T, (2*(self.y - self.output) * sigmoid(self.output, True)))
        d_weights2 = np.dot(self.layer1.T,  (np.dot(2*(self.y - self.output) * sigmoid(self.output, True), self.w3.T) * sigmoid(self.layer2, True)))
        d_weights1 = np.dot(self.input.T,  (np.dot(np.dot(2*(self.y - self.output) * sigmoid(self.output, True), self.w3.T), self.w2.T) * sigmoid(self.layer1, True)))

        # update the weights with the derivative (slope) of the loss function
        self.w1 += d_weights1*0.1
        self.w2 += d_weights2*0.1
        self.w3 += d_weights3*0.1
    
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

    input = np.array(input, ndmin=2)
    out = np.array(out, ndmin=2)

    #xor_in = np.array([[0,0], [0,1], [1,0], [1,1]])
    #xor_out = np.array([[0], [1], [1], [0]])
    
    neural_net = NeuralNet(input, out, 4, 16, 4)

    for i in range(5000):
        neural_net.feedforward()
        #print(neural_net.output)
        # diff = np.sum((neural_net.output - neural_net.y)**2)/len(neural_net.input)
        # print(diff)
        neural_net.backpropagation()

    # for k in neural_net.output:
    #     print(k)

    w1 = neural_net.w1.tolist()
    w2 = neural_net.w2.tolist()
    w3 = neural_net.w3.tolist()

    with open('w1', 'w') as out:
        json.dump(w1, out)

    with open('w2', 'w') as out:
        json.dump(w2, out)
    
    with open('w3', 'w') as out:
        json.dump(w3, out)
