from ai.neuralnetwork import Brain
import numpy as np
import math


class Bot:
    def __init__(self, col, rows, input_range, brain=None):
        if brain:
            self.brain = brain
            self.input_range = input_range
        else:
            self.brain = Brain(col * 2 * rows, col)
        self.input_range = input_range
        self.score = 0
        # output:
        # _ -> 8
        # _ -> 8
        # _ -> 8
        # _ -> 8

    def think(self, board, hints_board):
        game_board = np.concatenate((board / float(self.input_range), hints_board / 2.0))    # normalize input
        nn_input = np.resize(game_board, (1, game_board.size))
        prediction_result = list(self.brain.nn_model.predict(nn_input)[0])
        position_1 = math.ceil(prediction_result[0] * self.input_range)
        position_2 = math.ceil(prediction_result[1] * self.input_range)
        position_3 = math.ceil(prediction_result[2] * self.input_range)
        position_4 = math.ceil(prediction_result[3] * self.input_range)
        return [position_1, position_2, position_3, position_4]
