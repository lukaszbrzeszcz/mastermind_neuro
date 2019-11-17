import ai.neuralnetwork as nn
import numpy as np


class Bot:
    def __init__(self, col, rows, input_range, brain=None):
        if brain:
            self.brain = brain
            self.input_range = input_range
        else:
            self.brain = nn.build_model(col * 2 * rows, rows)
        self.input_range = input_range
        self.score = 0
        # output:
        # _ -> 8
        # _ -> 8
        # _ -> 8
        # _ -> 8

    def think(self, board, hints_board):
        game_board = np.concatenate((board, hints_board))
        game_board = game_board/self.input_range
        nn_input = np.resize(game_board, (1, game_board.size))
        prediction_result = list(self.brain.predict(nn_input)[0])
        position_1 = round(prediction_result[0]*self.input_range)
        position_2 = round(prediction_result[1]*self.input_range)
        position_3 = round(prediction_result[2]*self.input_range)
        position_4 = round(prediction_result[3]*self.input_range)
        return [position_1, position_2, position_3, position_4]
