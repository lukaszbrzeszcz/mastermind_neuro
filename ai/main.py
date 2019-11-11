import ai.neuralnetwork as nn

if __name__ == "__main__":
    input_data = [1, 1, 0, 1]
    nn_model = nn.build_model(input_data, 18)
    print(nn_model.summary())
