import ai.neuralnetwork as nn
import numpy as np


class Bot:
    def __init__(self, col, rows, input_range):
        self.brain = nn.build_model(col * 2 * rows, input_range * rows)
        self.input_range = input_range
        # output:
        # _ -> 8
        # _ -> 8
        # _ -> 8
        # _ -> 8

    def think(self, board, hints_board):
        game_board = np.concatenate((board, hints_board))
        nn_input = np.resize(game_board, (1, game_board.size))
        prediction_result = list(self.brain.predict(nn_input)[0])
        position_1 = (
            prediction_result[0 : self.input_range].index(
                max(prediction_result[0 : self.input_range])
            )
            + 1
        )
        position_2 = (
            prediction_result[self.input_range : self.input_range * 2].index(
                max(prediction_result[self.input_range : self.input_range * 2])
            )
            + 1
        )
        position_3 = (
            prediction_result[self.input_range * 2 : self.input_range * 3].index(
                max(prediction_result[self.input_range * 2 : self.input_range * 3])
            )
            + 1
        )
        position_4 = (
            prediction_result[self.input_range * 3 : self.input_range * 4].index(
                max(prediction_result[self.input_range * 3 : self.input_range * 4])
            )
            + 1
        )
        return [position_1, position_2, position_3, position_4]
