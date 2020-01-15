from ai.neuralnetwork import Brain
import numpy as np
import random
import math


class Bot:
    def __init__(self, col, rows, input_range, brain=None, name=""):
        if brain:
            self.brain = brain
            self.input_range = input_range
        else:
            self.brain = Brain(col * 2 * rows, col)
        self.name = name
        self.input_range = input_range
        self.score = 0
        # output:
        # _ -> 8
        # _ -> 8
        # _ -> 8
        # _ -> 8

    def think(self, board, hints_board, random_input):
        game_board = np.concatenate((board, hints_board))    # normalize input
        nn_input = np.resize(game_board, (1, game_board.size))
        prediction_result = list(self.brain.nn_model.predict(nn_input)[0])
        # position_1 = math.ceil(prediction_result[0] * self.input_range)
        if random_input:
            positions = [random.randint(1,8) for i in range(4)]
            return positions
        #print(prediction_result[0:8])
        position_1 = prediction_result[0:8].index(max(prediction_result[0:8])) + 1
        position_2 = prediction_result[9:17].index(max(prediction_result[9:17])) + 1
        position_3 = prediction_result[18:26].index(max(prediction_result[18:26])) + 1
        position_4 = prediction_result[27:35].index(max(prediction_result[27:35])) + 1
        # position_2 = math.ceil(prediction_result[1] * self.input_range)
        # position_3 = math.ceil(prediction_result[2] * self.input_range)
        # position_4 = math.ceil(prediction_result[3] * self.input_range)
        return [position_1, position_2, position_3, position_4]
