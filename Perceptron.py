import numpy as np

def collect_user_input():
    weights = np.array([float(x) for x in input("Enter initial weights (e.g., 0.5 0.5): ").split()])
    learning_rate = float(input("Enter learning rate value: "))
    bias = float(input("Enter bias value: "))
    n = int(input("Enter the number of training examples: "))
    training_examples = []
    for i in range(n):
        row = input(f"Enter input and expected output for example {i+1} (e.g., 1 0 1): ").split()
        training_examples.append(([int(row[0]), int(row[1])], int(row[2])))
    return weights, learning_rate, bias, training_examples

def train_perceptron(weights, learning_rate, bias, data):
    for epoch in range(100):
        for input_vector, target in data:
            result = np.dot(input_vector, weights) + bias
            prediction = 1 if result >= 0 else 0
            error = target - prediction
            weights += learning_rate * error * np.array(input_vector)
            bias += learning_rate * error
    return weights, bias

def test_perceptron(weights, bias):
    while True:
        test_input = input("Enter input for test (e.g., 1 0) or 'leave' to quit: ")
        if test_input == 'leave':
            break
        input_vector = np.array([int(x) for x in test_input.split()])
        result = np.dot(input_vector, weights) + bias
        prediction = 1 if result >= 0 else 0
        print(f"Output: {prediction}")

weights, learning_rate, bias, data = collect_user_input()
weights, bias = train_perceptron(weights, learning_rate, bias, data)
print("Training accomplished.")
test_perceptron(weights, bias)
