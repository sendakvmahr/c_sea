import numpy as np
import random

def matrix_height(m):
    if len(m.shape) == 1:
        return 1
    return m.shape[0]

def matrix_width(m):
    return m.shape[1]

def prepend_column_of_ones(arr):
    if matrix_height(arr) == 1:
        return np.array([1] + list(arr))
    ones = np.array([[1] for i in range(matrix_height(arr))])
    return np.append(ones, arr, axis=1)

def Numerical_Predictor():
    def __init__(self):
        raise NotImplementedError("Not implemented in base classes.")

    def predict(self):
        raise NotImplementedError("Not implemented in base classes.")

    def train(self):
        raise NotImplementedError("Not implemented in base classes.")

def list_to_col_vec(l):
    return np.transpose(np.array([l]))

class Linear_Regression():
    def __init__(self, learning_rate):
        self.m = random.random()
        self.b = random.random()
        self.m = .4
        self.b = .6
        self.learning_rate = learning_rate

    def predict(self, x):
        """x can be an int, float, or numpy array"""
        return self.m*x + self.b

    def train(self, inputs, outputs, epochs):
        """Gradient descent."""
        count = len(inputs)
        k = self.learning_rate/(2*count)
        inputs = np.array(inputs)

        for i in range(epochs):
            hyp = self.m * inputs + self.b
            difference = outputs - hyp
            self.m = self.m + k * sum(difference * inputs)
            self.b = self.b + k * sum(difference)
        
    def error(self, inputs, outputs):
        count = len(inputs)
        inputs = np.array([[self.predict(i) for i in inputs]])
        outputs = np.array(outputs)
        return np.sum((inputs-outputs)**2)/(2*count)

EPOCHS = 50
inputs =  [1, 2, 3, 4, 5, 6, 48] 
outputs = [2, 4, 6, 8, 10, 12, 96] 

c = Linear_Regression(.001)
print("e-1: ", c.error(inputs, outputs))
c.train(inputs, outputs, EPOCHS)
print("y = {}x + {}".format(c.m, c.b))
print("error: ", c.error(inputs, outputs))
#for i in inputs:
#    print(i, c.predict(i))

print(linear_regression(np.array(inputs), np.array(outputs), .4, .6, EPOCHS, .001))
