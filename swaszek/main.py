from mastermind import Mastermind
from itertools import product
import random
MAX_NUMBER = 6

if __name__ == '__main__':
    solution = [random.randint(1,MAX_NUMBER) for i in range(4)]
    mm = Mastermind(4, 8, solution, MAX_NUMBER)
    mm.play_swaszek()
