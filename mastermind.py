import numpy as np

class Mastermind:
    def __init__(self, cols, rows):
        self.cols = cols
        self.rows = rows
        self.board = np.zeros((self.rows, self.cols), dtype=int) 

    def board(self):
        return board
